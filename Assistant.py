# from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from pyHS100 import SmartPlug
from phue import Bridge
from gtts import gTTS
import datetime as dt
from ahk import AHK
import threading
import playsound
import json
import os
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

class Assistant:

    def __init__(self, assistant_name, user_name, user_nickname):
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.assistant_name = assistant_name
        self.user_name = user_name
        self.user_nickname = user_nickname
        self.voice_response = self.phrase_data['settings']['voice_response']
        self.text_response = self.phrase_data['settings']['text_response']
        self.debug = self.phrase_data['settings']['debug']
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.Lighthouse = SmartPlug('192.168.0.196')
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    def Speak(self, text):
        '''Using gTTS, verbally says the text variable with Text-To_Speech '''
        # TODO Add threading
        def text_to_speech(text):
            tts = gTTS(text=text, lang='en')
            date_string = dt.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = f'voice{date_string}.mp3'
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        thread = threading.Thread(target=text_to_speech(text))
        thread.start()


    # TODO Add Voice Recongition
    # def get_audio():
    # 	r = sr.Recognizer()
    # 	with sr.Microphone() as source:
    # 		audio = r.listen(source)
    # 		said = ""

    # 		try:
    # 		    said = r.recognize_google(audio)
    # 		    print(said)
    # 		except Exception as e:
    # 		    print("Exception: " + str(e))
    # 	return said.lower()


    def Simplify_Phrase(self, sentence):
        '''ph'''
        with open("stopwords.txt", "r") as f:
            stopwords = f.read()
        stemmer = LancasterStemmer()
        sentence = stemmer.stem(sentence.lower())
        # stop_words = set(stopwords.words('english'))
        stop_words = set(stopwords)
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        return filtered_sentence


    def Install_nltk_data(self):
	    # nltk.download('stopwords')
        pass


    def Time_Till(self, subject, month, day, year):
        time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        text = f'{subject} is out in {time_till.days} days.'
        self.Speak(text)
        print(text)


    def Toggle_Heater(self):
        pass


    def Set_Volume(self, level):
        pass


    def Roku(self, action):
        pass
