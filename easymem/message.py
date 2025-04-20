"""Basic memory message class."""

from dataclasses import dataclass, field


@dataclass
class BasicMemMessage:
    """Basic memory message class."""

    content: str = field(metadata={"description": "The content of memory."})
