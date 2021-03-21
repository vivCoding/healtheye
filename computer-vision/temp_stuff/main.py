from PIL import Image, ImageDraw, ImageFont
import os

def save_image(image, filename, ext):
    n = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    while os.path.exists("output/" + filename + "_" + str(n) + ext):
        n += 1
    image.save("output/" + filename + "_" + str(n) + ext)

def draw_objects(image_path, objects, label=False, show=False):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font="assets/Hack-Bold.ttf", size=15)
    for object in objects:
        draw.rectangle((
            object.rectangle.x,
            object.rectangle.y,
            object.rectangle.x + object.rectangle.w,
            object.rectangle.y + object.rectangle.h
        ), fill=None, outline="red", width=2)
        if label: draw.text((object.rectangle.x + 1, object.rectangle.y + 1), object.object_property, font=font, fill="red")
    if show: image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    save_image(image, filename, ext)

def draw_faces(image_path, faces, show=False):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font="assets/Hack-Bold.ttf", size=15)
    for face in faces:
        draw.rectangle((
            face.face_rectangle.left,
            face.face_rectangle.top,
            face.face_rectangle.left + face.face_rectangle.width,
            face.face_rectangle.top + face.face_rectangle.height
        ), fill=None, outline="red", width=2)
        # draw.text((face.face_rectangle.left + 1, face.face_rectangle.top + 1), "face", font=font, fill="red")
    if show: image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    save_image(image, filename, ext)







from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
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