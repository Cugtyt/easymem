# ruff: noqa: INP001, T201, D103, ANN201, D100, D101

import json
from dataclasses import dataclass
from typing import Annotated

from easymem.base.message import MessageField
from easymem.basic.easymem import BasicEasyMem
from easymem.basic.message import BasicMemMessage
from easymem.basic.msearch.text import BasicTextMassiveSearch
from easymem.ext.qdrant.easymem import QdrantEasyMem
from easymem.ext.qdrant.message import QdrantMemMessage
from easymem.ext.qdrant.msearch.vector import QdrantVectorMassiveSearch


async def basic() -> None:
    mem = BasicEasyMem()
    await mem.add(BasicMemMessage(content="Hello", date="2020-10-01"))
    await mem.add(BasicMemMessage(content="World", date="2023-10-02"))
    await mem.add(BasicMemMessage(content="Python", date="2023-10-03"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello and Python before 2023-01-01")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)


@dataclass(slots=True)
class MyBasicMemMessage(BasicMemMessage):
    person: Annotated[
        str,
        MessageField(
            description="person name who is sending the message.",
            examples=[],
            msearch=BasicTextMassiveSearch,
        ),
    ] = "Bob"


async def basic_ext() -> None:
    mem = BasicEasyMem(MyBasicMemMessage)
    await mem.add(MyBasicMemMessage(content="Hello", date="2020-10-01"))
    await mem.add(MyBasicMemMessage(content="World", date="2023-10-02"))
    await mem.add(MyBasicMemMessage(content="Python", date="2023-10-03"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello or Python before 2023-01-01")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)


async def qdrant():
    mem = QdrantEasyMem()
    await mem.add(QdrantMemMessage(content="Hello", datetime="2020-10-01T00:00:00Z"))
    await mem.add(QdrantMemMessage(content="World", datetime="2023-10-02T00:00:00Z"))
    await mem.add(QdrantMemMessage(content="Python", datetime="2023-10-03T00:00:00Z"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello and Python before 2023-01-01")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)


@dataclass(slots=True)
class MyQdrantMemMessage(QdrantMemMessage):
    person: Annotated[
        str,
        MessageField(
            description="person name who is sending the message.",
            examples=[],
            msearch=QdrantVectorMassiveSearch,
        ),
    ] = "Bob"


async def qdrant_ext():
    mem = QdrantEasyMem(MyQdrantMemMessage)
    await mem.add(MyQdrantMemMessage(content="Hello", datetime="2020-10-01T00:00:00Z"))
    await mem.add(MyQdrantMemMessage(content="World", datetime="2023-10-02T00:00:00Z"))
    await mem.add(MyQdrantMemMessage(content="Python", datetime="2023-10-03T00:00:00Z"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello or Python before 2023-01-01")
    print("Query:", json.dumps(query))
    print("Result:")
    for item in result:
        print(item)


if __name__ == "__main__":
    import asyncio

    # asyncio.run(basic())
    # asyncio.run(qdrant())
    # asyncio.run(basic_ext())
    asyncio.run(qdrant_ext())
