import asyncio
import pytest
import os
import sys

# Ensure backend and root are in python path
sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

from app.core.database import SessionLocal, init_db
from app.models.event import Event
from app.streaming.memory_stream import MemoryProducer
from app.consumer import stream_consumer_service
from producer.replay_traffic import TrafficGenerator

@pytest.mark.asyncio
async def test_end_to_end_streaming_pipeline():
    init_db()
    
    # 1. Start consumer service
    await stream_consumer_service.start()
    
    # 2. Produce test events
    producer = MemoryProducer()
    await producer.connect()
    
    test_events_count = 15
    for _ in range(test_events_count):
        flow = TrafficGenerator.generate_flow()
        await producer.send_event("network_traffic_stream", flow)
    
    # Allow async consumer to process
    await asyncio.sleep(0.5)
    
    # 3. Verify in database
    db = SessionLocal()
    try:
        events = db.query(Event).all()
        assert len(events) >= test_events_count, f"Expected at least {test_events_count} events, found {len(events)}"
        sample_event = events[-1]
        assert sample_event.src_ip is not None
        assert sample_event.dst_port > 0
        assert sample_event.prediction in ["Benign", "DoS-Hulk", "DDoS-LOIC-HTTP", "Botnet", "SSH-Bruteforce", "Infiltration"]
        assert sample_event.inference_latency_ms >= 0.0
    finally:
        db.close()
        await stream_consumer_service.stop()
