import logging
import azure.functions as func
import json
from uuid import uuid4

def make_message(message={"status": "ok"}, status=200):
    return func.HttpResponse(
        json.dumps(message),
        status_code=200,
        mimetype="application/json" 
    )

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        data = req.get_json()
    except ValueError:
        return make_message({"status": "error! no parameters provided" })
    else:
        doc.set(func.Document.from_dict({
            "id": uuid4().hex,
            "people": data.get("people", 0),
            "violations": data.get("violations", 0),
            "time": data.get("time", "0"),
            "location": data.get("location", {})
        }))
        return make_message({ "status": "ok" })
