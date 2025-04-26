"""Qdrant vector massive search module for EasyMem."""

from dataclasses import dataclass
from typing import Annotated

from pydantic import Field
from qdrant_client.models import Condition, Filter

from easymem.ext.qdrant.massivesearch import QdrantMassiveSearchProtocol


@dataclass(slots=True)
class QdrantVectorMassiveSearch(QdrantMassiveSearchProtocol):
    """Qdrant vector massive search module for EasyMem."""

    query: Annotated[
        str,
        Field(
            ...,
            description=(
                "Query for the vector search. "
                "This should be a string in natural language."
                "The query is used to filter the results."
            ),
        ),
    ]

    score_threshold: Annotated[
        float,
        Field(
            ...,
            description=(
                "Score threshold for the vector search. "
                "Only results with a score above this threshold will be returned."
                "It should be a float value between 0 and 1, 0.9 is a good "
                "default value for most use cases."
            ),
        ),
    ]

    async def search_task(self, key: str) -> Condition:
        """Ignored because Qdrant directly supports vector search."""
        _ = key
        return Filter()
