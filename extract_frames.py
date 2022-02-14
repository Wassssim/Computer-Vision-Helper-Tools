import matplotlib.pyplot as plt
import argparse
import multiprocessing
import time
from functools import partial
from datetime import date
import cv2
#import dlib
import imutils
import numpy as np
from imutils.video import FPS, VideoStream
import sys
import re
import os

if len(sys.argv) < 2:
    print("[ERROR] Please provide an input path")
    sys.exit()

input_path = (sys.argv[1]).replace("\\", "/")
file_name = os.path.splitext( os.path.basename(input_path))[0]

args={
    "input": input_path,
    "output": os.path.join( os.path.dirname(input_path), os.path.splitext( os.path.basename(input_path))[0]).replace("\\", "/")
}

print(args["input"])
print(args["output"])

# Check whether the specified path exists or not
isExist = os.path.exists(args["output"])

if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs(args["output"])
  print("The output directory is created")


print("[INFO] opening video file...")
vs = cv2.VideoCapture(args["input"])
input_video_fps= vs.get(cv2.CAP_PROP_FPS)
print(input_video_fps)
# initialize the video writer (we'll instantiate later if need be)
writer = None
# initialize the frame dimensions (we'll set them as soon as we read
# the first frame from the video)
W = None
H = None

totalFrames=0

# start the frames per second throughput estimator
fps = FPS().start()
# loop over frames from the video stream
while True:
    # grab the next frame and handle if we are reading from either
    # VideoCapture or VideoStream
    ret, frame = vs.read()
    #print(ret)
    #print(frame)
    #cv2.imshow("test", frame)
    #frame = frame[1] if args.get("input", False) else frame
    # if we are viewing a video and we did not grab a frame then we
    # have reached the end of the video
    if not ret:
        continue
    else:
        if args["input"] is not None and frame is None:
            break

    """if totalFrames != 75:
        for i in range(0,100):
            for j in range(55, 805):
                frame[i, j, 0] = 0
                frame[i, j, 1] = 0
                frame[i, j, 2] = 0

    
    for i in range(0,300):
        for j in range(0, 150):
            frame[i, j, 0] = 0
            frame[i, j, 1] = 0
            frame[i, j, 2] = 0"""

    # resize the frame to have a maximum width of 500 pixels (the
    # less data we have, the faster we can process it), then convert
    # the frame from BGR to RGB for dlib
    #frame = imutils.resize(frame, width=608)
    rgb=frame
    #rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # if the frame dimensions are empty, set them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    # if we are supposed to be writing a video to disk, initialize
    # the writer
    '''
    if args["output"] is not None and writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"DIVX")
        writer = cv2.VideoWriter(args["output"], fourcc, 30,
            (W, H), True)
    '''
    # check to see if we should write the frame to disk
    #if writer is not None:
     #   writer.write(frame)
    
    if totalFrames % 30 == 0 and totalFrames > -1:
        #if (totalFrames > 2550) and (totalFrames < 2580): 
        cv2.imwrite(str(args["output"]+"/"+file_name.replace(".","_")+"_"+str(totalFrames)+".jpg") , frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    # increment the total number of frames processed thus far and
    # then update the FPS counter
    totalFrames += 1
    fps.update()

    print("Frame:", totalFrames, end="\r")
    """if totalFrames>15 :
      break"""

    
print("Frame:", totalFrames)
# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# if we are not using a video file, stop the camera video stream
if not args.get("input", False):
    vs.stop()

# otherwise, release the video file pointer
else:
    vs.release()

