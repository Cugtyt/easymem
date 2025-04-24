"""Basic EasyMem module."""

import uuid

import numpy as np

from easymem.base.easymem import EasyMemBase
from easymem.basic.message import BasicMemMessage
from easymem.basic.model import AzureOpenAIClient
from easymem.basic.record import BasicMemResult


class BasicEasyMem(EasyMemBase[BasicMemMessage, BasicMemResult]):
    """Basic EasyMem class."""

    async def connect(self) -> None:
        """Connect to the database."""
        await super().connect()
        self.model = AzureOpenAIClient()
        self.memory: np.ndarray = np.empty((0, 3), dtype=object)

    async def add(self, message: BasicMemMessage) -> None:
        """Add a message to the database."""
        message_id = str(uuid.uuid4())
        self.memory = np.append(
            self.memory,
            np.array([[message_id, message.content, message.date]], dtype=object),
            axis=0,
        )

    async def massivequery(self, query: str) -> list[BasicMemResult]:
        """Massive search in the database."""
        massive_search_response = await self.model.response(
            query,
            self.index_context,
            self.format_model,
        )
        partial_results = []
        for key, search_args in massive_search_response.items():
            partial_results.append(
                await self.massive_searches[key].search_task(**search_args),
            )

        merged = (
            np.vstack(partial_results)
            if partial_results
            else np.empty((0, 3), dtype=object)
        )

        _, unique_idx = np.unique(merged[:, 0], return_index=True)
        merged = merged[unique_idx]

        return []
