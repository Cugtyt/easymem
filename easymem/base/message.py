"""EasyMem message."""

import json
from dataclasses import asdict, dataclass, fields, is_dataclass
from typing import Any, get_type_hints

from pydantic import BaseModel, Field, create_model


class MessageHelper:
    """EasyMem message helper class."""

    def __init__(
        self,
        message_type: type,
        protocol: type,
    ) -> None:
        """Initialize the EasyMem message helper."""
        self.ensure_types(message_type, protocol)
        self.parse_message()
        self.build_msearch_format_model()

    def ensure_types(self, message_type: type, protocol: type) -> None:
        """Ensure the types of message and massive search protocol."""
        if not is_dataclass(message_type) or not hasattr(
            message_type,
            "__slots__",
        ):
            msg = (
                f"{message_type} must be a dataclass with __slots__ attribute. "
                "Usage: `@dataclass(slots=True)`"
            )
            raise TypeError(msg)

        type_hints = get_type_hints(message_type, include_extras=True)
        for field in fields(message_type):
            field_metadata = type_hints[field.name].__metadata__
            if not field_metadata:
                msg = (
                    f"{message_type.__name__}.{field.name} must have "
                    "Annotated metadata."
                )
                raise TypeError(msg)

            message_fields = [t for t in field_metadata if isinstance(t, MessageField)]

            if len(message_fields) != 1:
                msg = (
                    f"{message_type.__name__}.{field.name} must have exactly ONE "
                    "MessageField in its Annotated metadata. "
                    "example: `field: Annotated[str, MessageField(...)]`"
                )
                raise TypeError(msg)

            if not isinstance(message_fields[0].msearch, type) or not is_dataclass(
                message_fields[0].msearch,
            ):
                msg = f"{message_fields[0].msearch} must be a dataclass type."
                raise TypeError(msg)

            if not issubclass(message_fields[0].msearch, protocol):
                msg = (
                    f"{message_type.__name__}.{field.name} must have a "
                    f"{protocol.__name__} subclass in its Annotated metadata. "
                )
                raise TypeError(msg)

        self.message_type = message_type
        self.protocol = protocol
        self.message_fields = [field.name for field in fields(message_type)]

    def parse_message(self) -> None:
        """Parse the message metadata."""
        self.massive_search_types: dict[str, type] = {}
        index_context: dict[str, dict] = {}
        type_hints = get_type_hints(self.message_type, include_extras=True)
        for field in fields(self.message_type):
            metadata = type_hints[field.name].__metadata__
            message_fields = [t for t in metadata if isinstance(t, MessageField)]
            self.massive_search_types[field.name] = message_fields[0].msearch
            index_context[field.name] = message_fields[0].to_dict()
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
    """Message field."""

    description: str
    examples: list[str]
    msearch: type

    def __post_init__(self) -> None:
        """Initialize the message field."""
        type_hints = get_type_hints(self.msearch, include_extras=True)
        for msearch_field in fields(self.msearch):
            metadata = type_hints[msearch_field.name].__metadata__
            if not metadata:
                msg = (
                    f"{self.msearch.__name__}.{msearch_field.name} must have "
                    "Annotated metadata. "
                )
                raise TypeError(msg)
            massive_search_fields = [
                t for t in metadata if isinstance(t, MassiveSearchField)
            ]
            if len(massive_search_fields) != 1:
                msg = (
                    f"{self.msearch.__name__}.{msearch_field.name} must have exactly "
                    "ONE MassiveSearchField in its Annotated metadata. "
                    "example: `field: Annotated[str, MassiveSearchField(...)]`"
                )
                raise TypeError(msg)

    def to_dict(self) -> dict[str, Any]:
        """Convert the message field to a dictionary."""
        result = {}
        for k, v in asdict(self).items():
            if k != "msearch":
                result[k] = v
            else:
                result[k] = self.massive_search_dict(v)
        return result

    @staticmethod
    def massive_search_dict(massive_search: type) -> dict[str, Any]:
        """Convert the massive search to a dictionary."""
        type_hints = get_type_hints(massive_search, include_extras=True)
        result = {}
        for field in fields(massive_search):
            metadata = type_hints[field.name].__metadata__
            massive_search_fields = [
                t for t in metadata if isinstance(t, MassiveSearchField)
            ]
            result[field.name] = asdict(
                massive_search_fields[0],
            )
        return result


@dataclass
class MassiveSearchField:
    """Massive search field."""

    description: str
    examples: list
