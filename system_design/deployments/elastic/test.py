from datetime import datetime
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200/", api_key="YOUR_API_KEY")

doc = {
    "author": "kimchy",
    "text": "Elasticsearch: cool. bonsai cool.",
    "timestamp": datetime.now(),
}
resp = client.index(index="test-index", id=1, document=doc)
print(resp["result"])

resp = client.get(index="test-index", id=1)
print(resp["_source"])

client.indices.refresh(index="test-index")

resp = client.search(index="test-index", query={"match_all": {}})
print("Got {} hits:".format(resp["hits"]["total"]["value"]))
for hit in resp["hits"]["hits"]:
    print("{timestamp} {author} {text}".format(**hit["_source"]))
