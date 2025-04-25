"""Database class for EasyMem."""

from abc import abstractmethod
from dataclasses import fields
from typing import Generic

from easymem.base.massivesearch import MassiveSearchQueryT
from easymem.base.message import MemMessageT


class EasyMemBase(Generic[MemMessageT]):
    """Database class for EasyMem."""

    def __init__(self, message_type: type[MemMessageT]) -> None:
        """Initialize the EasyMem."""
        self.message_type = message_type
        self.message_fileds = {f.name for f in fields(message_type)}
        self.format_model = self.message_type.build_msearch_format_model()
        self.index_context = self.message_type.build_prompt()
        self.massive_search_types = self.message_type.massive_searches()

    @abstractmethod
    async def add(self, message: MemMessageT) -> None:
        """Add a message to the database."""

    @abstractmethod
    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[MemMessageT], MassiveSearchQueryT]:
        """Massive search in the database."""
