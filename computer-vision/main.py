from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import cv2
def save_image(image, filename, ext):
    n = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    while os.path.exists("output/" + filename + "_" + str(n) + ext):
        n += 1
    image.save("output/" + filename + "_" + str(n) + ext)
def num(value):
    return int("{0:.2f}".format(value))
def draw_objects(image_path, objects, label=False, show=False):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
#    font = ImageFont.truetype(font="assets/Hack-Bold.ttf", size=15)
    #w, h = image.size
    img = cv2.imread(image_path)
    w = img.shape[1]
    h = img.shape[0]

    for object in objects:
        draw.rectangle((
            object.bounding_box.left*w,
            object.bounding_box.top*h,
            object.bounding_box.left*w + object.bounding_box.width*w,
            object.bounding_box.top*h + object.bounding_box.height*h
        ), fill=None, outline="red", width=2)
        if label: draw.text((object.bounding_box.left*w + 1, object.bounding_box.top*h + 1), object.object_property, font = font, fill="red")
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
        draw.text((face.face_rectangle.left + 1, face.face_rectangle.top + 1), "face", font=font, fill="red")
    if show: image.show()

    filename, ext = os.path.splitext(os.path.basename(image_path))
    save_image(image, filename, ext)







# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time


from dotenv import load_dotenv
from image_slicer import slice, join

import image_slicer
import os
import sys

load_dotenv()


ENDPOINT = os.getenv("ENDPOINT")
prediction_key = os.getenv("prediction_key")
# computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)



def detect_people(filepath, show=False):
    # ideal detection image size: 440 x 354
    print("Detecting people...")
    people = []
    with open(filepath, mode="rb") as test_data:
        results = predictor.detect_image("4e4dce9c-c8c0-491f-a3eb-0121d32cd620", "Iteration6", test_data)
    #object_results = results.detect_objects_in_stream(open(filepath, "rb"))
    for prediction in results.predictions:
        if(prediction.tag_name == "person" and prediction.probability >.2):
            people.append(prediction)
    #people = [object for object in object_results.objects if object.object_property == "person"]
    # object_results2  = computervision_client.analyze_image_by_domain_in_stream(open(filepath, "rb"))
    # print(object_results2.keys)
    count = len(people)
    draw_objects(filepath, people, show=show)
    return count, people


# def detect_faces(filepath, show=False):
#     print("Detecting faces...")
#     face_results = computervision_client.analyze_image_in_stream(open(filepath, "rb"), ["faces"])
#     count = len(face_results.faces)
#     draw_faces(filepath, face_results.faces, show=show)
#     return count

def get_points_from_box(prediction, pixw, pixh):
    # prediction.bounding_box.left = x
    # prediction.bounding_box.top = y
    # prediction.bounding_box.width = w
    # prediction.bounding_box.height = h
    # center = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,
    #           prediction.bounding_box.top*pixh + prediction.bounding_box.height*pixh)
    # upoid = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,  prediction.bounding_box.top*pixh)
    center = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,
              prediction.bounding_box.top*pixh + prediction.bounding_box.height*pixh/2)
    upoid = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,  prediction.bounding_box.top*pixh)
    return center, upoid

# #center = (width/2+x,y+length/2)
# #upoid =(x+width/2, y)
# """
# Get the center of the bounding and the point "on the ground"
# @ param = box : 2 points representing the bounding box
# @ return = centroid (x1,y1) and ground point (x2,y2)
# """
# # Center of the box x = (x1+x2)/2 et y = (y1+y2)/2
#
# center_x = int(((box[1]+box[3])/2))
# center_y = int(((box[0]+box[2])/2))
# # Coordiniate on the point at the bottom center of the box
# center_y_ground = center_y + ((box[2] - box[0])/2)
# return (center_x,center_y),(center_x,int(center_y_ground))

def get_centroids_and_uppoints(predictions, pixw, pixh):
    """
    For every bounding box, compute the centroid and the point located on the bottom center of the box
    @ array_boxes_detected : list containing all our bounding boxes
    """
    array_centroids, array_uppoints = [], []  # Initialize empty centroid and ground point lists
    for prediction in predictions:
        # Draw the bounding box
        # c
        # Get the both important points
        centroid, up_point = get_points_from_box(prediction, pixw, pixh)
        array_centroids.append(centroid)
        array_uppoints.append(centroid)
    return array_centroids, array_uppoints

