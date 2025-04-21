"""Basic memory message class."""

from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

MemMessageT = TypeVar("MemMessageT", bound="BasicMemMessage")


class BasicMemMessage(BaseModel):
    """Basic memory message class."""

    model_config = ConfigDict(extra="ignore")

    content: str = Field(
        ...,
        description="The content of the message.",
    )
