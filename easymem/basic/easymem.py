"""Basic EasyMem module."""

import uuid
from dataclasses import asdict, fields
from typing import Any

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
        merged = set()
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
                common_result = set(single_query_result[0])
                for i in range(1, len(single_query_result)):
                    common_result = common_result.intersection(
                        single_query_result[i],
                    )

                merged.update(common_result)

        return (
            [
                self.message_type(
                    **dict(zip(self.columns, row[1:], strict=False)),
                )
                for row in merged
            ],
            massive_search_query,
        )
