"""Model base."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

DEFAULT_SYSTEM_PROMPT = """Fill the search engine query arguments
based on the user's intent and current index information.

You will break down the user's intent into one or multiple queries,
each query has a sub_query and a structure of arguments for the search engine.
The sub_query is a string that represents the user's intent,
the arguments will be passed to the search engine.
These queries will be executed in parallel and aggregated.
Every query in the array represents an independent search path.

The relationship between different queries in the array is OR -
results matching ANY of the queries will be included in the final results.

Within each individual query, parameters have an AND relationship -
all conditions within a single query must be satisfied simultaneously.

IMPORTANT: If a user's intent involves a condition that could apply to multiple fields
(e.g., a keyword appearing in 'title' OR 'description'),
you MUST create separate queries for each field possibility,
combined with other constraints.

For example, for "find books about 'dogs' under $15",
if 'dogs' can be in 'title' or 'description', generate:
- Query 1: (title contains 'dogs' AND price <= 15)
- Query 2: (description contains 'dogs' AND price <= 15)
Do NOT generate a single query like
(title contains 'dogs' AND description contains 'dogs' AND price <= 15)
unless the user explicitly asks for the term in both fields.

Another example, with a query array of 5 elements, where each element contains
3 parameters:
- Query 1: (param1 AND param2 AND param3)
- Query 2: (param1 AND param2 AND param3)
- Query 3: (param1 AND param2 AND param3)
- Query 4: (param1 AND param2 AND param3)
- Query 5: (param1 AND param2 AND param3)

The final search logic is:
(Query 1) OR (Query 2) OR (Query 3) OR (Query 4) OR (Query 5)

This structure allows you to create complex search patterns that capture
different aspects of the user's intent while maintaining logical clarity.

The following is the index information, msearch for each index has the search
arguments description:

{index_context}
"""


MassiveSearchQueryT = list[dict[str, Any]]


class ModelResponseError(Exception):
    """Model Response Error."""


class ModelBase(ABC):
    """Base class for all model clients."""

    def __init__(self, system_prompt: str | None = None) -> None:
        """Initialize the model with a system prompt."""
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    def build_messages(self, query: str, index_content: str) -> list[dict]:
        """Build the messages for the Azure OpenAI service."""
        return [
            {
                "role": "system",
                "content": self.system_prompt.format(index_context=index_content),
            },
            {
                "role": "user",
                "content": query,
            },
        ]

    @abstractmethod
    async def response(
        self,
        query: str,
        index_content: str,
        format_model: type[BaseModel],
    ) -> MassiveSearchQueryT:
        """Get a response from the model."""
