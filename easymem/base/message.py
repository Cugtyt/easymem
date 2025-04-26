"""Base class for memory messages."""

import json
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, get_type_hints

from pydantic import BaseModel, Field, create_model

from easymem.base.massivesearch import MassiveSearchProtocol


class MessageHelper:
    """EasyMem message helper class."""

    def __init__(
        self,
        message_type: type,
        protocol: type[MassiveSearchProtocol],
    ) -> None:
        """Initialize the EasyMem message helper."""
        self.message_type = message_type
        self.protocol = protocol
        self.type_check()
        self.message_fields = {f.name for f in fields(message_type)}
        self.parse_message_metadata()
        self.build_msearch_format_model()

    def type_check(self) -> None:
        """Check if the message type is a dataclass with __slots__."""
        if not is_dataclass(self.message_type) or not hasattr(
            self.message_type,
            "__slots__",
        ):
            msg = (
                f"{self.message_type} must be a dataclass with __slots__ attribute. "
                "Usage: `@dataclass(slots=True)`"
            )
            raise TypeError(msg)

    def parse_message_metadata(self) -> None:
        """Parse the message metadata."""
        self.massive_search_types: dict[str, type[MassiveSearchProtocol]] = {}
        index_context: dict[str, dict] = {}
        for field_name in self.message_fields:
            metadata = get_type_hints(self.message_type, include_extras=True)[
                field_name
            ].__metadata__
            if not metadata:
                msg = (
                    f"{self.message_type.__name__}.{field_name} must have "
                    "Annotated metadata. "
                )
                raise TypeError(msg)
            message_fields = [t for t in metadata if isinstance(t, MessageField)]
            if len(message_fields) != 1:
                msg = (
                    f"{self.message_type.__name__}.{field_name} must have exactly ONE "
                    "MessageField in its Annotated metadata. "
                    "example: `field: Annotated[str, MessageField(...)]`"
                )
                raise TypeError(msg)

            if not issubclass(message_fields[0].msearch, self.protocol):
                msg = (
                    f"{self.message_type.__name__}.{field_name} must have a "
                    f"{self.protocol.__name__} subclass in its Annotated metadata. "
                )
                raise TypeError(msg)

            self.massive_search_types[field_name] = message_fields[0].msearch
            index_context[field_name] = asdict(
                message_fields[0],
                dict_factory=MessageField.dict_factory,
            )
        self.index_context = json.dumps(index_context)

    def build_msearch_format_model(self) -> None:
        """Build the massive search format model."""
        format_model_fields: dict[str, Any] = {"sub_query": (str, ...)}
        searches = self.massive_search_types
        for field_name, msearch_type in searches.items():
            format_model_fields[field_name] = (
                msearch_type,
                ...,
            )

        single_query_format: type[BaseModel] = create_model(
            "SingleQueryFormat",
            **format_model_fields,
            __base__=BaseModel,
        )

        self.format_model = create_model(
            "MultiQueryFormat",
            queries=(list[single_query_format], Field(...)),  # type: ignore[valid-type]
            __base__=BaseModel,
        )


@dataclass
class MessageField:
    """Message field model."""

    description: str
    examples: list[str]
    msearch: type

    @staticmethod
    def dict_factory(f: list[tuple]) -> dict[str, Any]:
        """Create a dictionary from the field."""
        exclude_fields = {"msearch"}
        return {k: v for (k, v) in f if k not in exclude_fields and v is not None}
