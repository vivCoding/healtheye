from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

import itertools
import cv2
import os
import math
import numpy as np
from draw_detections import draw_objects

class Vision:
    def __init__ (self, prediction_key, endpoint, iteration_id, iteration_name):
        """Makes a call to custom vision api and use trained model to detect people
        """
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        self._predictor = CustomVisionPredictionClient(endpoint, credentials)
        self._iteration_id = iteration_id
        self._iteration_name = iteration_name

    def detect_people(self, filepath, show=False):
        """Makes a call to custom vision api and use trained model to detect people
        """
        if show: print ("Making call to vision api...")
        people = []
        with open(filepath, mode="rb") as image:
            results = self._predictor.detect_image(self._iteration_id, self._iteration_name, image)
        for prediction in results.predictions:
            if(prediction.tag_name == "person" and prediction.probability > .2):
                people.append(prediction)
        count = len(people)
        if show: draw_objects(filepath, people, wait=True)
        return people

    def get_points_from_box(self, prediction, pixw, pixh):
        """
        prediction.bounding_box.left = x
        prediction.bounding_box.top = y
        prediction.bounding_box.width = w
        prediction.bounding_box.height = h
        """
        center = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,
                prediction.bounding_box.top*pixh + prediction.bounding_box.height*pixh)
        upoid = (prediction.bounding_box.width*pixw / 2 + prediction.bounding_box.left*pixw,  prediction.bounding_box.top*pixh)
        return center, upoid

    def get_centroids_and_uppoints(self, predictions, pixw, pixh):
        """
        For every bounding box, compute the centroid and the point located on the bottom center of the box
        @ array_boxes_detected : list containing all our bounding boxes
        """
        array_centroids, array_uppoints = [], []  # Initialize empty centroid and ground point lists
        for prediction in predictions:
            # Draw the bounding box
            # Get the both important points
            centroid, up_point = self.get_points_from_box(prediction, pixw, pixh)
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
        #list_points_to_detect = np.float32(list_upoids).reshape(-1, 1, 2)
        list_points_to_detect = np.float32(list_upoids).reshape(-1, 1, 2)
        transformed_points = cv2.perspectiveTransform(list_points_to_detect, matrix)
        # Loop over the points and add them to the list that will be returned
        transformed_points_list = list()
        try:
            for i in range(0, transformed_points.shape[0]):
                transformed_points_list.append([transformed_points[i][0][0], transformed_points[i][0][1]])
        except Exception as e:
            print ("computer point perspective transformation error", e)
        return transformed_points_list
    
    # TODO: { people, violations, time, location }
    def analyzeFrame(self, image_path, dist_threshold=100):
        val = [[ 1022 ,  91 ], [1879 ,  228 ], [9 ,  883], [1637 ,  1072]]
        # for now if val does not exist just set a default val array and we will deal with it later
        # for now if covid violation threshold does not exist just set a default val array and we will deal with it later
        img = cv2.imread(image_path)
        # method to get the num of poeple in a image frame and
        predictions = self.detect_people(image_path)
        p_count = len(predictions)
        if p_count == 0:
            return predictions, 0, 0
        # val[x][y] ---> verticies of image
        corner_points = [[val[0][0], val[0][1]], [val[1][0], val[1][1]], [val[2][0], val[2][1]], [val[3][0], val[3][1]]]
        M, new_img = self.compute_perspective_transform(corner_points, img)
        h = img.shape[1]
        w = img.shape[0]
        array_centroids, array_uppoints = self.get_centroids_and_uppoints(predictions, h, w)
        transformed_points_list = self.compute_point_perspective_transformation(M, array_uppoints)
        violation_count = 0
        for i, pair in enumerate(itertools.combinations(transformed_points_list, r=2)):
            # print(pair) --> testing method
            # get distance from points - print this out see whats going on
            if math.sqrt((pair[0][0] - pair[1][0]) ** 2 + (pair[0][1] - pair[1][1]) ** 2) < int(dist_threshold):
                violation_count = violation_count + 1
        return predictions, p_count, violation_count