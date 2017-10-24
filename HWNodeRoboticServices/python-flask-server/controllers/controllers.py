from gtts import gTTS
import os
from RappCloud import RappPlatformAPI
from PIL import Image
import unirest
import zbar
from pytesseract import image_to_string
import numpy as np
import cv2
import wave
import Image
import angus
import Image_
import Algorithmia
import json
import base64
import zlib
import subprocess
from flask import abort

addr = None 		# addr = 'localhost'  OR   addr = None (for Rapp Server)
# library RappCloud has no attribute addr in my PC. It works only at RPi

MashapeKey = "IamijJzmI8mshgm0aWB8EPOqXEd2p1Jx2I7jsnDa13HpU9eK7N"
###Paths at PC
image_path = '/home/panos/Desktop/Swagger/finalTest/test_v5/'     #path to save the image
RAPPtext2speech_full_path = '/home/panos/Desktop/Swagger/finalTest/test_v5/sound.mp3'
#OpenCV path to cascades
face_cascade_path = '/home/panos/Desktop/Thesis/OpenCV/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
eye_cascade_path = '/home/panos/Desktop/Thesis/OpenCV/opencv/data/haarcascades/haarcascade_eye.xml'
smile_cascade_path = '/home/panos/Desktop/Thesis/OpenCV/opencv/data/haarcascades/haarcascade_smile.xml'
body_cascade_path = '/home/panos/Desktop/Thesis/OpenCV/opencv/data/haarcascades/haarcascade_fullbody.xml'

#PATHS at RPi
#image_path = '../files/'
#RAPPtext2speech_full_path = '../files/sound.wav'
#face_cascade_path = '../../openCV/haarcascades/haarcascade_frontalface_default.xml'
#eye_cascade_path = '../../openCV/haarcascades/haarcascade_eye.xml'
#smile_cascade_path = '../../openCV/haarcascades/haarcascade_smile.xml'
#body_cascade_path = '../../openCV/haarcascades/haarcascade_fullbody.xml'

