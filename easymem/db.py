"""Database class for EasyMem."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from easymem.message import BasicMemMessage


@dataclass
class MemoryDB(ABC):
    """Database class for EasyMem."""

    collection_name: str = "easymem"
    limit: int = 10

    @abstractmethod
    def connect(self) -> None:
        """Connect to the database."""

    @abstractmethod
    def add(self, mid: str, message: BasicMemMessage) -> None:
        """Add a message to the database."""

    @abstractmethod
    def query(self, query: str) -> list[dict]:
        """Query the database."""
