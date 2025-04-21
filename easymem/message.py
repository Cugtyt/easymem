"""Basic memory message class."""

from typing import Annotated, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from easymem.massivesearch.vector import VectorMassiveSearchSpecBase

MemMessageT = TypeVar("MemMessageT", bound="BasicMemMessage")


class BasicMemMessage(BaseModel):
    """Basic memory message class."""

    model_config = ConfigDict(extra="ignore")

    content: Annotated[
        str,
        Field(
            ...,
            description="The content of the message.",
        ),
        VectorMassiveSearchSpecBase,
    ]