class Controller(object):
	def __init__(self):
			pass

	########### Algorithmia Services  ##############
	def AlgoDeepAgeDetection(self, apiKey, imageString, image):

		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('deeplearning/AgeClassification/2.0.0')  # determine which service to call

		# Uploads image to Algorithmia's DataBase using function UploadToAlgorithmia
		#The function also uses another function (str2img) to convert string to image if it is needed.
		UploadToAlgorithmia(client, imageString, image)

		input = {"image": "data://PanosDoxopoulos/nlp_directory/image.jpg"}	#Use path of image in Algorithmia databases
		response = algo.pipe(input)		#call service
		return response.result

	def AlgoDeepGenderDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('deeplearning/GenderClassification/2.0.0')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = {"image": "data://PanosDoxopoulos/nlp_directory/image.jpg"}
		response = algo.pipe(input)		#call service
		return response.result

	def AlgoDeepObjectDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('deeplearning/CaffeNet/2.0.1')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = {"image": "data://PanosDoxopoulos/nlp_directory/image.jpg"}
		response = algo.pipe(input)		#call service
		return response.result

	def AlgoDlibFaceDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('dlib/FaceDetection/0.2.0')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = {"images": [{"url": "data://PanosDoxopoulos/nlp_directory/image.jpg"}]}
		response = algo.pipe(input)		#call service
		return response.result

	def AlgoOCR(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('ocr/RecognizeCharacters/0.3.0')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = "data://PanosDoxopoulos/nlp_directory/image.jpg"
		response = algo.pipe(input)		#call service
		return response.result

	def AlgoOpenCvBodyDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('opencv/BodyDetection/1.0.0')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = {"imageUrl":"data://PanosDoxopoulos/nlp_directory/image.jpg", "outputUrl":"data://PanosDoxopoulos/nlp_directory/result.jpg"}
		algo.pipe(input)		#call service
		response = client.file("data://PanosDoxopoulos/nlp_directory/result.jpgrects.txt").getString()
		print response
		return response

	def AlgoOpenCvEyesDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('opencv/EyeDetection/0.1.1')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = ["data://PanosDoxopoulos/nlp_directory/image.jpg", "data://PanosDoxopoulos/nlp_directory/result.jpg"]
		algo.pipe(input)		#call service
		response = client.file("data://PanosDoxopoulos/nlp_directory/result.jpgrects.txt").getString() # read the response from the file
		print response
		return response

	def AlgoOpenCvFaceDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('opencv/FaceDetection/0.1.8')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = ["data://PanosDoxopoulos/nlp_directory/image.jpg", "data://PanosDoxopoulos/nlp_directory/result.jpg"]
		algo.pipe(input)		#call service
		response = client.file("data://PanosDoxopoulos/nlp_directory/result.jpgrects.txt").getString()
		return response

	def AlgoOpenCvSmileDetection(self, apiKey, imageString, image):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('opencv/SmileDetection/0.1.0')  # determine which service to call

		UploadToAlgorithmia(client, imageString, image)

		input = ["data://PanosDoxopoulos/nlp_directory/image.jpg"]
		algo.pipe(input)		#call service
		response = client.file("data://PanosDoxopoulos/nlp_directory/.algo/temp/img.jpgrects.txt").getString()
		return response

	def AlgoSentiment(self, text, apiKey):
		client = Algorithmia.client(apiKey) 	#authorization
		algo = client.algo('nlp/SentimentAnalysis/1.0.3')  # determine which service to call
		input = {"document": text}		#<text> format need to be: {text = "document": 'your text'}
		response = algo.pipe(input)
		return response.result

	############# Angus Services  ################
	def AngusExpression(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		conn = angus.connect()		#connection
		service = conn.services.get_service('face_expression_estimation', version=1)	# determine which service to call
		job = service.process({'image': open(path, 'rb')})	#call service
		response = job.result
		return response

	def AngusGender(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		conn = angus.connect() 		#connection
		service = conn.services.get_service("age_and_gender_estimation", version=1) # determine which service to call
		job = service.process({'image': open(path, 'rb')})	#call service
		response = job.result
		return response

	def AngusText2Sound(self, text, lang):
		def decode_output(sound, filename):
			sound = base64.b64decode(sound)
			sound = zlib.decompress(sound)
			with open(filename, "wb") as f:
					f.write(sound)
		conn = angus.connect()
		service = conn.services.get_service('text_to_speech', version=1)
		job = service.process({'text': text, 'lang' : lang})
		decode_output(job.result["sound"], "angusSound.mp3")
		f1 = open("angusSound.mp3","r")
		return f1

	############# Google Service  ################
	def gtts(self, text, lang):
		tts = gTTS(text=text, lang=lang) 	#text2sound function
		tts.save("newfile.mp3")  		#save to mp3 file
		#f = open('newfile.mp3','r')		#It is a file. It is NOT JSON serializable.
		f = open("newfile.mp3").read()		#It is an array of values. It is serializable.
		return f

	############# Mashape Services  ################
	def MashapeBreakingNews(self):
		url = "https://myallies-breaking-news-v1.p.mashape.com/news"
		headers={"X-Mashape-Key": MashapeKey, "Accept":"application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeBreakingNewsSymbol(self, symbol):
		url = "https://myallies-breaking-news-v1.p.mashape.com/news/"
		url += symbol
		headers={"X-Mashape-Key": MashapeKey, "Accept": "application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeFaceRect(self, features, imageString , image):

		path = imageORimageString(imageString, image)
		url = "https://apicloud-facerect.p.mashape.com/process-file.json"
		response = unirest.post(url, headers = {'X-Mashape-Key' : MashapeKey}, params = {'features' : features, 'image' : open(path, mode = "r")})
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeLanguageIdentification(self, text):
		url = "https://systran-systran-platform-for-language-processing-v1.p.mashape.com/nlp/lid/detectLanguage/document?input="
		url += text
		headers={"X-Mashape-Key": MashapeKey, "Accept": "application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeNameEntities(self, text, lang):
		url = "https://systran-systran-platform-for-language-processing-v1.p.mashape.com/nlp/ner/extract/entities?input="
		url += text
		url += "&lang="
		url += lang
		headers={"X-Mashape-Key": MashapeKey, "Accept": "application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeNewsAlyze(self, url):
		new_url = "https://newsalyze.p.mashape.com/article?url="
		new_url += url
		headers={"X-Mashape-Key": MashapeKey, "Accept": "text/plain"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeReminders(self, phrase, timezone):
		url = "https://maciejgorny-reminderdrop-v1.p.mashape.com/"
		url += phrase
		url = url + phrase + "/" + timezone
		headers={"X-Mashape-Key": MashapeKey, "Accept": "application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeSentiment(self, txt):
		url = "https://community-sentiment.p.mashape.com/text/"
		headers={"X-Mashape-Key": MashapeKey, "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
		params={"txt": txt}
		response = unirest.post(url, headers = headers, params = params)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeTranslate(self, text, source, target):
		#Systran.io
		url = "https://systran-systran-platform-for-language-processing-v1.p.mashape.com/translation/text/translate?source="
		url = url + source + "&target=" + target + "&input=" + text
		headers={"X-Mashape-Key": MashapeKey, "Accept": "application/json"}
		response = unirest.get(url, headers = headers)
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	def MashapeWeather(self, lat, lng):
		url = 'https://simple-weather.p.mashape.com/weather'
		url+='?lat='
		url+=str(lat)
		url+='&lng='
		url+=str(lng)
		response = unirest.get(url, headers = {'X-Mashape-Key' : MashapeKey, 'accept' : "text/plain"})
		if response.code is not 200:
			abort(response.code, response.body)
		return response.body

	############# OpenCV Services  ################
	def OpenCvFaceDetection(self, imageString, image, eyeDetection, smileDetection):

		path = imageORimageString(imageString, image) #path of saved image.

		###  classifiers  ###
		face_cascade = cv2.CascadeClassifier(face_cascade_path)
		eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
		smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
		body_cascade = cv2.CascadeClassifier(body_cascade_path)

		img = cv2.imread(path)

		####### Face Detection
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		FaceCounter=0
		data ={}
		for (x,y,w,h) in faces:
			data[FaceCounter] = {
				"face{0}".format(FaceCounter):
					{
					"up_left_point": {"x":x,"y":y},
					"width": w,
					"height": h
					}
			}

			####### Eye Detection
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			EyeCounter = 0
			data1={}

			if eyeDetection:
				for (ex,ey,ew,eh) in eyes:
					EyeCounter += 1
					data1[EyeCounter] = {
						"eye{0}".format(EyeCounter):
							{
							"up_left_point": {"x":x+ex,"y":y+ey},
							"width": ew,
							"height": eh
							}
						}
			if EyeCounter == 1:
				eye1 = data1[1]
				data[FaceCounter].update(eye1)
				eye2 = 'Eye could not be detected'
			elif EyeCounter == 2:
				eye1 = data1[1]
				eye2 = data1[2]
				data[FaceCounter].update(eye1)
				data[FaceCounter].update(eye2)
			else:
				eye1 = 'Eye could not be detected'
				eye2 = 'Eye could not be detected'


			####### Smile Detection
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			smile = smile_cascade.detectMultiScale(roi_gray)
			SmileCounter = 0
			data2={}
			print smile
			if smileDetection:
				for (sx,sy,sw,sh) in smile:
					SmileCounter += 1
					data2 = {
						"smile":
							{
							"up_left_point": {"x":x+sx,"y":y+sy},
							"width": sw,
							"height": sh
							}
					}
				if SmileCounter == 1:
					smile = data2
					data[FaceCounter].update(smile)
				else:
					smile = 'Smile could not be detected'

			FaceCounter+=1

		print data
		#cv2.imwrite('resultImage.jpg',img) #save image
		#f = open('resultImage.jpg', "r")
		#response = f.read()
		return data

	def OpenCvBodyDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		body_cascade = cv2.CascadeClassifier(body_cascade_path)
		img = cv2.imread(path)

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		body = body_cascade.detectMultiScale(gray, 1.3, 5)
		Counter=0
		data ={}
		print 'one'
		print body
		for (bx,by,bw,bh) in body:
			print 'one'
			print(bx,by,bh,bw)
			data[Counter] = {
				"body{0}".format(Counter):
					{
					"up_left_point": {"x":bx,"y":by},
					"width": bw,
					"height": bh
					}
			}
			Counter+=1

		return data

	def OpenCvEyesDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		###  classifier  ###
		eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
		img = cv2.imread(path)

		####### Smile Detection
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		eye = eye_cascade.detectMultiScale(gray)
		print eye
		response = json.dumps(eye.tolist())  	#JSON serialization
		return response			##################### SOS  #USUALLY THE LAST ARRAY IS RUBBISH (MAYBE ALWAYS) -- CHECK AGAIN

	def OpenCvSmileDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		###  classifier  ###
		smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
		img = cv2.imread(path)

		####### Smile Detection
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		smile = smile_cascade.detectMultiScale(gray, 1.3, 14)			#scale, minNeighbors
		print smile
		response = json.dumps(smile.tolist())
		return response

	############# Rapp Services  ################
	def RappFaceDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI(address = addr)
		response = ch.faceDetection(path) # Use the server's path of the image.
		return response

	def RappGeolocation(self, IP):
		#sys.path.append('../../../Thesis/rapp_portable/rapp-api/python')
		ch = RappPlatformAPI() #address = addr
		response = ch.geolocation(IP)
		if response.get('error') is not "":
			abort(500, response.get('error'))
		return response

	def RappQrDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI()		###############address = addr
		response = ch.qrDetection(path) # Use the server's path of the image.
		if not response.get('error') == "":
			abort(500, response.get('error'))
		return response

	def RappHumanDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI(address = addr)
		response = ch.humanDetection(path) # Use the server's path of the image.
		return response

	def RappFaceDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI(address = addr)
		response = ch.faceDetection(path) # Use the server's path of the image.
		return response

	def RappWeatherCurrent(self, city, weatherReporter, metric):

		ch = RappPlatformAPI()  #########address = addr
		response = ch.weatherReportCurrent(city, weatherReporter, metric)
		return response

	def RappWeatherForecast(self, city, weather_reporter, metric):
		ch = RappPlatformAPI() ######################address = addr
		response = ch.weatherReportForecast(city, weather_reporter, metric) #Rapp service
		return response

	def RappDoorDetection(self, imageString, image):
		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI()#################address = addr
		#im=Image.open(image)
		#im.save("/home/panos/Desktop/Swagger/finalTest/test_v5/Door.png","PNG", progressive = True)  #Path to save the image on 	the server.
		### deinterlacing #
		#size=list(im.size)
		#size[0] /= 2
		#size[1] /= 2
		#downsized=im.resize(self, size, Image.NEAREST) # NEAREST drops the lines
		#downsized.save("/home/panos/Desktop/Swagger/finalTest/test_v5/Door.png")
		#######
		response = ch.hazardDetectionDoor(path) # Use the server's path of the 	image.
		return response

	def RappLightDetection(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI(address = addr)
		response = ch.hazardDetectionLights(path) # Use the server's path of 	the image.
		return response

	def RappObjectRecCaffe(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		ch = RappPlatformAPI(address = addr)
		response = ch.objectRecognitionCaffe(path) # Use the server's path 	of the image.
		return response

	def RappSpeechDetectionGoogle(self, audioString, audioFile, language, audioSource):

		path = audioFileORaudioString(audioString, audioFile)
		ch = RappPlatformAPI() ###address = addr
		response = ch.speechRecognitionGoogle(path, audioSource, language)
		return response

	def RappSpeechDetectionSphinx(self, audioString, audioFile, language, audioSource, words = None, sentences = None, grammar = None):

		path = audioFileORaudioString(audioString, audioFile)
		ch = RappPlatformAPI(address = addr)
		response = ch.speechRecognitionSphinx(path, language = language, audio_source = audioSource, words = words, sentences = sentences, grammar = grammar)
		#f=open('/home/panos/Desktop/Swagger/finalTest/test_v3/RappGoogle.wav','r')
		return response

	def RappText2Speech(self, text, language ):
		ch = RappPlatformAPI(address = addr)
		response = ch.textToSpeech(text, language, RAPPtext2speech_full_path)
		f=open(RAPPtext2speech_full_path,'r')   #at RPi: f = open(RAPPtext2speech_full_path).read()  #serializable
		return f

	############# Tesseract Service  ################
	def Tesseract(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.
		# running tessaract OCR function
		response = image_to_string(Image.open(path))
		return response

	############# Zbar Service  ################
	def Zbar(self, imageString, image):

		path = imageORimageString(imageString, image) #path of saved image.

		#create a reader
		scanner = zbar.ImageScanner()

		#configure the reader
		scanner.parse_config('enable')

		#obtain image data
		im = Image.open(path).convert('L')
		width, height = im.size
		raw = im.tostring()		####################tobytes() to RPi

		#wrap image data
		image = zbar.Image(width, height, 'Y800', raw)

		#scan image for barcodes
		scanner.scan(image)

		for symbol in image:
			response = symbol.data
		return response



############################### functions  ###################################

#Function str2img. Convert base64 to image, using file Image_.py
def str2img(imageString):
	img = Image_.Image(charbuffer = imageString, base64 = True)
	img.load_from_base64(imageString)
	path = image_path + 'image.jpg'
	img.save(path)  #img.save("base64.jpg")
	img.clear()

#Function str2audio. Convert base64 to audio, using file Image_.py
def str2audio(audioString):
	audio = Image_.Image(charbuffer = audioString, base64 = True)
	audio.load_from_base64(audioString)
	audio.save("audio.mp3")
	audio.clear()

def UploadToAlgorithmia(client, imageString, image):
	path = imageORimageString(imageString, image) #path of saved image.
	imagefile = "data://PanosDoxopoulos/nlp_directory/image.jpg"		#path to Algorithmia databases
	client.file(imagefile).putFile(path)

#function imageORimageString. Check which parameter is given.
def imageORimageString(imageString, image):
	if imageString is not None:
		str2img(imageString = imageString)  #convert base64 to image and save it, locally.
		path = image_path + 'image.jpg'
	elif image is not None:
		im=Image.open(image)
		path = image_path + "image.jpg"
		im.save(path, "JPEG") #save image
	else:
		abort(400, 'Bad Request. Please give one of the parameters: image or imageString')  #Bad Request. Raise an error if there is no image or imageString.
	return path  #Return the path of the saved image

#function imageORimageString. Check which parameter is given.
def audioFileORaudioString(audioString, audioFile):
	if audioString is not None:
		str2audio(audioString = audioString)  #convert base64 to audio and save it, locally.
		path = image_path + 'audio.mp3'
	elif audioFile is not None:
		path = image_path + 'audio.mp3'
		#save audio file locally
		with open(path, "wb") as f1:
			f1.write(audioFile.stream.read())
	else:
		abort(400, 'Bad Request. Please give one of the parameters: audioFile or audioString')  #Bad Request. Raise an error.
	return path  #Return the path of the saved audio file
