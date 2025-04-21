"""Memory record classes."""

from pydantic import BaseModel, ConfigDict

from easymem.message import BasicMemMessage


class BasicMemoryRecord(BaseModel):
    """Memory records."""

    model_config = ConfigDict(extra="ignore")

    id: str | int
    message: BasicMemMessage
    score: float
