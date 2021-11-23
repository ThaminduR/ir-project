from elasticsearch import Elasticsearch, client, helpers
import json
from time import sleep

client = Elasticsearch("localhost:9200")

json_file = open("../irpScrape/data/pm-si-data.json", "r", encoding="utf-8")

data = json.load(json_file)

print("Number of Documents: ", len(data))


id = 1
for item in data:
    item["_id"] = id
    id += 1

try:
    print("\nCreating index")

    resp = helpers.bulk(
        client,
        data,
        index="lk-pm-en",
        doc_type="_doc"
    )

    print("Response: ", resp)
    print("Response: ", json.dumps(resp, indent=4))

except Exception as err:
    print("Elasticsearch Error", err)
    quit()

query_all = {
    'size': 10_000,
    'query': {
        'match_all': {}
    }
}

sleep(2)

resp = client.search(
    index="lk-pm-en",
    body=query_all
)

# print ("search() response:", json.dumps(resp, indent=4))

print ("Length of docs returned by search():", len(resp['hits']['hits']))