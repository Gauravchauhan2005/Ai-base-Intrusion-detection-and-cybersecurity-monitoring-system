import os
import sys
import time
import json
import asyncio
import argparse
import statistics
import logging
from typing import List

sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

from app.core.database import SessionLocal, init_db
from app.models.alert import Alert
from app.models.event import Event
from app.streaming.factory import get_stream_producer
from app.consumer import stream_consumer_service
from producer.replay_traffic import TrafficGenerator

logging.basicConfig(level=logging.WARNING)

async def run_load_test(duration_sec: int = 5, target_eps: int = 100):
    print("=" * 70)
    print("   AI-IDS REAL-TIME PIPELINE BENCHMARK & LOAD TEST")
    print("=" * 70)
    print(f"Target Throughput  : {target_eps} Events/Sec (EPS)")
    print(f"Benchmark Duration : {duration_sec} Seconds")
    print(f"Target Total Events: {duration_sec * target_eps} Flows")
    print("-" * 70)

    init_db()
    await stream_consumer_service.start()
    producer = get_stream_producer()
    await producer.connect()

    latencies: List[float] = []
    produced_count = 0
    start_time = time.time()
    end_time = start_time + duration_sec

    # Send bursts in 100ms intervals
    interval = 0.1
    batch_size = max(1, int(target_eps * interval))

    while time.time() < end_time:
        step_start = time.perf_counter()
        for _ in range(batch_size):
            flow = TrafficGenerator.generate_flow()
            await producer.send_event("network_traffic_stream", flow)
            produced_count += 1

        elapsed = time.perf_counter() - step_start
        sleep_dur = max(0.0, interval - elapsed)
        if sleep_dur > 0:
            await asyncio.sleep(sleep_dur)

    # Allow consumer to drain remaining events
    print("Flushing stream queue...")
    await asyncio.sleep(1.0)
    total_time = time.time() - start_time

    # Collect stats
    db = SessionLocal()
    try:
        total_events_in_db = db.query(Event).count()
        total_alerts_in_db = db.query(Alert).count()
    finally:
        db.close()

    await stream_consumer_service.stop()

    actual_eps = produced_count / total_time
    consumer_latencies = list(stream_consumer_service.latencies)

    print("\n" + "=" * 70)
    print("                      BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Total Flows Ingested    : {produced_count:,} flows")
    print(f"Total Benchmark Time    : {total_time:.2f} seconds")
    print(f"Effective Ingestion Rate: {actual_eps:.1f} EPS")
    print(f"Total Alerts Triggered  : {total_alerts_in_db:,} alerts")

    if consumer_latencies:
        p50 = statistics.median(consumer_latencies)
        p95 = statistics.quantiles(consumer_latencies, n=20)[18] if len(consumer_latencies) >= 20 else p50
        p99 = statistics.quantiles(consumer_latencies, n=100)[98] if len(consumer_latencies) >= 100 else p95
        mean_lat = statistics.mean(consumer_latencies)

        print("-" * 70)
        print("ML Inference Latency (Dual Engine: XGBoost + Isolation Forest):")
        print(f"  - Mean Latency : {mean_lat:.2f} ms")
        print(f"  - Median (P50) : {p50:.2f} ms")
        print(f"  - 95th % (P95) : {p95:.2f} ms")
        print(f"  - 99th % (P99) : {p99:.2f} ms")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=5, help="Test duration in seconds")
    parser.add_argument("--target-eps", type=int, default=100, help="Target EPS")
    args = parser.parse_args()

    asyncio.run(run_load_test(duration_sec=args.duration, target_eps=args.target_eps))
