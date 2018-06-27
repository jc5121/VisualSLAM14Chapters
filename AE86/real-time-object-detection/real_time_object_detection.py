#!/usr/bin/env python3

# USAGE
# python real_time_object_detection.py 

# import the necessary packages
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy
import numpy as np
import argparse
import imutils
import time
import cv2
import pygame

#initialize the music play mode 
pygame.mixer.init() 
pygame.mixer.music.load("hey.mp3")

def play_sounds():  
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# CLASSES = ["person"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

def callback(ros_image):
	#frame = vs.read()
	bridge = CvBridge()
	try:
		img = bridge.imgmsg_to_cv2(ros_image, "bgr8")
	except CvBridgeError:
		print(CvBridgeError)
	frame = img
	frame = imutils.resize(frame, width=400)

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > 0.2:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			if idx == 15:  # person
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)
				print("hey")
				play_sounds()
				
			#y = startY - 15 if startY - 15 > 15 else startY + 15
			#cv2.putText(frame, label, (startX, y),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	
rospy.init_node('detection_listener', anonymous=True)
rospy.Subscriber("/camera/rgb/image_raw", Image, callback)
rospy.spin()

# do a bit of cleanup
cv2.destroyAllWindows()

