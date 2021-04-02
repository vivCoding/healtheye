from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
import os
import cv2
import numpy as np

class Detections:
    def __init__(self):
        load_dotenv()
        self._API_KEY = os.getenv("API_KEY")
        self._ENDPOINT = os.getenv("ENDPOINT")
        self._client = ComputerVisionClient(self._ENDPOINT, CognitiveServicesCredentials(self._API_KEY))

    def get_points_from_box(slelf, prediction):
        center = (prediction.rectangle.w / 2 + prediction.rectangle.x,
                  prediction.rectangle.y + prediction.rectangle.h)
        upoid = (prediction.bounding_box.width / 2 + prediction.bounding_box.left, prediction.bounding_box.top)
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

    def get_centroids_and_uppoints(self, predictions):
        """
        For every bounding box, compute the centroid and the point located on the bottom center of the box
        @ array_boxes_detected : list containing all our bounding boxes
        """
        array_centroids, array_uppoints = [], []  # Initialize empty centroid and ground point lists
        for prediction in predictions:
            # Draw the bounding box
            # c
            # Get the both important points
            centroid, up_point = self.get_points_from_box(prediction)
            array_centroids.append(centroid)
            array_uppoints.append(centroid)
        return array_centroids, array_uppoints

    # array_groundpoints is pased in as param list_downoids in compute point transformation

    # corner points = corner points of the portion of the image where you want to detect objects (one set of opposite sides must be ||)
    # get the height and width of the image, read the image like cv2.imread(img_path)
    def compute_perspective_transform(self, corner_points, img):
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
    def compute_point_perspective_transformation(self, matrix, list_upoids):
        """ Apply the perspective transformation to every ground point which have been detected on the main frame.
        @ matrix : the 3x3 matrix
        @ list_downoids : list that contains the points to transform
        return : list containing all the new points
        """
        # Compute the new coordinates of our points
        list_points_to_detect = np.float32(list_upoids).reshape(-1, 1, 2)
        transformed_points = cv2.perspectiveTransform(list_points_to_detect, matrix)
        # Loop over the points and add them to the list that will be returned
        transformed_points_list = list()
        for i in range(0, transformed_points.shape[0]):
            transformed_points_list.append([transformed_points[i][0][0], transformed_points[i][0][1]])
        return transformed_points_list


    def detect_people(self, img):
        object_results = self._client.detect_objects_in_stream(img)

        people = [object for object in object_results.objects if object.object_property == "person"]
        return people

    def image_trans(self, img, corner_points):
        predictions = self.detect_people(self, img)
        M, new_img = self.compute_perspective_transform(self, corner_points, img)
        array_centroids, array_uppoints = self.get_centroids_and_uppoints(predictions)
        transformed_points_list = self.compute_point_perspective_transformation(M,array_uppoints)
        return transformed_points_list, new_img

