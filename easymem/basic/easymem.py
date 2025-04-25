"""Basic EasyMem module."""

import uuid
from dataclasses import asdict, fields

import numpy as np

from easymem.base.easymem import EasyMemBase
from easymem.base.massivesearch import MassiveSearchQueryT
from easymem.base.model import ModelBase
from easymem.basic.message import BasicMemMessage, BasicMemMessageT
from easymem.basic.model import AzureOpenAIClient


class BasicEasyMem(EasyMemBase[BasicMemMessageT]):
    """Basic EasyMem class."""

    def __init__(
        self,
        message_type: type[BasicMemMessageT],
        model: ModelBase | None = None,
    ) -> None:
        """Initialize the BasicEasyMem."""
        if not issubclass(message_type, BasicMemMessage):
            msg = (
                "message_type must be a subclass of BasicMemMessage, "
                f"not {type(message_type)}"
            )
            raise TypeError(
                msg,
            )
        super().__init__(message_type)
        self.model = model or AzureOpenAIClient()
        self.columns = {f.name: i for i, f in enumerate(fields(self.message_type), 1)}
        self.memory: np.ndarray = np.empty((0, len(self.columns) + 1), dtype=object)

    async def add(self, message: BasicMemMessageT) -> None:
        """Add a message to the database."""
        message_id = str(uuid.uuid4())
        message_content = list(asdict(message).values())
        self.memory = np.append(
            self.memory,
            np.array([[message_id, *message_content]], dtype=object),
            axis=0,
        )

    async def massivequery(
        self,
        query: str,
    ) -> tuple[list[BasicMemMessageT], MassiveSearchQueryT]:
        """Massive search in the database."""
        massive_search_response = await self.model.response(
            query,
            self.index_context,
            self.format_model,
        )
        massive_search_query = massive_search_response["queries"]
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
            else np.empty((0, 3), dtype=object)
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
