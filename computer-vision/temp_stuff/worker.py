import queue
import threading
import time
import cv2
from detections import Detections
import os
import shutil

class Worker:
    def __init__(self):
        self._queue = queue.Queue()
        self._imshow_queue = queue.Queue()
        self._thread = threading.Thread(target=self.process_frames)
        self._vision = Detections()
        self._running = False
        self._transactions = 0
        self.temp_folder = "temp"

    def add_frame(self, frame):
        self._queue.put(frame)
        # print ("added frame")
        self.start()

    def process_frames(self):
        if not os.path.exists(self.temp_folder):
            os.mkdir(self.temp_folder)
        else:
            shutil.rmtree(self.temp_folder)
            os.mkdir(self.temp_folder)
        while self._running:
            frame = self._queue.get()
            file_path = os.path.join(self.temp_folder, str(self._transactions) + ".png")
            img = cv2.imwrite(file_path, frame)
            people = self._vision.detect_people(open(file_path, "rb"))
            for person in people:
                cv2.rectangle(frame,
                    (person.rectangle.x, person.rectangle.y),
                    (person.rectangle.x + person.rectangle.w, person.rectangle.y + person.rectangle.h),
                    (0, 0, 255), 3
                )
            cv2.imwrite(file_path, frame)
            print ("Processing:", self._transactions, "/", self._queue.qsize(), ", we got", len(people))
            self._transactions += 1
            # self._imshow_queue.put([frame, people])
            # do other api stuff here
            if self._transactions >= 200:
                shutil.rmtree(self.temp_folder)
                os.mkdir(self.temp_folder)

    def start(self):
        if not self._running:
            self._running = True
            self._thread.start()

    def join(self):
        self._running = False
        self._thread.join()

    def show_frames(self, fps):
        # print ("showing frame")
        if self._imshow_queue.qsize() > fps * 4:
            data = self._imshow_queue.get()
            frame = data[0]
            people = data[1]
            for person in people:
                cv2.rectangle(frame,
                    (person.rectangle.x, person.rectangle.y),
                    (person.rectangle.x + person.rectangle.w, person.rectangle.y + person.rectangle.h),
                    (0, 0, 255), 3
                )
            cv2.imshow("video capture", frame)
