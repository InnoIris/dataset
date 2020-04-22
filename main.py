import argparse
from video2img import FrameCapture
from tracker import Tracker

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=False, help="Path for the image", default=0)
ap.add_argument("-t", "--thres", required=False, type=float, default=500.0) # Threshold is very scene dependent. Make sure to specify one
args = vars(ap.parse_args())

tracker = Tracker()

def trackerCallback(frame):
  image = tracker.callback(frame)
  return image

FrameCapture(args["path"], args["thres"], [trackerCallback])