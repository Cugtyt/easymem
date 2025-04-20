"""Memory record classes."""

from dataclasses import dataclass

from easymem.message import BasicMemMessage


@dataclass
class MemoryRecord:
    """Memory records."""

    id: str
    message: BasicMemMessage
    score: float