# array_groundpoints is pased in as param list_downoids in compute point transformation

# corner points = corner points of the portion of the image where you want to detect objects (one set of opposite sides must be ||)
# get the height and width of the image, read the image like cv2.imread(img_path)
def compute_perspective_transform(corner_points, img):
    pt_A = corner_points[0]
    pt_B = corner_points[1]
    pt_C = corner_points[2]
    pt_D = corner_points[3]
    width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))

    input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])
    # matrix
    M = cv2.getPerspectiveTransform(input_pts, output_pts)
    out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    return M, out


# matrix is the transformed image, list of downoids are the list of points that represent objects detected in the image(bottom center of image)
def compute_point_perspective_transformation( matrix, list_upoids):
    """ Apply the perspective transformation to every ground point which have been detected on the main frame.
    @ matrix : the 3x3 matrix
    @ list_downoids : list that contains the points to transform
    return : list containing all the new points
    """
    # Compute the new coordinates of our points
    #list_points_to_detect = np.float32(list_upoids).reshape(-1, 1, 2)
    list_points_to_detect = np.float32(list_upoids).reshape(-1, 1, 2)
    transformed_points = cv2.perspectiveTransform(list_points_to_detect, matrix)
    # Loop over the points and add them to the list that will be returned
    transformed_points_list = list()
    for i in range(0, transformed_points.shape[0]):
        transformed_points_list.append([transformed_points[i][0][0], transformed_points[i][0][1]])
    return transformed_points_list

def click_event(event, x, y):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

if __name__ == "__main__":
    # TODO: use arguments to test image
    # example: python main.py test/students.jpg
    # webcam images are 1280 x 720
    #image_path = sys.argv[1]
    image_path =  "/Users/shellyganga/Desktop/test3.png"


    count, predictions = detect_people(image_path, show=True)

    new_count = 0
    # slices = slice(image_path, 6)
    # for tile in slices:
    #     new_count += detect_people(tile.filename)[0]
    #     os.remove(tile.filename)
    # if new_count > count:
    #     count = new_count
    print("Total people: ", count)
    #[254,277], [474,369], [598,227], [446,139]
    # 127
    # 304
    # 397
    # 452
    # 709
    # 249
    # 489
    # 153
    # [100, 260], [366, 485], [710, 275], [480, 133]
    # reading the image
    # ix, iy = -1, -1
    # val = []
    # img = cv2.imread(image_path, 1)
    #
    # # displaying the image
    # cv2.imshow('image', img)

    # setting mouse hadler for the image
    # and calling the click_event() function
    # cv2.setMouseCallback('image', click_event)
    # while (len(val)!=4):
    #     print(len(val))
    #     check = -1
    #     cv2.imshow('image', img)
    #     k = cv2.waitKey() & 0xFF
    #     if k == 27:
    #         break
    #     elif k == ord('a'):
    #         val.append([ix, iy])
    # for point in val:
    #     print(point)
    # cv2.destroyAllWindows()
    # corner_points = [[val[0][0],val[0][1]], [val[1][0],val[1][1]], [val[2][0],val[2][1]], [val[3][0],val[3][1]]]
    corner_points = [[100,304], [397,452], [709,249], [489,153]]
    M, new_img = compute_perspective_transform(corner_points, cv2.imread(image_path))
    img = cv2.imread(image_path)
    h = img.shape[1]
    w = img.shape[0]
    # image = Image.open(image_path)
    # w, h = image.size
    array_centroids, array_uppoints = get_centroids_and_uppoints(predictions, h, w)
    transformed_points_list = compute_point_perspective_transformation(M, array_uppoints)
    for point in transformed_points_list:
        print(point)
        new_img = cv2.circle(new_img, (point[0], point[1]), radius=5, color=(0, 0, 255), thickness=-1)
    # cv2.startWindowThread()
    # cv2.namedWindow("preview")
    # cv2.imshow("preview", new_img)
    #
    # cv2.waitKey()
    #(237, 205)
    # [134.45435, 370.00583]
    # [72.73135, 250.46169]
    # [10.99829, 252.83537]
    # [125.809105, 362.99817]

    #new_img = cv2.circle(new_img, (226, 216), radius=10, color=(0, 0, 255), thickness=-1)
    cv2.startWindowThread()
    cv2.namedWindow("preview2")
    cv2.imshow("preview2", new_img)
    cv2.waitKey()