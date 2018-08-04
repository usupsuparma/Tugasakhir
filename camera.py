
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1080, 720)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1080, 720))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("c"):
		cv2.imwrite("result.jpg", image)
		img = cv2.imread('result.jpg')
		h,w = img.shape[:2]
		center = (w/2,h/2)
		rotate = cv2.getRotationMatrix2D(center,360-90,1)

		rotatingImg = cv2.warpAffine(img,rotate,(w,h))
		cv2.imshow('Rotating', rotatingImg)
		cv2.imwrite('hasilrotate.jpg', rotatingImg)

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
