"""Vector Massive Search."""

from pydantic import Field

from easymem.massivesearch.base import MassiveSearchSpecBase


class VectorMassiveSearchSpecBase(MassiveSearchSpecBase):
    """Vector massive search spec."""

    query: str = Field(
        ...,
        description=(
            "Query string for vector search, typically a natural language "
            "question or a search term."
        ),
        examples=[
            "What is the capital of France?",
            "Tell me about Python programming.",
        ],
    )
