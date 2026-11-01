import asyncio
import json
import logging
from typing import Callable, Awaitable, Dict, Any, Optional
from app.streaming.base import BaseProducer, BaseConsumer

logger = logging.getLogger(__name__)

class KafkaProducerAdapter(BaseProducer):
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    async def connect(self) -> None:
        try:
            from aiokafka import AIOKafkaProducer
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            await self._producer.start()
            logger.info(f"Connected KafkaProducer to {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka producer at {self.bootstrap_servers}: {e}")
            raise

    async def send_event(self, topic: str, event: Dict[str, Any]) -> bool:
        if not self._producer:
            await self.connect()
        try:
            await self._producer.send_and_wait(topic, event)
            return True
        except Exception as e:
            logger.error(f"Kafka produce error on {topic}: {e}")
            return False

    async def close(self) -> None:
        if self._producer:
            await self._producer.stop()
            logger.info("KafkaProducer stopped.")

class KafkaConsumerAdapter(BaseConsumer):
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._consumer = None
        self._running = False

    async def connect(self) -> None:
        pass

    async def consume(
        self,
        topic: str,
        group: str,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        consumer_id: Optional[str] = None
    ) -> None:
        from aiokafka import AIOKafkaConsumer
        self._running = True
        self._consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group,
            auto_offset_reset="latest",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True
        )
        await self._consumer.start()
        logger.info(f"Kafka consumer started on topic '{topic}' group '{group}'")
        try:
            while self._running:
                data = await self._consumer.getmany(timeout_ms=1000, max_records=50)
                for tp, messages in data.items():
                    for msg in messages:
                        try:
                            await callback(msg.value)
                        except Exception as cb_err:
                            logger.error(f"Error in Kafka consumer callback: {cb_err}", exc_info=True)
        except asyncio.CancelledError:
            pass
        finally:
            await self._consumer.stop()

    async def stop(self) -> None:
        self._running = False

    async def close(self) -> None:
        self._running = False
        if self._consumer:
            await self._consumer.stop()
