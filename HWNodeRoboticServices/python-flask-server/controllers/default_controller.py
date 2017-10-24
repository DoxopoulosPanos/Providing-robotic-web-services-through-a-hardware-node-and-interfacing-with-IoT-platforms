from controllers import Controller
controller = Controller()

########### Algorithmia Services  ##############
def algorithmia_deep_learning_age_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoDeepAgeDetection(apiKey, imageString, image)
    return response

def algorithmia_deep_learning_gender_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoDeepGenderDetection(apiKey, imageString, image)
    return response

def algorithmia_deep_learning_object_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoDeepObjectDetection(apiKey, imageString, image)
    return response

def algorithmia_dlib_face_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoDlibFaceDetection(apiKey, imageString, image)
    return response

def algorithmia_ocr(apiKey, imageString = None, image = None):
    response = controller.AlgoOCR(apiKey, imageString, image)
    return response

def algorithmia_open_cv_body_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoOpenCvBodyDetection(apiKey, imageString, image)
    return response

def algorithmia_open_cv_eyes_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoOpenCvEyesDetection(apiKey, imageString, image)
    return response

def algorithmia_open_cv_face_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoOpenCvFaceDetection(apiKey, imageString, image)
    return response

def algorithmia_open_cv_smile_detection(apiKey, imageString = None, image = None):
    response = controller.AlgoOpenCvSmileDetection(apiKey, imageString, image)
    return response

def algorithmia_sentiment(text, apiKey):
    response = controller.AlgoSentiment(text, apiKey)
    return response

########### Angus Services  ##############
def angus_expression(imageString = None, image = None):
    response = controller.AngusExpression(imageString, image)
    return response

def angus_gender(imageString = None, image = None):
    response = controller.AngusGender(imageString, image)
    return response

def angus_text2_sound(text, lang = None):
    response = controller.AngusText2Sound(text, lang)
    return response

########### Google Service  ##############
def g_tts(text, lang):
    response = controller.gtts(text,lang)
    return response

########### Mashape Services  ##############
def mashape_breaking_news():
    response = controller.MashapeBreakingNews()
    return response

def mashape_breaking_news_symbol(symbol):
    response = controller.MashapeBreakingNewsSymbol(symbol)
    return response

def mashape_face_rect(features = None, imageString = None, image = None):
    response = controller.MashapeFaceRect(features, imageString, image)
    return response

def mashape_language_identification_api(text):
    response = controller.MashapeLanguageIdentification(text)
    return response

def mashape_name_entities_api(text, lang):
    response = controller.MashapeNameEntities(text, lang)
    return response

def mashape_newsalyze(url):
    response = controller.MashapeNewsAlyze(url)
    return response

def mashape_reminders_nlpapi(phrase, timezone = None):
    response = controller.MashapeReminders(phrase, timezone)
    return response

def mashape_sentiment_api(txt):
    response = controller.MashapeSentiment(txt)
    return response

def mashape_translate_api(text, target, source = None):
    response = controller.MashapeTranslate(text, source, target)
    return response

def mashape_weather_api(lat = None, lng = None):
    response = controller.MashapeWeather(lat, lng)
    return response

########### OpenCV Services  ##############
def open_cv_face_detection(imageString = None, image = None, eyeDetection = None, smileDetection = None):
    response = controller.OpenCvFaceDetection(imageString, image, eyeDetection, smileDetection)
    return response

def open_cv_body_detection(imageString = None, image = None):
    response = controller.OpenCvBodyDetection(imageString, image)
    return response

def open_cv_eyes_detection(imageString = None, image = None):
    response = controller.OpenCvEyesDetection(imageString, image)
    return response

def open_cv_smile_detection(imageString = None, image = None):
    response = controller.OpenCvSmileDetection(imageString, image)
    return response

########### Rapp Services  ##############
def rapp_door_detection(imageString = None, image = None):
    response = controller.RappDoorDetection(imageString, image)
    return response

def rapp_face_detection(imageString = None, image = None):
    response = controller.RappFaceDetection(imageString = imageString, image = None)
    return response

def rapp_geolocation(ip):
    response = controller.RappGeolocation(ip)
    return response

def rapp_human_detection(imageString = None, image = None):
    response = controller.RappHumanDetection(imageString, image)
    return response

def rapp_light_detection(imageString = None, image = None):
    response = controller.RappLightDetection(imageString, image)
    return response

def rapp_object_rec_caffe(imageString = None, image = None):
    response = controller.RappObjectRecCaffe(imageString, image)
    return response

def rapp_qr_detection(imageString = None, image = None):
    response = controller.RappQrDetection(imageString, image)
    return response

def rapp_speech_detection_google(audioString = None, audioFile = None, language = None, audioSource = None):
    response = controller.RappSpeechDetectionGoogle(audioString, audioFile, language, audioSource)
    return response

def rapp_speech_detection_sphinx(audioString = None, audioFile = None, language = None, audioSource = None, words = None, sentences = None, grammar = None):
    response = controller.RappSpeechDetectionSphinx(audioString, audioFile, language, audioSource, words, sentences, grammar)
    return response

def rapp_text2_speech(text, language = None):
    response = controller.RappText2Speech(text, language)
    return response

def rapp_weather_current(city, weatherReporter = None, metric = None):
    response = controller.RappWeatherCurrent(city, weatherReporter, metric)
    return response

def rapp_weather_forecast(city, weatherReporter = None, metric = None):
    response = controller.RappWeatherForecast(city, weatherReporter, metric)
    return response

########### Tesseract Service  ##############
def tesseract(imageString = None, image = None):
    response = controller.Tesseract(imageString, image)
    return response

############   zbar Service   ###############
def zbar(imageString = None, image = None):
    response = controller.Zbar(imageString, image)
    return response
