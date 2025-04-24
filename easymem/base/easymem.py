"""Database class for EasyMem."""

from abc import abstractmethod
from typing import Generic

from easymem.base.message import MemMessageT
from easymem.base.record import MemQueryResultRecordT


class EasyMemBase(Generic[MemMessageT, MemQueryResultRecordT]):
    """Database class for EasyMem."""

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the database."""

    @abstractmethod
    async def add(self, message: MemMessageT) -> None:
        """Add a message to the database."""

    @abstractmethod
    async def massivequery(self, query: str) -> list[MemQueryResultRecordT]:
        """Massive search in the database."""
