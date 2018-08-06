import serial
import time, string, argparse, cv2, os, playsound
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


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
					print("[INFO] {}".format(label))
					cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)

					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

					# menampilkan hasil
					cv2.imshow("output",image)
					cv2.waitKey(0)

					return label

		except Exception as e:
			print("[EROR] Gambar Tidak Teridentifikasi")
			return None

# ======== Akhir kelas objek detection==================


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
		ser = serial.Serial('/dev/ttyUSB0', 9600)
		output =int(ser.readline())
		print("nilai keluar: ", output)

		time.sleep(1)

		if output >= 50:
			print("Jarak Aman")
		elif output <= 50:
			print("bahaya")

			time.sleep(1)

			# capture = Capture()
			# takePic = capture.takePic(output)
			#print(takePic)
            #rotateImg = capture.rotate()
			camera.capture(rawCapture, format="bgr")
			image = rawCapture.array
			cv2.imwrite("result.jpg",image)
			img = cv2.imread('result.jpg')
			h,w = img.shape[:2]
			center = (w/2,h/2)
			rotate = cv2.getRotationMatrix2D(center,360-90,1)

			rotatingImg = cv2.warpAffine(img,rotate,(w,h))
			cv2.imwrite('result_rotate.jpg', rotatingImg)
			check = ObjectDetection("result_rotate.jpg")
			if check is None:
				print("Objek Tidak Teridentifikasi")
				continue
			else:
				try:
					result = check.identifikasi()
					print("cek hasil string: ",result[0:6])
					if result[0:6] == "Manusia":
						print("manusia terdeteksi")
						playsound.playsound('musik/manusia.mp3')
					elif result[0:9] == "Sepeda Motor":
						print("motor terdeteksi")
						playsound.playsound('musik/motor.mp3')
					elif result[0:3] == "Mobil":
						print("mobil terdeteksi")
						playsound.playsound('musik/mobil.mp3')
					elif result[0:4] == "Kursi":
						print("kursi terdeteksi")
						playsound.playsound('musik/kursi.mp3')

					print("hasil uji: ",result)

				except Exception as e:
					print("=="*10)
					print("[Info] Gambar Tidak Teridentifikasi")


			rawCapture.truncate(0)

            #os.remove("user.jpg")
			print("=="*10)

	except KeyboardInterrupt:
		print('keluar dari program')
		break
