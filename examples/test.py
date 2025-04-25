"""Sample for EasyMem."""  # noqa: INP001

import json

from easymem.basic.easymem import BasicEasyMem
from easymem.basic.message import BasicMemMessage


async def main() -> None:  # noqa: D103
    mem = BasicEasyMem(BasicMemMessage)
    await mem.add(BasicMemMessage(content="Hello", date="2023-10-01"))
    await mem.add(BasicMemMessage(content="World", date="2023-10-02"))
    await mem.add(BasicMemMessage(content="Python", date="2023-10-03"))
    result, query = await mem.massivequery("find Hello and Python")
    print("Query:", json.dumps(query, indent=2))
    print("Result:", result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
