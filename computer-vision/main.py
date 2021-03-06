from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
from draw_detections import draw_objects
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

image_path = "test/students.jpg"
objects_results = computervision_client.detect_objects_in_stream(open(image_path, "rb"))

print("Detecting objects in local image:")
if len(objects_results.objects) == 0:
    print("No objects detected.")
else:
    print ("Found objects")
    draw_objects(image_path, objects_results.objects)