import queue
import threading
import time
import cv2
#from detections import Detections
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



def getFrames(video_path, desired_fps):
    array = []
    cameraCapture = cv2.VideoCapture(video_path)
    fps = cameraCapture.get(cv2.CV_CAP_PROP_FPS)
    frame_frequency = int(fps / desired_fps)
    frame_count = 0
    while success:
        success, frame = cameraCapture.read()
        frame_count = frame_count +1
        time = float(frame_count) / fps
        if frame_count % frame_frequency == 0:
            array.append([[frame],[time]])
    cv2.destroyAllWindows()
    cameraCapture.release()
    return getFrames


    # frameData = []
    # array = []
    # cameraCapture = cv2.VideoCapture('./res/2_003_013.mp4')
    #
    # success, frame = cameraCapture.read()
    # while success:
    #     if cv2.waitKey(1) == 27:
    #         break
    #     cv2.imshow('Test camera', frame)
    #     frameData.append([frame])
    #
    #     success, frame = cameraCapture.read()
    #     milliseconds = cameraCapture.get(cv2.CAP_PROP_POS_MSEC)
    #     frameData.append([])
    #     seconds = milliseconds//1000
    #     milliseconds = milliseconds%1000
    #     minutes = 0
    #     hours = 0
    #     if seconds >= 60:
    #         minutes = seconds//60
    #         seconds = seconds % 60
    #
    #     if minutes >= 60:
    #         hours = minutes//60
    #         minutes = minutes % 60
    #
    # print(int(hours), int(minutes), int(seconds), int(milliseconds))

    cv2.destroyAllWindows()
    cameraCapture.release()
#
# desired_fps = 6
# fps = capture.get(cv2.CAP_PROP_FPS)
# frame_frequency = int(fps / desired_fps)
# ret, frame  = capture.read()
#     if ret is False:
#         continue
#     # to maintain desired fps, skip every few frames
#     frame_count += 1
#     if frame_count % frame_frequency == 0:
#         worker.add_frame(frame)
#         cv2.imshow("video capture", frame)
#         key = cv2.waitKey(10)
#         if key == ord(" "):
#             break