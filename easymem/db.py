"""Database class for EasyMem."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from easymem.message import BasicMemMessage
from easymem.records import BasicMemoryRecord


@dataclass
class MemoryDB(ABC):
    """Database class for EasyMem."""

    collection_name: str = "easymem"
    limit: int = 10

    message_type: type[BasicMemMessage] = BasicMemMessage
    record_type: type[BasicMemoryRecord] = BasicMemoryRecord

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the database."""

    @abstractmethod
    async def add(self, message: BasicMemMessage) -> None:
        """Add a message to the database."""

    @abstractmethod
    async def query(self, query: str) -> list[BasicMemoryRecord]:
        """Query the database."""

    @abstractmethod
    async def massive_search(self, query: dict) -> list[BasicMemoryRecord]:
        """Massive search in the database."""
