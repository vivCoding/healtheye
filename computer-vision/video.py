import cv2
import time
from worker import Worker
import os
from detections import Detections

vision = Detections()

worker = Worker()

print ("Getting video capture...")
capture = cv2.VideoCapture(2)
if not capture.isOpened():
    print ("Cannot get video capture!")
    exit(0)

print ("Setting up capture...")
# setting resolution to max
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print ("Camera res:", capture.get(cv2.CAP_PROP_FRAME_WIDTH), "x", capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
# setting fps
desired_fps = 6
fps = capture.get(cv2.CAP_PROP_FPS)
frame_frequency = int(fps / desired_fps)
frame_count = 0
print ("Camera FPS:", desired_fps)

print ("Displaying video. Press space to exit...")
while True:
    ret, frame  = capture.read()
    if ret is False:
        continue
    # to maintain desired fps, skip every few frames
    frame_count += 1
    if frame_count % frame_frequency == 0:
        worker.add_frame(frame)
        cv2.imshow("video capture", frame)
        key = cv2.waitKey(10)
        if key == ord(" "):
            break

worker.join()
capture.release()
cv2.destroyAllWindows()