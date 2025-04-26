# EasyMem: a lightweight and flexible multi-dimension memory library for LLM.

This project is based and evolved from [Massive Search](https://github.com/Cugtyt/massivesearch). It is easy to use and leverages the LLM structured output ability to query the multi-dimension memory, the framework is flexible to extend to other databases.

## Examples

You can find the example code [here](./examples/test.py)

``` python
mem = BasicEasyMem()
await mem.add(BasicMemMessage(content="Hello", date="2020-10-01"))
await mem.add(BasicMemMessage(content="World", date="2023-10-02"))
await mem.add(BasicMemMessage(content="Python", date="2023-10-03"))


result, query = await mem.massivequery("find Hello and Python")
print("Query:\n\t", json.dumps(query))
print("Result:")
for item in result:
    print("\t", item)


result, query = await mem.massivequery("find Hello or Python before 2023-01-01")
print("Query:\n\t", json.dumps(query))
print("Result:")
for item in result:
    print("\t", item)
```

Extend the message:

``` python
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

mem = BasicEasyMem(MyBasicMemMessage)
await mem.add(MyBasicMemMessage(content="Hello", date="2020-10-01"))
await mem.add(MyBasicMemMessage(content="World", date="2023-10-02"))
await mem.add(MyBasicMemMessage(content="Python", date="2023-10-03"))


result, query = await mem.massivequery("find Hello and Python")
print("Query:\n\t", json.dumps(query))
print("Result:")
for item in result:
    print("\t", item)


result, query = await mem.massivequery("find Hello or Python before 2023-01-01")
print("Query:\n\t", json.dumps(query))
print("Result:")
for item in result:
    print("\t", item)
```

Support external database like Qdrant:

``` python
mem = QdrantEasyMem()
await mem.add(QdrantMemMessage(content="Hello", datetime="2020-10-01T00:00:00Z"))
await mem.add(QdrantMemMessage(content="World", datetime="2023-10-02T00:00:00Z"))
await mem.add(QdrantMemMessage(content="Python", datetime="2023-10-03T00:00:00Z"))


result, query = await mem.massivequery("find Hello and Python")
print("Query:\n\t", query)
print("Result:")
for item in result:
    print("\t", item)


result, query = await mem.massivequery("find Hello or Python before 2023-01-01")
print("Query:\n\t", query)
print("Result:")
for item in result:
    print("\t", item)
```

## Concepts

* message: a python dataclass type with necessary annotation to define the memory message info.
* massive search protocol: a interface to define the search arguments like keywords, and the method to execute.
* model: the ai model to response a massive search queries, it coverts a string query into a list of dict, every key is from message field, and value is massive search arguments organized as dict.
* easymem: the interface to add message and query.