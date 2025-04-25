"""Base class for memory messages."""

import json
from dataclasses import dataclass, fields
from typing import Any, TypeVar, get_type_hints

from pydantic import BaseModel, Field, create_model

from easymem.base.massivesearch import MassiveSearchSpecBase


@dataclass(slots=True)
class MemMessageBase:
    """Base class for memory messages."""

    def __post_init__(self) -> None:
        """Post-initialization method to set up the message."""
        self.massive_searches()

    @classmethod
    def build_prompt(cls) -> str:
        """Return a tiny JSON description of the dataclass fields."""
        schema = {f.name: str(f.type) for f in fields(cls)}
        return json.dumps(schema)

    @classmethod
    def massive_searches(cls) -> dict[str, type[MassiveSearchSpecBase]]:
        """Extract MassiveSearchSpecBase annotations from type hints."""
        searches: dict[str, type[MassiveSearchSpecBase]] = {}
        for field_name in get_type_hints(cls):
            metadata = get_type_hints(cls, include_extras=True)[field_name].__metadata__
            msearch_specs = [
                t
                for t in metadata
                if isinstance(t, type) and issubclass(t, MassiveSearchSpecBase)
            ]
            if len(msearch_specs) != 1:
                msg = (
                    f"{cls.__name__}.{field_name} must have exactly ONE "
                    "MassiveSearchSpecBase subclass in its Annotated metadata. "
                    "example: `field: Annotated[str, SomeMassiveSearch]`"
                )
                raise TypeError(msg)
            searches[field_name] = msearch_specs[0]
        return searches

    @classmethod
    def build_msearch_format_model(cls) -> type[BaseModel]:
        """Build the massive search format model."""
        format_model_fields: dict[str, Any] = {"sub_query": (str, ...)}
        searches = cls.massive_searches()
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

        return create_model(
            "MultiQueryFormat",
            queries=(list[single_query_format], Field(...)),  # type: ignore[valid-type]
            __base__=BaseModel,
        )


MemMessageT = TypeVar("MemMessageT", bound=MemMessageBase)
