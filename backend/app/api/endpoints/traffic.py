import logging
from typing import Dict, Any
from fastapi import APIRouter
from app.schemas.metrics import TrafficControlRequest
from app.streaming.factory import get_stream_producer
from app.core.config import settings
from producer.replay_traffic import TrafficGenerator

logger = logging.getLogger("traffic_api")
router = APIRouter(prefix="/traffic", tags=["Traffic Simulation Control"])

# Simulation runtime state
_SIMULATION_STATE = {
    "rate_eps": 25,
    "is_paused": False
}

@router.get("/status")
def get_traffic_status():
    return _SIMULATION_STATE

@router.post("/control")
async def control_traffic(req: TrafficControlRequest):
    """
    Controls simulated traffic generation:
    - Modifies EPS rate
    - Injects targeted attack bursts (e.g., DDoS, Botnet, SSH Bruteforce)
    - Pauses / Resumes simulation
    """
    if req.rate_eps is not None:
        _SIMULATION_STATE["rate_eps"] = max(1, min(1000, req.rate_eps))
    if req.is_paused is not None:
        _SIMULATION_STATE["is_paused"] = req.is_paused

    injected_count = 0
    if req.burst_attack:
        attack_type = req.burst_attack
        burst_size = req.burst_count or 50
        logger.info(f"Injecting attack burst: {burst_size} packets of {attack_type}...")
        
        producer = get_stream_producer()
        await producer.connect()

        for _ in range(burst_size):
            flow = TrafficGenerator.generate_flow(attack_override=attack_type)
            await producer.send_event(settings.STREAM_TOPIC, flow)
            injected_count += 1

    return {
        "status": "success",
        "simulation_state": _SIMULATION_STATE,
        "injected_packets": injected_count
    }
