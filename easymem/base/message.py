"""Base class for memory messages."""

import json
from abc import ABC, abstractmethod
from typing import Any, TypeVar, get_type_hints

from pydantic import BaseModel, ConfigDict, model_validator

from easymem.base.massivesearch import MassiveSearchSpecBase


class MemMessageBase(BaseModel, ABC):
    """Base class for memory messages."""

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def check_fields(cls, data: Any) -> Any:  # noqa: ANN401
        """Check the fields of the model."""
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
        return data

    def build_prompt(self) -> str:
        """Build the prompt."""
        return json.dumps(self.model_json_schema())

    @abstractmethod
    def build_msearch_format_model(self) -> type[BaseModel]:
        """Build the massive search format model."""


MemMessageT = TypeVar("MemMessageT", bound=MemMessageBase)
