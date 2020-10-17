from Assistant import Assistant
import speech_recognition as sr
import time
import json
import os
import random
from nltk.stem.lancaster import LancasterStemmer
import nltk
import difflib

with open("intents.json") as file:
    data = json.load(file)

App = Assistant('Clara', data)

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
# text = get_audio()


def Phrase_Matcher(phrase):
	stemmer = LancasterStemmer()
	intents = App.phrase_data['intents']
	max_similarity = 0
	phrase_stemmed = stemmer.stem(phrase.lower())
	for item in intents:
		for pattern in item['patterns']:
			pattern_stemmed = stemmer.stem(pattern.lower())
			similarity = difflib.SequenceMatcher(None, pattern_stemmed, phrase_stemmed).ratio()
			if similarity > max_similarity:
				print(pattern, similarity)
				tag = item['tag']
				response = item['responses']
	print('Final pick is:', tag)
	return tag, response

def Random_Response(responses):
	index = random.randrange(len(responses))
	App.Speak(responses[index])

def Main():
	start_phrase = f"I am {App.name}, how can I help you?"
	print(start_phrase)
	App.Speak(start_phrase)
	while True:
		tag = ''
		response = input()
		tag, response = Phrase_Matcher(response)
		if tag == 'turn_on_lights':
			App.Set_Scene('Bright')
		if tag == 'turn_off_lights':
			App.Turn_Off_Lights()
		elif tag == '':
			response = App.phrase_data['other_responses'][0]['unknown']
		Random_Response(response)


if __name__ == "__main__":
	Main()
	pass