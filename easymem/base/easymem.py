"""Database class for EasyMem."""

from abc import abstractmethod
from typing import Generic, get_args

from easymem.base.message import MemMessageT
from easymem.base.record import MemQueryResultRecordT


class EasyMemBase(Generic[MemMessageT, MemQueryResultRecordT]):
    """Database class for EasyMem."""

    async def connect(self) -> None:
        """Connect to the database."""
        if not hasattr(self, "__orig_bases__"):
            msg = (
                "Unable to determine MemMessageT; make sure the subclass "
                "is parametrised, e.g.  EasyMemBase[MyMemMessage, …]"
            )
            raise RuntimeError(msg)
        message_class: type[MemMessageT] = get_args(
            self.__orig_bases__[0],  # type: ignore  # noqa: PGH003
        )[0]

        self.format_model = message_class.build_msearch_format_model()
        self.index_context = message_class.build_prompt()
        self.massive_searches = message_class.massive_searches()

    @abstractmethod
    async def add(self, message: MemMessageT) -> None:
        """Add a message to the database."""

    @abstractmethod
    async def massivequery(self, query: str) -> list[MemQueryResultRecordT]:
        """Massive search in the database."""
