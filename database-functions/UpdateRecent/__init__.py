import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import os

ENDPOINT = os.getenv("CosmosDBEndpoint", "")
KEY = os.getenv("CosmosDBKey", "")
DB = os.getenv("CosmosDBId", "")
CONTAINER = os.getenv("CosmosDBContainerId", "")


client = cosmos_client.CosmosClient(ENDPOINT, KEY)
database = client.get_database_client(DB)
container = database.get_container_client(CONTAINER)

def main(documents: func.DocumentList) -> str:
    try:
        item = container.read_item(item="recent", partition_key="recent")
    except:
        item = container.create_item({
            "id": "recent",
            "time": ""
        })
    item["time"] = documents[0]["time"]
    response = container.replace_item(item=item, body=item)
    
