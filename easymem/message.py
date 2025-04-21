"""Basic memory message class."""

from pydantic import BaseModel, ConfigDict, Field


class BasicMemMessage(BaseModel):
    """Basic memory message class."""

    model_config = ConfigDict(extra="ignore")

    content: str = Field(
        ...,
        description="The content of the message.",
    )
