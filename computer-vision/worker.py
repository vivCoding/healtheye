import queue
import threading
import time
import cv2
import os
import shutil
from draw_detections import draw_objects

class Worker:
    def __init__(self, vision):
        self.vision = vision
        self._queue = queue.Queue()
        self._imshow_queue = queue.Queue()
        self._thread = threading.Thread(target=self.process_frames)
        self._running = False
        self._transactions = 0
        self.temp_folder = "temp"
        self.max_temp = 30

    def add_frame(self, frame):
        self._queue.put(frame)
        # print ("added frame")
        self.start()
        self.show_frames()

    def process_frames(self):
        if not os.path.exists(self.temp_folder):
            os.mkdir(self.temp_folder)
        else:
            shutil.rmtree(self.temp_folder)
            os.mkdir(self.temp_folder)
        while self._running:
            frame = self._queue.get()
            file_path = os.path.join(self.temp_folder, str(self._transactions) + ".png")
            cv2.imwrite(file_path, frame)
            # predictions = []
            # people_count = 0
            # violations = 0
            predictions, people_count, violations = self.vision.analyzeFrame(file_path)
            print ("Processing:", self._transactions, "/", self._queue.qsize(), ", we got", people_count, end="\r")
            self._transactions += 1
            self._imshow_queue.put([frame, predictions, people_count, violations])
            if self._transactions >= self.max_temp:
                shutil.rmtree(self.temp_folder)
                os.mkdir(self.temp_folder)

    def start(self):
        if not self._running:
            self._running = True
            self._thread.start()

    def join(self):
        self._running = False
        self._thread.join()

    def show_frames(self):
        if self._imshow_queue.qsize() > 0:
            data = self._imshow_queue.get()
            frame = data[0]
            people = data[1]
            draw_objects(frame, people)