import asyncio
import logging
from typing import Callable, Awaitable, Dict, Any, Optional
from collections import defaultdict
from app.streaming.base import BaseProducer, BaseConsumer

logger = logging.getLogger(__name__)

# Shared in-memory pub-sub channels
_CHANNELS: Dict[str, asyncio.Queue] = defaultdict(lambda: asyncio.Queue(maxsize=10000))

class MemoryProducer(BaseProducer):
    async def connect(self) -> None:
        logger.info("MemoryProducer connected.")

    async def send_event(self, topic: str, event: Dict[str, Any]) -> bool:
        queue = _CHANNELS[topic]
        try:
            if queue.full():
                # Discard oldest to handle backpressure smoothly in memory
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            await queue.put(event)
            return True
        except Exception as e:
            logger.error(f"Error publishing to in-memory topic {topic}: {e}")
            return False

    async def close(self) -> None:
        pass

class MemoryConsumer(BaseConsumer):
    def __init__(self):
        self._running = False

    async def connect(self) -> None:
        logger.info("MemoryConsumer connected.")

    async def consume(
        self,
        topic: str,
        group: str,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        consumer_id: Optional[str] = None
    ) -> None:
        self._running = True
        queue = _CHANNELS[topic]
        logger.info(f"MemoryConsumer started listening on topic '{topic}'")
        while self._running:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=1.0)
                try:
                    await callback(event)
                except Exception as cb_err:
                    logger.error(f"Error processing in-memory event: {cb_err}", exc_info=True)
                finally:
                    queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                if self._running:
                    logger.error(f"MemoryConsumer loop error: {e}")
                    await asyncio.sleep(0.1)

    async def stop(self) -> None:
        self._running = False

    async def close(self) -> None:
        self._running = False
