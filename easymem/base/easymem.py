"""EasyMem base class."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import is_dataclass
from functools import wraps
from typing import Any

from easymem.base.message import MessageHelper
from easymem.base.model import MassiveSearchQueryT


class EasyMemBase(ABC):
    """EasyMem base."""

    def __init__(
        self,
        message_type: type,
        massive_search_protocol: type,
    ) -> None:
        """Initialize the EasyMem."""
        message_helper = MessageHelper(message_type, massive_search_protocol)
        self.message_type = message_helper.message_type
        self.massive_search_protocol = message_helper.protocol
        self.message_fields = message_helper.message_fields
        self.massive_search_types = message_helper.massive_search_types
        self.format_model = message_helper.format_model
        self.index_context = message_helper.index_context

    @staticmethod
    def valid_message(func: Callable) -> Callable:
        """Validate message."""

        @wraps(func)
        async def warpper(
            self: "EasyMemBase",
            message: Any,  # noqa: ANN401
        ) -> None:
            if not is_dataclass(message):
                msg = "message must be a dataclass."
                raise TypeError(msg)
            if type(message) is not self.message_type:
                msg = (
                    f"message must be an instance of {self.message_type}, "
                    f"not {type(message)}."
                )
                raise TypeError(msg)
            return await func(self, message)

        return warpper

    @abstractmethod
    async def add(self, message: Any) -> None:  # noqa: ANN401
        """Add a message to the EasyMem."""

    @abstractmethod
    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[Any], MassiveSearchQueryT]:
        """Massive search in the EasyMem."""
