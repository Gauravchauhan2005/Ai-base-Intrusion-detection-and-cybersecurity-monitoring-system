import asyncio
import logging
import time
from collections import deque
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.event import Event
from app.models.alert import Alert
from app.streaming.factory import get_stream_consumer
from app.streaming.base import BaseConsumer
from app.services.inference_service import inference_service
from app.services.alert_engine import alert_engine
from app.services.websocket_manager import ws_manager

logger = logging.getLogger("stream_consumer")

class StreamConsumerService:
    def __init__(self):
        self.consumer: Optional[BaseConsumer] = None
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # Telemetry & Performance Tracking
        self.events_processed = 0
        self.total_alerts = 0
        self.latencies: deque = deque(maxlen=200)
        self.recent_events_timestamps: deque = deque(maxlen=1000)
        self.history_time_series: deque = deque(maxlen=60)  # 60 1-second snapshots
        self._last_snapshot_sec = int(time.time())
        self._snapshot_events_count = 0
        self._snapshot_alerts_count = 0

    async def start(self):
        if self._running:
            return
        self._running = True
        self.consumer = get_stream_consumer()
        await self.consumer.connect()
        self._task = asyncio.create_task(self._run_consumer())
        logger.info(f"Stream consumer service started on topic '{settings.STREAM_TOPIC}'")

    async def _run_consumer(self):
        try:
            await self.consumer.consume(
                topic=settings.STREAM_TOPIC,
                group=settings.CONSUMER_GROUP,
                callback=self.process_event
            )
        except asyncio.CancelledError:
            logger.info("Stream consumer task cancelled.")
        except Exception as e:
            logger.error(f"Stream consumer encountered unexpected error: {e}", exc_info=True)

    async def process_event(self, raw_flow: Dict[str, Any]):
        now = time.time()
        self.events_processed += 1
        self.recent_events_timestamps.append(now)
        self._snapshot_events_count += 1

        # 1. Real-time ML Inference (XGBoost + Isolation Forest)
        inf_res = inference_service.predict_flow(raw_flow)
        latency_ms = inf_res["inference_latency_ms"]
        self.latencies.append(latency_ms)

        prediction = inf_res["prediction"]
        confidence = inf_res["confidence"]
        anomaly_score = inf_res["anomaly_score"]
        is_anomaly = inf_res["is_anomaly"]

        # 2. Database persistence & Alert processing
        db = SessionLocal()
        created_alert: Optional[Alert] = None
        is_new_alert = False

        alert_payload_to_broadcast = None
        try:
            # Check alert logic
            created_alert, is_new_alert = alert_engine.process_flow_for_alerts(raw_flow, inf_res, db)
            if created_alert:
                self._snapshot_alerts_count += 1
                if is_new_alert:
                    self.total_alerts += 1
                alert_payload_to_broadcast = {
                    "alert_id": str(created_alert.alert_id),
                    "severity": str(created_alert.severity),
                    "attack_type": str(created_alert.attack_type),
                    "confidence": float(created_alert.confidence),
                    "anomaly_score": float(created_alert.anomaly_score),
                    "src_ip": str(created_alert.src_ip),
                    "dst_ip": str(created_alert.dst_ip),
                    "dst_port": int(created_alert.dst_port),
                    "hit_count": int(created_alert.hit_count),
                    "status": str(created_alert.status),
                    "mitigation_action": created_alert.mitigation_action,
                    "timestamp": created_alert.last_seen.isoformat() if created_alert.last_seen else datetime.now(timezone.utc).isoformat(),
                    "is_new": is_new_alert
                }

            # Persist Event flow record
            event_obj = Event(
                src_ip=raw_flow.get("src_ip", "0.0.0.0"),
                dst_ip=raw_flow.get("dst_ip", "0.0.0.0"),
                src_port=raw_flow.get("src_port", 0),
                dst_port=raw_flow.get("dst_port", 0),
                protocol=raw_flow.get("protocol", "TCP"),
                flow_duration=float(raw_flow.get("flow_duration", 0.0)),
                tot_fwd_pkts=int(raw_flow.get("tot_fwd_pkts", 0)),
                tot_bwd_pkts=int(raw_flow.get("tot_bwd_pkts", 0)),
                tot_bytes=int(raw_flow.get("totlen_fwd_pkts", 0) + raw_flow.get("totlen_bwd_pkts", 0)),
                prediction=prediction,
                confidence=confidence,
                anomaly_score=anomaly_score,
                is_anomaly=is_anomaly,
                inference_latency_ms=latency_ms
            )
            db.add(event_obj)
            db.commit()
            event_id = event_obj.id
        except Exception as db_err:
            db.rollback()
            logger.error(f"Error persisting flow/alert to database: {db_err}")
            event_id = 0
        finally:
            db.close()

        # 3. Real-Time WebSocket Telemetry Broadcast
        flow_telemetry = {
            "type": "FLOW",
            "data": {
                "id": event_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "src_ip": raw_flow.get("src_ip", "0.0.0.0"),
                "dst_ip": raw_flow.get("dst_ip", "0.0.0.0"),
                "src_port": raw_flow.get("src_port", 0),
                "dst_port": raw_flow.get("dst_port", 0),
                "protocol": raw_flow.get("protocol", "TCP"),
                "prediction": prediction,
                "confidence": confidence,
                "anomaly_score": anomaly_score,
                "is_anomaly": is_anomaly,
                "latency_ms": latency_ms
            }
        }
        await ws_manager.broadcast_json(flow_telemetry)

        # Broadcast Alert if generated or updated
        if alert_payload_to_broadcast:
            await ws_manager.broadcast_json({
                "type": "ALERT",
                "data": alert_payload_to_broadcast
            })

        # 4. Periodic Snapshot for Time-Series Chart (once per second)
        current_sec = int(now)
        if current_sec > self._last_snapshot_sec:
            avg_lat = sum(self.latencies) / max(1, len(self.latencies))
            self.history_time_series.append({
                "timestamp": datetime.fromtimestamp(current_sec, timezone.utc).strftime("%H:%M:%S"),
                "events_count": self._snapshot_events_count,
                "alerts_count": self._snapshot_alerts_count,
                "avg_latency_ms": round(avg_lat, 2)
            })
            self._last_snapshot_sec = current_sec
            self._snapshot_events_count = 0
            self._snapshot_alerts_count = 0

    def get_current_eps(self) -> float:
        now = time.time()
        # Count events in the last 2 seconds
        recent = [t for t in self.recent_events_timestamps if now - t <= 2.0]
        return round(len(recent) / 2.0, 1)

    def get_avg_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return round(sum(self.latencies) / len(self.latencies), 2)

    def get_p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        import numpy as np
        return round(float(np.percentile(list(self.latencies), 95)), 2)

    async def stop(self):
        self._running = False
        if self.consumer:
            await self.consumer.stop()
            await self.consumer.close()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Stream consumer service stopped.")

# Singleton instance
stream_consumer_service = StreamConsumerService()
