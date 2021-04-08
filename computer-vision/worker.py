import queue
import threading
import time
import cv2
import os
import shutil
from draw_detections import draw_objects
import requests
import json
import datetime

class Worker:
    def __init__(self, vision, frame_delay=-1):
        self.vision = vision
        self.frame_delay = frame_delay
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self.process_frames)
        self._imshow_queue = queue.Queue()
        self._dbqueue = queue.Queue()
        self._dbthread = threading.Thread(target=self.send_to_db)
        self.running = False
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
        while self.running:
            frame = self._queue.get()
            file_path = os.path.join(self.temp_folder, str(self._transactions) + ".png")
            cv2.imwrite(file_path, frame)
            # predictions = []
            # people_count = 0
            # violations = 0
            predictions, people_count, violations = self.vision.analyzeFrame(file_path)
            print ("Process:", self._transactions, ", Queued:", self._queue.qsize(), ", People:", people_count, ", Violations:", violations, end="\r")
            self._transactions += 1
            self._imshow_queue.put([frame, predictions])
            self._dbqueue.put([people_count, violations])
            if self._transactions >= self.max_temp:
                shutil.rmtree(self.temp_folder)
                os.mkdir(self.temp_folder)

    def start(self):
        if not self.running:
            self.running = True
            self._thread.start()
            self._dbthread.start()

    def stop(self):
        self.running = False
        self._thread.join()
        self._dbthread.join()
        print ("\n")

    def join(self):
        while self._queue.qsize() > 0 or self._imshow_queue.qsize() > 0 or self._dbqueue.qsize() > 0:
            self.show_frames()
            # print ("\n", self._dbqueue.qsize(), self._imshow_queue.qsize())
            time.sleep(self.frame_delay)
        self.running = False
        self._thread.join()
        self._dbthread.join()
        print ("\n")

    def show_frames(self):
        if self._imshow_queue.qsize() > 0:
            data = self._imshow_queue.get()
            frame = data[0]
            people = data[1]
            draw_objects(frame, people)

    def send_to_db(self):
        location_name = os.getenv("LOCATION_NAME", "no location specified")
        location_latitude = os.getenv("LOCATION_LAT", 0)
        location_longitude = os.getenv("LOCATION_LONG", 0)
        simulated = os.getenv("SIMULATED", "false") == "true"
        send_to_db = os.getenv("SEND_TO_DB", "false") == "true"
        db_endpoint = os.getenv("DB_ENDPOINT", "")
        if simulated:
            current_hour = 12
            current_min = 0
        while self.running and send_to_db:
            toadd = self._dbqueue.get()
            # this is just to simulate real data
            if simulated:
                current_min += 1
                if current_min > 60:
                    current_min = 0
                    current_hour += 1
                if current_hour > 24:
                    current_hour = 0
                new_time = datetime.datetime(2021, 4, 1, current_hour, current_min, 21).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "people": toadd[0],
                "violations": toadd[1],
                "time": new_time if simulated else time.strftime("%Y-%m-%d %H:%M:%S"),
                "location": {
                    "name": location_name,
                    "latitude": location_latitude,
                    "longitude": location_longitude
                }
            }
            r = requests.post(db_endpoint, json=data)
            resp = r.json()
            if r.status_code != 200:
                print ("error sending to database!")
            elif resp.get("status", "error") != "ok":
                print ("\n", resp.get("status", "error"))