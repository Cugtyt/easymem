"""Qdrant EasyMem message."""

from dataclasses import dataclass
from typing import Annotated, TypeVar

from easymem.base.message import MessageField
from easymem.ext.qdrant.msearch.date import QdrantDatetimeMassiveSearch
from easymem.ext.qdrant.msearch.vector import QdrantVectorMassiveSearch


@dataclass(slots=True)
class QdrantMemMessage:
    """Qdrant memory message class."""

    content: Annotated[
        str,
        MessageField(
            description="The content of the message.",
            examples=[
                "I love programming in Python!",
                "The weather is great today.",
            ],
            msearch=QdrantVectorMassiveSearch,
        ),
    ]
    datetime: Annotated[
        str,
        MessageField(
            description=(
                "The datetime of the message, the datetime starts from "
                "2000-01-01T00:00:00Z, current datetime is 2025-05-01T00:00:00Z."
            ),
            examples=[
                "2023-10-01T12:00:00Z",
                "2023-10-02T15:30:00Z",
            ],
            msearch=QdrantDatetimeMassiveSearch,
        ),
    ]


QdrantMemMessageT = TypeVar("QdrantMemMessageT", bound=QdrantMemMessage)
