"""Base class for memory messages."""

import json
from abc import ABC
from typing import Any, TypeVar, get_type_hints

from pydantic import BaseModel, ConfigDict, Field, create_model, model_validator

from easymem.base.massivesearch import MassiveSearchSpecBase


class MemMessageBase(BaseModel, ABC):
    """Base class for memory messages."""

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def check_fields(cls, data: Any) -> Any:  # noqa: ANN401
        """Check the fields of the model."""
        cls.massive_searches()
        return data

    @classmethod
    def build_prompt(cls) -> str:
        """Build the prompt."""
        return json.dumps(cls.model_json_schema())

    @classmethod
    def massive_searches(cls) -> dict[str, type[MassiveSearchSpecBase]]:
        """Get the massive search specs."""
        searches: dict[str, type[MassiveSearchSpecBase]] = {}
        for field in cls.model_fields:
            metadata = get_type_hints(cls, include_extras=True)[field].__metadata__

            msearch_specs = [
                t
                for t in metadata
                if isinstance(t, type) and issubclass(t, MassiveSearchSpecBase)
            ]

            if len(msearch_specs) != 1:
                msg = (
                    f"{cls.__name__}.{field} must have exactly ONE "
                    "MassiveSearchSpecBase subclass in its Annotated metadata. "
                    "example: `field: Annotated[str, Field(...), SomeMassiveSearch]`"
                )
                raise TypeError(msg)

            msearch_spec = msearch_specs[0]
            searches[field] = msearch_spec

        return searches

    @classmethod
    def build_msearch_format_model(cls) -> type[BaseModel]:
        """Build the massive search format model."""
        format_model_fields: dict[str, Any] = {"sub_query": (str, ...)}
        searches = cls.massive_searches()
        for field, msearch_type in searches.items():
            format_model_fields[field] = (
                msearch_type.build_format_model(),
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
