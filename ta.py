#inisialisasi pin dan kelas yang akan digunakan
import time, string, argparse, cv2, os, playsound, serial
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from pygame import mixer # Load the required library


# class deteksi objek
class ObjectDetection():
	__image = "test.jpg"

	def __init__(self,img):
		self.__image = img

	def identifikasi(self):

		CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "Mobil", "cat", "Kursi", "cow", "diningtable",
			"dog", "horse", "Sepeda Motor", "Manusia", "pottedplant", "sheep",
			"sofa", "train", "tvmonitor"]
		COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

		print("[INFO] loading model...")
		net = cv2.dnn.readNetFromCaffe("proto.txt", "model.caffemodel")
		try:
			image = cv2.imread(self.__image)
			(h, w) = image.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
			print("[info] computing object detections....")
			net.setInput(blob)
			detections = net.forward()

			#loop over the detections
			for i in np.arange(0, detections.shape[2]):
				# extract the confidence (i.e., probability) associated with the
			    # prediction
				confidence = detections[0, 0, i, 2]

				if confidence > args["confidence"]:
					idx = int(detections[0,0,i,1])
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")


					#display the prediction
					label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
					label1 = "{}".format(CLASSES[idx])
					print("[INFO] {}".format(label))
					cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)

					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

					# menampilkan hasil
					# cv2.imshow("output",image)
					# cv2.waitKey(0)
					#print("cek hasil string: ",result[0:7])


					return label1

		except Exception as e:
			print("[EROR] Gambar Tidak Teridentifikasi")
			return None

# ======== Akhir kelas objek detection==================

#===== deteksi Lubang
class Lubang():
	__image = "test.jpg"

	def __init__(self,img):
		self.__image = img

	def identifikasi(self):
		gray = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)

		# threshold the image, then perform a series of erosions +
		# dilations to remove any small regions of noise
		thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)[1]
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)
		#cv2.imshow("Image",thresh)

		# find contours in thresholded image, then grab the largest one

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		c = max(cnts, key=cv2.contourArea)

		# determine the most extreme points along the contour
		extLeft = tuple(c[c[:, :, 0].argmin()][0])
		extRight = tuple(c[c[:, :, 0].argmax()][0])
		extTop = tuple(c[c[:, :, 1].argmin()][0])
		extBot = tuple(c[c[:, :, 1].argmax()][0])

		# draw the outline of the object, then draw each of the
		# extreme points, where the left-most is red, right-most
		# is green, top-most is blue, and bottom-most is teal
		cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
		cv2.circle(image, extLeft, 6, (0, 0, 255), -1)
		cv2.circle(image, extRight, 6, (0, 255, 0), -1)
		cv2.circle(image, extTop, 6, (255, 0, 0), -1)
		cv2.circle(image, extBot, 6, (255, 255, 0), -1)
		cv2.imwrite('image/result/Lubang.jpg', image)

		return 



#=========== ini adalah main program =============
print("=="*10)
print("Sistem Berjalan")
print("=="*10)




ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.8,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
#clas capture Gambar




while True:
	try:
		# pembacaan nilai serial
		try:
			ser = serial.Serial('/dev/ttyUSB0', 9600)
			output =int(ser.readline())
			print("/dev/ttyUSB0")
			print("Distance Measuring: ", output)
		except Exception as e:
			ser = serial.Serial('/dev/ttyUSB1', 9600)
			print("/dev/ttyUSB1")
			output =int(ser.readline())
			print("Distance Measuring: ", output)


		time.sleep(1)

		if output >= 100:
			print("Jarak Aman")
		elif output <= 100:
			print("bahaya")

			time.sleep(1)

			# capture = Capture()
			# takePic = capture.takePic(output)
			#print(takePic)
            #rotateImg = capture.rotate()
			#proses ambil gambar
			camera.capture(rawCapture, format="bgr")
			image = rawCapture.array

			#proses simpan gambar
			cv2.imwrite("image/capture/result.jpg",image)
			img = cv2.imread('image/capture/result.jpg')
			h,w = img.shape[:2]
			center = (w/2,h/2)

			#proses rotasi gambar
			rotate = cv2.getRotationMatrix2D(center,360-90,1)

			rotatingImg = cv2.warpAffine(img,rotate,(w,h))
			cv2.imwrite('image/result/result_rotate.jpg', rotatingImg)
			check = ObjectDetection("image/result/result_rotate.jpg")
			if check is None:
				print("Objek Tidak Teridentifikasi")
				continue
			else:
				try:
					result = check.identifikasi()
					print(result)
					#print("cek hasil string: ",result[0:7])
					if  result is "Manusia":
						print("manusia terdeteksi")
						mixer.init()
						mixer.music.load('musik/manusia.mp3')
						mixer.music.play()
						time.sleep(6)
					elif result is "Sepeda Motor":
						print("motor terdeteksi")
						mixer.init()
						mixer.music.load('musik/motor.mp3')
						mixer.music.play()
						time.sleep(7)
					elif result is "Mobil":
						print("mobil terdeteksi")
						mixer.init()
						mixer.music.load('musik/mobil.mp3')
						mixer.music.play()
						time.sleep(6)
					elif "Kursi" is result:
						print("kursi terdeteksi")
						mixer.init()
						mixer.music.load('musik/kursi.mp3')
						mixer.music.play()
						time.sleep(7)
					elif "none" is result:
						print("identifikasi Lubang")
						resut = Lubang("image/result/result_rotate.jpg")
						mixer.init()
						mixer.music.load('musik/lubang.mp3')
						mixer.music.play()
						time.sleep(5)




					print("hasil uji: ",result)

				except Exception as e:
					print("=="*10)
					print("[Info] Eror System deteksi")
					print("eror",e)
					print("=="*10)


			rawCapture.truncate(0)

            #os.remove("user.jpg")
			print("=="*10)

	except KeyboardInterrupt:
		print('keluar dari program')
		break
