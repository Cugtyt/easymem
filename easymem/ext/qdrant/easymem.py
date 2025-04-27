"""Qdrant EasyMem."""

from dataclasses import asdict
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter

from easymem.base import EasyMemBase, MassiveSearchQueryT, ModelBase
from easymem.basic.model import AzureOpenAIClient
from easymem.ext.qdrant.massivesearch import QdrantMassiveSearchProtocol
from easymem.ext.qdrant.message import QdrantMemMessage


class QdrantEasyMem(EasyMemBase):
    """Qdrant EasyMem class."""

    def __init__(
        self,
        message_type: type = QdrantMemMessage,
        qdrant_client_args: dict | None = None,
        collection_name: str = "easymem",
        model: ModelBase | None = None,
    ) -> None:
        """Initialize the QdrantEasyMem."""
        super().__init__(message_type, QdrantMassiveSearchProtocol)
        if not hasattr(message_type, "content"):
            msg = f"{message_type.__name__} must have a 'content' field."
            raise TypeError(msg)
        self.client = AsyncQdrantClient(
            **(qdrant_client_args or {"location": ":memory:"}),
        )
        self.collection_name = collection_name
        self.model = model or AzureOpenAIClient()

    @EasyMemBase.valid_message
    async def add(self, message: Any) -> None:  # noqa: ANN401
        """Add a message."""
        metadata = {k: v for k, v in asdict(message).items() if k != "content"}
        await self.client.add(
            collection_name=self.collection_name,
            documents=[message.content],
            metadata=[metadata],
        )

    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[Any], MassiveSearchQueryT]:
        """Massive search."""
        massive_search_query = await self.model.response(
            query,
            self.index_context,
            self.format_model,
        )
        results = []
        for single_query in massive_search_query:
            filters = []
            for key, search_args in single_query.items():
                if key in {"content", "sub_query"}:
                    continue
                cur_filter = await self.massive_search_types[key](
                    **search_args,
                ).search_task(
                    key,
                )
                filters.append(cur_filter)
            cur_result = await self.client.query(
                collection_name=self.collection_name,
                query_text=single_query["content"]["query"],
                query_filter=Filter(
                    must=filters,
                ),
                score_threshold=single_query["content"]["score_threshold"],
            )

            for r in cur_result:
                metadata = {
                    k: v for k, v in r.metadata.items() if k in self.message_fields
                }
                results.append(
                    self.message_type(
                        content=r.document,  # type: ignore  # noqa: PGH003
                        **metadata,
                    ),
                )
        return results, massive_search_query
