"""Basic EasyMem module."""

import uuid
from dataclasses import asdict, fields
from typing import Any

import numpy as np

from easymem.base.easymem import EasyMemBase
from easymem.base.model import MassiveSearchQueryT, ModelBase
from easymem.basic.massivesearch import BasicMassiveSearchProtocol
from easymem.basic.message import BasicMemMessage
from easymem.basic.model import AzureOpenAIClient


class BasicEasyMem(EasyMemBase):
    """Basic EasyMem class."""

    def __init__(
        self,
        message_type: type = BasicMemMessage,
        model: ModelBase | None = None,
    ) -> None:
        """Initialize the BasicEasyMem."""
        super().__init__(message_type, BasicMassiveSearchProtocol)
        self.model = model or AzureOpenAIClient()
        self.columns = {f.name: i for i, f in enumerate(fields(self.message_type), 1)}
        self.memory: list[tuple] = []

    @EasyMemBase.valid_message
    async def add(self, message: Any) -> None:  # noqa: ANN401
        """Add a message to the database."""
        message_id = str(uuid.uuid4())
        self.memory.append((message_id, *asdict(message).values()))

    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[Any], MassiveSearchQueryT]:
        """Massive search in the database."""
        massive_search_query = await self.model.response(
            query,
            self.index_context,
            self.format_model,
        )
        partial_results = []
        for single_query in massive_search_query:
            single_query_result = []
            for key, search_args in single_query.items():
                if key == "sub_query":
                    continue

                single_query_result.append(
                    await self.massive_search_types[key](**search_args).search_task(
                        col=self.columns[key],
                        data=self.memory,
                    ),
                )
            if single_query_result:
                common_rows = single_query_result[0]
                for arr in single_query_result[1:]:
                    common_rows = common_rows[np.isin(common_rows[:, 0], arr[:, 0])]
                if common_rows.size:
                    partial_results.append(common_rows)

        merged = (
            np.vstack(partial_results)
            if partial_results
            else np.empty((0, len(self.columns) + 1), dtype=object)
        )

        _, unique_idx = np.unique(merged[:, 0], return_index=True)
        merged = merged[unique_idx]

        return (
            [
                self.message_type(
                    **dict(zip(self.columns, row[1:], strict=False)),
                )
                for row in merged
            ],
            massive_search_query,
        )
