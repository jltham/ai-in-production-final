import requests
import os
import weaviate


def populate_vector_db():
    text_files_paths = [
        file_path for file_path in os.listdir("./data") if file_path.endswith(".txt")
    ]

    contents = []

    for text_file_path in text_files_paths:
        with open(f"./data/{text_file_path}", "r") as fp:
            contents.append(fp.read())

    embeddings = requests.post(
        "http://ollama:11434/api/embed", json={"model": "nomic-embed-text", "input": contents}
    ).json()["embeddings"]

    client = weaviate.connect_to_local(host="weaviate")

    try:
        collection = client.collections.get("RedDragonWebpage")
        print(collection)
    except Exception as e:
        collection = client.collections.create(
            name="RedDragonWebpage",
            vectorizer_config=[
                weaviate.classes.config.Configure.NamedVectors.none(name="data"),
            ],
            properties=[
                weaviate.classes.config.Property(
                    name="data", data_type=weaviate.classes.config.DataType.TEXT
                ),
            ],
        )

    for i in range(len(contents)):
        collection.data.insert(
            properties={"data": contents[i]},
            uuid=weaviate.util.generate_uuid5({"title": text_files_paths[i], "data": contents[i]}),
            vector=embeddings[i],
        )

    client.close()


def retrieve_near(prompt):
    client = weaviate.connect_to_local(host="weaviate")
    data_collection = client.collections.get("RedDragonWebpage")

    vector = requests.post(
        "http://ollama:11434/api/embed", json={"model": "nomic-embed-text", "input": prompt}
    ).json()["embeddings"][0]

    response = data_collection.query.near_vector(near_vector=vector, limit=2, target_vector="data")

    client.close()

    return [o.properties["data"] for o in response.objects]
