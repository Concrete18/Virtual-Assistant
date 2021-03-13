from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from pyHS100 import SmartPlug
from phue import Bridge
from ahk import AHK
import difflib
import random
import json


class Assistant:

	# module init
	stemmer = LancasterStemmer()
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


	def phrase_matcher(self, phrase):
		max_similarity = self.similarity_req
		prepped_phrase = self.simplify_phrase(phrase)
		for item in self.intents:
			for pattern in item['patterns']:
				prepped_pattern = self.simplify_phrase(pattern)
			similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
			if similarity > max_similarity:
				max_similarity = similarity
				match_data = item
				match_data['pattern'] = pattern.lower()
		if self.debug == 1:
			print(f'Final pick is: {match_data["tag"]} with similarity:{max_similarity}\n{match_data["pattern"]}\n')
		return match_data


	def simplify_phrase(self, sentence):
		sentence = self.stemmer.stem(sentence.lower())
		word_tokens = word_tokenize(sentence)
		filtered_sentence = [word for word in word_tokens if not word in self.stop_words]
		for word in word_tokens:
			if word not in self.stop_words:
				filtered_sentence.append(word)
		if self.debug == 1:
			print(f'filtered sentence: {filtered_sentence}')
		return filtered_sentence


	def respond(self, responses):
		if type(responses) == str:
			choice = responses
		else:
			choice = responses[random.randrange(0, len(responses))]
		print(f'{self.assistant_name}: {choice}\n')


	def main(self):
		'''
		Main Initialization function.
		'''
		print(f"{self.assistant_name}: Hello, I'm {self.assistant_name}.")
		while True:
			user_input = input()
			if user_input == '':  # allows for skipping to beginingg if no response
				continue
			match_dict = self.phrase_matcher(user_input)  # takes user_input and gets match information
			if 'Action' in match_dict.keys():
				# Hue lights and Smarthub Actions
				if match_dict['tag'] == 'turn_on_lights':
					self.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)
				if match_dict['tag'] == 'backlight':
					self.Hue_Hub.run_scene('My Bedroom', 'Backlight', 1)
				elif match_dict['tag'] == 'turn_off_lights':
					self.Hue_Hub.set_group('My git pBedroom', 'on', False)
				elif match_dict['tag'] == 'toggle_heater':
					self.Toggle_heater(match_dict['pattern'])
				# Computer Control Actions
				elif match_dict['tag'] == 'set_audio_default':
					self.Set_Audio_Default(match_dict['pattern'])
				elif match_dict['tag'] == 'display_switch':
					self.Display_Switch(match_dict['pattern'])
				elif match_dict['tag'] == 'start_vr':
					self.Start_VR()
				# Informational Actions
				elif match_dict['tag'] == 'date_time':
					self.Check_Time_Date(match_dict['pattern'])
				elif match_dict['tag'] == 'roku_abc':
					self.Roku_to_ABC()
			# End of Actions
			elif match_dict['tag'] == '':
				responses = self.phrase_data['other_responses']['unknown']
			if responses[0] != '':  # This is for blocking the response if an action handles it.
				self.respond(responses)
			if match_dict['tag'] == 'goodbye':
				exit()


if __name__ == "__main__":
	App = Assistant('Clara', 'Michael', 'Concrete')
	App.main()
