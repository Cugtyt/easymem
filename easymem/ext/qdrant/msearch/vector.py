"""Qdrant vector massive search module for EasyMem."""

from dataclasses import dataclass
from typing import Annotated

from qdrant_client.models import Condition, Filter

from easymem.base.massivesearch import MassiveSearchField
from easymem.ext.qdrant.massivesearch import QdrantMassiveSearchProtocol


@dataclass(slots=True)
class QdrantVectorMassiveSearch(QdrantMassiveSearchProtocol):
    """Qdrant vector massive search module for EasyMem."""

    query: Annotated[
        str,
        MassiveSearchField(
            description=(
                "Query for the vector search. "
                "This should be a string in natural language."
                "The query is used to filter the results."
            ),
            examples=[],
        ),
    ]

    score_threshold: Annotated[
        float,
        MassiveSearchField(
            description=(
                "Score threshold for the vector search. "
                "Only results with a score above this threshold will be returned."
                "It should be a float value between 0 and 1, 0.9 is a good "
                "default value for most use cases."
            ),
            examples=[
                0.9,
            ],
        ),
    ]

    async def search_task(self, key: str) -> Condition:
        """Ignored because Qdrant directly supports vector search."""
        _ = key
        return Filter()
