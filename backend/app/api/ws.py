import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import ws_manager

logger = logging.getLogger("websocket_route")
router = APIRouter(tags=["WebSocket Telemetry"])

@router.websocket("/ws/live-stream")
async def websocket_live_stream(websocket: WebSocket):
    """
    Real-time bidirectional WebSocket stream for live security alerts and network flow events.
    Supports client heartbeats and subscription filtering.
    """
    await ws_manager.connect(websocket)
    # Send connection greeting
    await websocket.send_text(json.dumps({
        "type": "CONNECTION_ESTABLISHED",
        "data": {
            "message": "Connected to real-time cybersecurity telemetry feed",
            "protocol_version": "1.0"
        }
    }))

    try:
        while True:
            # Await client messages (heartbeat pings or commands)
            text_data = await websocket.receive_text()
            try:
                msg = json.loads(text_data)
                msg_type = msg.get("type")
                if msg_type == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket client loop exception: {e}")
        await ws_manager.disconnect(websocket)
