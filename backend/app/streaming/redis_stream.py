import asyncio
import json
import logging
from typing import Callable, Awaitable, Dict, Any, Optional
import redis.asyncio as redis
from app.streaming.base import BaseProducer, BaseConsumer

logger = logging.getLogger(__name__)

class RedisStreamProducer(BaseProducer):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        await self.client.ping()
        logger.info(f"Connected to Redis Stream Producer at {self.redis_url}")

    async def send_event(self, topic: str, event: Dict[str, Any]) -> bool:
        if not self.client:
            await self.connect()
        try:
            # Flatten or serialize payload as JSON in field "payload"
            payload = json.dumps(event)
            await self.client.xadd(topic, {"data": payload}, maxlen=50000, approximate=True)
            return True
        except Exception as e:
            logger.error(f"Failed to produce to Redis stream {topic}: {e}")
            return False

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()
            logger.info("Closed Redis Stream Producer connection.")

class RedisStreamConsumer(BaseConsumer):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.client: Optional[redis.Redis] = None
        self._running = False

    async def connect(self) -> None:
        self.client = redis.from_url(self.redis_url, decode_responses=True)
        await self.client.ping()
        logger.info(f"Connected to Redis Stream Consumer at {self.redis_url}")

    async def _ensure_group(self, topic: str, group: str):
        try:
            # Create stream and consumer group if not present
            await self.client.xgroup_create(name=topic, groupname=group, id="$", mkstream=True)
            logger.info(f"Created Redis stream consumer group '{group}' on stream '{topic}'")
        except redis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                pass  # Group already exists
            else:
                logger.error(f"Unexpected error creating Redis consumer group: {e}")

    async def consume(
        self,
        topic: str,
        group: str,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        consumer_id: Optional[str] = "consumer_1"
    ) -> None:
        if not self.client:
            await self.connect()
        await self._ensure_group(topic, group)
        self._running = True
        logger.info(f"RedisStreamConsumer '{consumer_id}' reading from group '{group}' on stream '{topic}'")

        while self._running:
            try:
                # Read new messages for this consumer group
                response = await self.client.xreadgroup(
                    groupname=group,
                    consumername=consumer_id,
                    streams={topic: ">"},
                    count=50,
                    block=1000
                )
                if not response:
                    continue

                for stream_name, messages in response:
                    for msg_id, data in messages:
                        try:
                            raw_payload = data.get("data", "{}")
                            event = json.loads(raw_payload)
                            await callback(event)
                            await self.client.xack(stream_name, group, msg_id)
                        except Exception as item_err:
                            logger.error(f"Error handling message {msg_id}: {item_err}", exc_info=True)
            except asyncio.CancelledError:
                break
            except Exception as e:
                if self._running:
                    logger.error(f"RedisStreamConsumer read loop error: {e}")
                    await asyncio.sleep(1.0)

    async def stop(self) -> None:
        self._running = False

    async def close(self) -> None:
        self._running = False
        if self.client:
            await self.client.aclose()
