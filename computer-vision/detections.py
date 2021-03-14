from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
import os

class Detections:
    def __init__(self):
        load_dotenv()
        self._API_KEY = os.getenv("API_KEY")
        self._ENDPOINT = os.getenv("ENDPOINT")
        self._client = ComputerVisionClient(self._ENDPOINT, CognitiveServicesCredentials(self._API_KEY))

    def detect_people(self, img):
        object_results = self._client.detect_objects_in_stream(img)
        people = [object for object in object_results.objects if object.object_property == "person"]
        return people