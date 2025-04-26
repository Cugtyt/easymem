"""EasyMem base class."""

from abc import abstractmethod
from typing import Generic, TypeVar

from easymem.base.massivesearch import MassiveSearchProtocol
from easymem.base.message import MessageHelper
from easymem.base.model import MassiveSearchQueryT

MemMessageT = TypeVar("MemMessageT")


class EasyMemBase(Generic[MemMessageT]):
    """Database class for EasyMem."""

    def __init__(
        self,
        message_type: type[MemMessageT],
        massive_search_protocol: type[MassiveSearchProtocol],
    ) -> None:
        """Initialize the EasyMem."""
        message_helper = MessageHelper(message_type, massive_search_protocol)
        self.massive_search_protocol = massive_search_protocol
        self.message_type = message_helper.message_type
        self.message_fields = message_helper.message_fields
        self.massive_search_types = message_helper.massive_search_types
        self.format_model = message_helper.format_model
        self.index_context = message_helper.index_context

    @abstractmethod
    async def add(self, message: MemMessageT) -> None:
        """Add a message to the database."""

    @abstractmethod
    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[MemMessageT], MassiveSearchQueryT]:
        """Massive search in the database."""
