import cv2
import time
import os
from worker import Worker

def analyze_video(capture, vision, desired_fps=1, size=None, show=False):
    print ("Starting thread worker...")
    worker = Worker(vision)
    print ("Setting up capture...")
    print (capture)
    capture = cv2.VideoCapture(capture)
    if not capture.isOpened():
        print ("Cannot get video capture!")
        exit(0)
    if size:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
    print ("Camera res:", capture.get(cv2.CAP_PROP_FRAME_WIDTH), "x", capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # setting fps
    fps = capture.get(cv2.CAP_PROP_FPS)
    if desired_fps > fps : desired_fps = fps
    frame_frequency = int(fps / desired_fps)
    time_delay = 1 / fps
    frame_count = 0
    print ("Previous FPS:", fps)
    print ("Current FPS:", desired_fps)

    print ("Displaying video. Press space to exit...")
    while True:
        ret, frame  = capture.read()
        if ret is False:
            print ("Video ended, cannot grab next frame")
            break
        # to maintain desired fps, skip every few frames
        frame_count += 1
        if frame_count % frame_frequency == 0:
            worker.add_frame(frame)
            # cv2.imshow("video capture", frame)
            key = cv2.waitKey(10)
            if key == ord(" "):
                break
        # to maintain fps
        time.sleep(time_delay)

    print ("\nExiting...")
    worker.join()
    capture.release()
    cv2.destroyAllWindows()