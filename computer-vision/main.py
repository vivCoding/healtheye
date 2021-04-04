from dotenv import load_dotenv
import os
import sys
import getopt
from vision import Vision
from video import analyze_video
from draw_detections import draw_objects

def main():
    load_dotenv()

    PREDICTION_KEY = os.getenv("PREDICTION_KEY")
    ENDPOINT = os.getenv("ENDPOINT")
    ITERATION_ID = os.getenv("ITERATION_ID")
    ITERATION_NAME = os.getenv("ITERATION_NAME")

    vision = Vision(PREDICTION_KEY, ENDPOINT, ITERATION_ID, ITERATION_NAME)

    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "i:v:c:h")
    except getopt.GetoptError:
        print ("Bad arguments! Use -h for help")
        exit(1)

    # really cheap arg parsing
    # TODO: add more options using argparse
    fps = 1
    size = (1280, 720)
    for opt, arg in opts:
        if opt == "-h":
            print ("-" * 30)
            print ("Usage: python main.py <input_option> [-h]")
            print ("Input options (choose one):")
            print ("-i <path to image file> : Analyzes one image")
            print ("-v <path to video file> : Analyzes video")
            print ("-c <camera port number> : Analyzes camera stream at specified port number")
            print ("\n-h : display help")
            print ("-" * 30)
            exit(0)
        elif opt == "-i":
            predictions, people_count, violations = vision.analyzeFrame(arg, dist_threshold=1000)
            print ("Number of people:", people_count)
            print ("Violations:", violations)
            draw_objects(arg, predictions, wait=True)
        elif opt == "-v":
            analyze_video(arg, vision, desired_fps=fps, size=size, show=True)
        elif opt == "-c":
            analyze_video(int(arg), vision, desired_fps=fps, size=size, show=True)
        

if __name__ == "__main__":
    main()