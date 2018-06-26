# USAGE
# python build_face_dataset.py --cascade haarcascade_frontalface_default.xml --output dataset/adrian

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--cascade", required=True,	help = "path to where the face cascade resides")
#ap.add_argument("-o", "--output", required=True,	help="path to output directory")
#args = vars(ap.parse_args())

# load OpenCV's Haar cascade for face detection from disk
#detector = cv2.CascadeClassifier(args["cascade"])
detector = cv2.CascadeClassifier("/home/jhonex/Documents/project_enroll/haarcascade_frontalface_default.xml")


# initialize the video stream, allow the camera sensor to warm up,
# and initialize the total number of example faces written to disk
# thus far
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 1
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, clone it, (just
	# in case we want to write it to disk), and then resize the frame
	# so we can apply face detection faster
	frame = vs.read()
	orig = frame.copy()
	frame = imutils.resize(frame, width=400)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30))

	# loop over the face detections and draw them on the frame
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `k` key was pressed, write the *original* frame to disk
	# so we can later process it and use it for face recognition
	if total <= 500:
		
		p = os.path.sep.join(["dataset/jhon", "{}.png".format(
			str(total).zfill(5))])
		cv2.imwrite(p, orig)
		#p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(5))])
		
		total += 1
	else:
		print("fin")
		break
	# if the `q` key was pressed, break from the loop
	#elif key == ord("q"):
	#	break

# do a bit of cleanup
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()