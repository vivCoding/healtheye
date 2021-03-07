from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
from draw_detections import draw_objects, draw_faces
from image_slicer import slice, join
import image_slicer
import os
import sys

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

def detect_people(filepath, show=False):
    # ideal detection image size: 440 x 354
    print("Detecting people...")
    object_results = computervision_client.detect_objects_in_stream(open(filepath, "rb"))
    people = [object for object in object_results.objects if object.object_property == "person"]
    count = len(people)
    draw_objects(filepath, people, show=show)
    return count

def detect_faces(filepath, show=False):
    print("Detecting faces...")
    face_results = computervision_client.analyze_image_in_stream(open(filepath, "rb"), ["faces"])
    count = len(face_results.faces)
    draw_faces(filepath, face_results.faces, show=show)
    return count

if __name__ == "__main__":
    # TODO: use arguments to test image
    # example: python main.py test/students.jpg
    # webcam images are 1280 x 720
    image_path = sys.argv[1]
    count = detect_people(image_path, show=True)

    new_count = 0
    slices = slice(image_path, 6)
    for tile in slices:
        new_count += detect_people(tile.filename)
        os.remove(tile.filename)
    if new_count > count:
        count = new_count
    print("Total people: ", count)