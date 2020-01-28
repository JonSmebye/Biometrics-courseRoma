import face_recognition
from imutils.video import VideoStream
import cv2
import time
import os

def getImageFromWebcam():
	cam = VideoStream(src=0).start()
	time.sleep(0.5)
	image = cam.read()
	cv2.destroyAllWindows()
	cam.stop()
	return image

def faceRecognition(imgPath, img):
	known_image = face_recognition.load_image_file(imgPath)
	unkown_image = img
	know_encoding = face_recognition.face_encodings(known_image)[0]
	unkwnown_encoding = face_recognition.face_encodings(unkown_image)[0]
	results = face_recognition.compare_faces([know_encoding],unkwnown_encoding)
	return results[0]

def takePictureAsRefferance():
	image = getImageFromWebcam()
	filePath = "refe.jpg"
	cv2.imwrite(filePath, image)
	return filePath

def menu():
	ans=True
	while ans:
		print ("""
	1.Take referance picture now
	2.Use an existing photo
			""")
		ans=input("What would you like to do? ") 
		if ans=="1":
			print("\nTaking a picture now")
			imagePath = takePictureAsRefferance()
			ans = False
		elif ans=="2":
			imagePath = input("What is the entire filepath of the picture?")
			ans = False
		else:
			print("\nNot Valid Choice Try again")
	return imagePath


def main():
	imagePathStored = menu()
	notRecognized = 0
	while True:
		img = getImageFromWebcam()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_front_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		faces_front = face_front_cascade.detectMultiScale(gray, 1.3, 5)
		cv2.destroyAllWindows()
		try:
			faces_front.all()
			res = faceRecognition(imagePathStored, img)
			if res != True:
				print("Unauthorized subject detected")
				notRecognized += 1
				if notRecognized > 2:
					user = os.popen('whoami').read()
					cmd = 'launchctl bootout gui/$(id -u "'+user.strip('\n')+ '")'
					os.system(cmd)
			else:
				print("Autorized subject detected")
				notRecognized = 0
		except:
			print("No faces detected")
		time.sleep(2.0)

if __name__ == '__main__':
    main()


