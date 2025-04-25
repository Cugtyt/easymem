# ruff: noqa: INP001, T201, D103, ANN201, D100

import json

from easymem.basic.easymem import BasicEasyMem
from easymem.basic.message import BasicMemMessage
from easymem.ext.qdrant.easymem import QdrantEasyMem
from easymem.ext.qdrant.message import QdrantMemMessage


async def basic() -> None:
    mem = BasicEasyMem(BasicMemMessage)
    await mem.add(BasicMemMessage(content="Hello", date="2020-10-01"))
    await mem.add(BasicMemMessage(content="World", date="2023-10-02"))
    await mem.add(BasicMemMessage(content="Python", date="2023-10-03"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query, indent=2))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello and Python before 2023-01-01")
    print("Query:", json.dumps(query, indent=2))
    print("Result:")
    for item in result:
        print(item)


async def qdrant():
    mem = QdrantEasyMem(QdrantMemMessage)
    await mem.add(QdrantMemMessage(content="Hello", datetime="2020-10-01T00:00:00Z"))
    await mem.add(QdrantMemMessage(content="World", datetime="2023-10-02T00:00:00Z"))
    await mem.add(QdrantMemMessage(content="Python", datetime="2023-10-03T00:00:00Z"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query, indent=2))
    print("Result:")
    for item in result:
        print(item)

    result, query = await mem.massivequery("find Hello and Python before 2023-01-01")
    print("Query:", json.dumps(query, indent=2))
    print("Result:")
    for item in result:
        print(item)


if __name__ == "__main__":
    import asyncio

    asyncio.run(basic())
    asyncio.run(qdrant())
