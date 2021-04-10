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

    return make_message({
        "time": doc[0]["time"],
    })
