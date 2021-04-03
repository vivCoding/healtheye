import itertools
import math
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import cv2
import sys
from statsmodels.tsa.api import VAR
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
        results = predictor.detect_image("4e4dce9c-c8c0-491f-a3eb-0121d32cd620", "Iteration8", test_data)
    #object_results = results.detect_objects_in_stream(open(filepath, "rb"))
    for prediction in results.predictions:
        if(prediction.tag_name == "person" and prediction.probability >.2):
            people.append(prediction)
    count = len(people)
    draw_objects(filepath, people, show=show)
    return count, people


#projection of the point of their head; onto the ground compare distances
def get_points_from_box(prediction, pixw, pixh):
    # prediction.bounding_box.left = x
    # prediction.bounding_box.top = y
    # prediction.bounding_box.width = w
    # prediction.bounding_box.height = h
    center = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,
              prediction.bounding_box.top*pixh + prediction.bounding_box.height*pixh)
    upoid = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,  prediction.bounding_box.top*pixh)
    # center = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,
    #           prediction.bounding_box.top*pixh + prediction.bounding_box.height*pixh/2)
    # upoid = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,  prediction.bounding_box.top*pixh)
    return center, upoid


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

# def click_event(event, x, y, flags, params):
#         # checking for left mouse clicks
#         if event == cv2.EVENT_LBUTTONDOWN:
#             # displaying the coordinates
#             # on the Shell
#             val.append([x,y])
#
#             # displaying the coordinates
#             # on the image window
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             cv2.putText(img, str(x) + ',' +
#                         str(y), (x, y), font,
#                         1, (255, 0, 0), 2)
#             cv2.imshow('image', img)
#
#         # checking for right mouse clicks
#
#         # displaying the coordinates
#         # on the Shell

#TODO: { people, violations, time, location }
def analyzeFrame(image_path,val, dist_threshold):
    #for now if val does not exist just set a default val array and we will deal with it later
    #for now if covid violation threshold does not exist just set a default val array and we will deal with it later
    img = cv2.imread(image_path)
    #method to get the num of poeple in a image frame and
    p_count, predictions = detect_people(image_path, show=True)
    #val[x][y] ---> verticies of image
    corner_points = [[val[0][0], val[0][1]], [val[1][0], val[1][1]], [val[2][0], val[2][1]], [val[3][0], val[3][1]]]
    M, new_img = compute_perspective_transform(corner_points, img)
    h = img.shape[1]
    w = img.shape[0]
    array_centroids, array_uppoints = get_centroids_and_uppoints(predictions, h, w)
    transformed_points_list = compute_point_perspective_transformation(M, array_uppoints)
    violation_count = 0
    for i, pair in enumerate(itertools.combinations(transformed_points_list, r=2)):
        # print(pair) --> testing methode
        # get distance from points - print this out see whats going on
        if math.sqrt((pair[0][0] - pair[1][0]) ** 2 + (pair[0][1] - pair[1][1]) ** 2) < int(dist_threshold):
            violation_count = violation_count + 1
    return p_count, violation_count

def time_series(data, future_forcast, location):



    #[[people, violations, time, location],[people, violations, time, location],[people, violations, time, location]]
    columns = ["people", "violations", "time", "location"]



    df = pd.DataFrame(data=data, columns=columns)
    df = df[df["location"]==location]
    df['time'] = pd.to_datetime(df['time'])

    for i in range(len(df)):
        df['time'][i] = df['time'][i].hour

    dict_p = {}
    dict_v = {}
    for i in range(len(df)):
        if(df['time'][i] not in dict_p.keys()):
            dict_p[df['time'][i]] = [df["people"][i]]
        else:
            dict_p[df['time'][i]].append(df["people"][i])
        if (df['time'][i] not in dict_v.keys()):
            dict_v[df['time'][i]] = [df["violations"][i]]
        else:
            dict_v[df['time'][i]].append(df["violations"][i])

    people = []
    violations = []
    times = []


    for k, v in dict_p.items():
        people.append(sum(v) / float(len(v)))
        timet = pd.Timestamp(year=2000, month=1, day=1, hour=k, minute=0, second=0)
        times.append(timet)



    for k, v in dict_v.items():
        violations.append(sum(v) / float(len(v)))

    n_df = pd.DataFrame(columns=["people", "violations", "time"])
    n_df["people"] = people
    n_df["violations"] = violations
    n_df["time"] = times
    #df['time'] = pd.to_datetime(df['time'], format='%H')
    #timet = pd.Timestamp(year=0, month=0, day=0, hour=5, minute=0, second=0)
    n_df = n_df.sort_values(by=['time'])
    n_df.time = pd.DatetimeIndex(n_df.time).to_period('H')
    data1 = n_df[["people", 'violations']]
    data1.index = n_df["time"]
    print(data1)

    model = VAR(data1)
    model_fit = model.fit()
    #print(n_df["time"][len(n_df)-1].hour)
    freq = (n_df["time"][0].hour - n_df["time"][len(n_df)-1].hour) / (len(n_df)-1)
    steps = (future_forcast + n_df["time"][0].hour - n_df["time"][0].hour)/freq
    pred = model_fit.forecast(model_fit.y, steps)
    #pred 0 = num of ppl, pred 1 = violations
    return pred[0], pred[1]




