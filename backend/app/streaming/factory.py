import logging
from app.core.config import settings
from app.streaming.base import BaseProducer, BaseConsumer
from app.streaming.memory_stream import MemoryProducer, MemoryConsumer

logger = logging.getLogger(__name__)

# Singletons for producers
_producer_instance: BaseProducer = None

def get_stream_producer() -> BaseProducer:
    global _producer_instance
    if _producer_instance is not None:
        return _producer_instance

    backend_type = settings.STREAM_BACKEND.lower()
    if backend_type == "redis":
        from app.streaming.redis_stream import RedisStreamProducer
        _producer_instance = RedisStreamProducer(redis_url=settings.REDIS_URL)
    elif backend_type == "kafka":
        from app.streaming.kafka_stream import KafkaProducerAdapter
        _producer_instance = KafkaProducerAdapter(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    else:
        _producer_instance = MemoryProducer()
        
    logger.info(f"Initialized stream producer with backend: {backend_type}")
    return _producer_instance

def get_stream_consumer() -> BaseConsumer:
    backend_type = settings.STREAM_BACKEND.lower()
    if backend_type == "redis":
        from app.streaming.redis_stream import RedisStreamConsumer
        return RedisStreamConsumer(redis_url=settings.REDIS_URL)
    elif backend_type == "kafka":
        from app.streaming.kafka_stream import KafkaConsumerAdapter
        return KafkaConsumerAdapter(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    else:
        return MemoryConsumer()
