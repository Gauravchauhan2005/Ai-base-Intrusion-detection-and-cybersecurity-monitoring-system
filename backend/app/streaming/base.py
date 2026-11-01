from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Dict, Any, Optional

class BaseProducer(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Connect to streaming broker."""
        pass

    @abstractmethod
    async def send_event(self, topic: str, event: Dict[str, Any]) -> bool:
        """Send an event dictionary to the designated topic/stream."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Disconnect and cleanup resources."""
        pass

class BaseConsumer(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Connect to streaming broker and ensure topic/group exists."""
        pass

    @abstractmethod
    async def consume(
        self,
        topic: str,
        group: str,
        callback: Callable[[Dict[str, Any]], Awaitable[None]],
        consumer_id: Optional[str] = None
    ) -> None:
        """Continuously consume events from the stream and invoke callback for each."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Signal consumer to stop reading."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Cleanup connection resources."""
        pass
