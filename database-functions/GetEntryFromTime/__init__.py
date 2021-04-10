import logging
import azure.functions as func
import json

def make_message(message={"status": "ok"}, status=200):
    return func.HttpResponse(
        json.dumps(message),
        status_code=200,
        mimetype="application/json" 
    )

def main(req: func.HttpRequest, doc:func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    entries = []
    for entry in doc:
        if entry["id"] != "recent":
            entries.append({
                "people": entry["people"],
                "violations": entry["violations"],
                "time": entry["time"],
                "location": entry["location"]
            })

    return make_message(entries)
