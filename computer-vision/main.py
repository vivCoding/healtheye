from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
from draw_detections import draw_objects, draw_faces
import os
import sys
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

def detect_people(stream):
    # ideal detection image size: 440 x 354
    print("Detecting objects in local image...")
    object_results = computervision_client.detect_objects_in_stream(stream)
    if len(object_results.objects) == 0:
        print("No objects detected.")
    else:
        print ("Found objects")
        people = [object for object in object_results.objects if object.object_property == "person"]
        draw_objects(image_path, people)

def detect_faces(stream):
    print("Detecting faces in local image...")
    face_results = computervision_client.analyze_image_in_stream(stream, ["faces"])
    if len(face_results.faces) == 0:
        print("No objects detected.")
    else:
        print ("Found objects")
        draw_faces(image_path, face_results.faces)

if __name__ == "__main__":
    # TODO: use arguments to test image
    # example: python main.py test/students.jpg
    # ideal images are 1280 x 720
    image_path = sys.argv[1]
    image = open(image_path, "rb")
    detect_people(image)