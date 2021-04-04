from dotenv import load_dotenv
from vision import Vision
import os
import sys
import getopt

def main():
    load_dotenv()

    vision = Vision(
        os.getenv("PREDICTION_KEY"),
        os.getenv("ENDPOINT"),
        os.getenv("ITERATION_ID"),
        os.getenv("ITERATION_NAME")
    )

    try:
        argv = sys.argv[1:]
        opts, args = getopt.getopt(argv, "i:v:c:h")
    except getopt.GetoptError:
        print ("Bad arguments! Use -h for help")
        exit(1)
    for opt, arg in opts:
        if opt == "-h":
            print ("-" * 30)
            print ("Input Options (choose one):")
            print ("-i <path to image file> : Analyzes one image")
            print ("-v <path to video file> : Analyzes video")
            print ("-c <port number for camera> : Analyzes camera stream")
            print ("\n-h : display help")
            print ("-" * 30)
            exit(0)
        elif opt == "-i":
            vision.detect_people(arg, True)
            

if __name__ == "__main__":
    main()