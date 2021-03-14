from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from pyHS100 import SmartPlug
from phue import Bridge
from ahk import AHK
import difflib
import random
import json
from Assistant_Actions import Actions


class Assist:
	# module init
	stemmer = LancasterStemmer()
	func = Actions()
	with open("stopwords.txt", "r") as f:
		stop_words = set(f.read())

	# obj init
	Hue_Hub = Bridge('192.168.0.134')
	Heater = SmartPlug('192.168.0.146')
	Lighthouse = SmartPlug('192.168.0.196')
	ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
	ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
	ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
	ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


	def __init__(self, assistant_name, user_name, user_nickname):
		# config init
		with open("intents.json") as file:
			self.data = json.load(file)
		self.similarity_req = self.data['settings']['similarity_req']
		self.debug = self.data['settings']['debug']
		self.intents = self.data['intents']

		# name init
		self.assistant_name = assistant_name
		self.user_name = user_name
		self.user_nickname = user_nickname


	def simplify_phrase(self, sentence):
		sentence = self.stemmer.stem(sentence.lower())
		word_tokens = word_tokenize(sentence)
		return [word for word in word_tokens if not word in self.stop_words]


	def phrase_matcher(self, phrase):
		max_similarity = self.similarity_req
		prepped_phrase = self.simplify_phrase(phrase)
		match_dict = {'tag':None}
		for item in self.intents:
			for pattern in item['patterns']:
				prepped_pattern = self.simplify_phrase(pattern)
				similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
				if similarity > max_similarity:
					max_similarity = similarity
					match_dict = item
					match_dict['pattern'] = pattern.lower()
		if self.debug == 1 and 'tag' in match_dict.keys():
			print(f'\nTag: {match_dict["tag"]}\nSimilarity:{max_similarity}')
		return match_dict


	def main(self):
		'''
		Starts assistant loop.
		'''
		print(f"{self.assistant_name}:\nHello, I'm {self.assistant_name}.")
		while True:
			print(f'\n{self.user_name}:')
			user_input = input()
			if user_input == '':  # skips to beginning if no response is given
				continue
			# takes user_input and gets match information
			match_dict = self.phrase_matcher(user_input)
			if match_dict['tag'] == None:
				response = random.choice(self.data['other_responses']['unknown'])
			elif 'responses' in match_dict.keys():
				response = random.choice(match_dict['responses'])
			# assistant actions
			if 'action' in match_dict.keys():
				# Hue lights and Smarthub Actions
				if match_dict['action'] == 'turn_on_lights':
					self.func.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)
				if match_dict['action'] == 'turn_on_backlight':
					self.func.Hue_Hub.run_scene('My Bedroom', 'Backlight', 1)
				elif match_dict['action'] == 'turn_off_lights':
					self.func.Hue_Hub.set_group('My Bedroom', 'on', False)
				elif match_dict['action'] == 'toggle_heater':
					self.func.toggle_heater(match_dict['pattern'])
				# Computer Control Actions
				elif match_dict['action'] == 'set_audio_default':
					self.func.set_audio_default(match_dict['pattern'])
				elif match_dict['action'] == 'display_switch':
					self.func.display_switch(match_dict['pattern'])
				elif match_dict['action'] == 'start_vr':
					self.func.Start_vr()
				# Informational Actions
				elif match_dict['action'] == 'date_time':
					response = self.func.check_time_date(match_dict['pattern'])
				if match_dict['action'] == 'exit':
					exit()
			print(f'\n{self.assistant_name}:\n{response}')


if __name__ == "__main__":
	App = Assist('Clara', 'Michael', 'Concrete')
	App.main()
