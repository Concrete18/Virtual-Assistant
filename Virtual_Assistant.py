from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from gtts import gTTS
import playsound
from threading import Thread
import difflib
import random
import json
import os
from Assistant_Actions import Action


class Assistant:
	# module init
	stemmer = LancasterStemmer()

	# var init
	with open("stopwords.txt", "r") as f:
		stop_words = set(f.read())

	# config init
	with open("intents.json") as file:
		data = json.load(file)
	intents = data['intents']
	unknown_msg_resp = data['other_responses']['unknown']

	with open("config.json") as file:
		data = json.load(file)
	assistant_name = data['settings']['assistant_name']
	user_name = data['settings']['real_name']
	synth_voice = data['settings']['synth_voice']
	similarity_req = data['settings']['similarity_req']
	debug = data['settings']['debug']


	def simplify_phrase(self, sentence):
		'''
		ph
		'''
		sentence = self.stemmer.stem(sentence.lower())
		word_tokens = word_tokenize(sentence)
		return [word for word in word_tokens if not word in self.stop_words]


	def phrase_matcher(self, phrase) -> dict:
		'''
		Takes the given phrase and finds a match in intents.json.
		'''
		max_similarity = self.similarity_req
		prepped_phrase = self.simplify_phrase(phrase)
		match_dict = {'tag':None}
		for item in self.intents:
			for pattern in item['patterns']:
				prepped_pattern = self.simplify_phrase(pattern)
				similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
				# print(pattern, similarity)
				if similarity > max_similarity:
					if self.debug == 1:
						print(f'\nPattern: {pattern}\n{similarity}')
					max_similarity = similarity
					match_dict = item
					match_dict['pattern'] = pattern.lower()
		if self.debug == 1 and 'tag' in match_dict.keys():
			print(f'\nTag: {match_dict["tag"]}\nSimilarity:{max_similarity}')
		return match_dict


	def speak(self, text):
		'''
		Using gTTS, verbally says the text variable with Text-To-Speech Text-To-Speech
        Arguments:
        text -- text to be spoken using Google Text-To-Speech
        '''
		tts = gTTS(text=text, lang='en')
		filename = 'voice.mp3'
		if os.path.exists(filename):  # removes old file if it exists due to error before it is deleted
			os.remove(filename)
		try:
			tts.save(filename)
		except ValueError as error:
			if self.debug == 1:
				print(error)
			return
		playsound.playsound(filename)
		os.remove(filename)


	def startup_convo(self):
		'''
		ph
		'''
		response = f"Hello {self.user_name}, How can I help?"
		if self.synth_voice:
			Thread(target=self.speak, args=(response,)).start()
		print(f'{self.assistant_name}:\n{response}')


	def respond(self, response, use_input=0):
		'''
		ph
		'''
		response = response.replace('{assistant_name}', self.assistant_name)
		response = response.replace('{user_name}', self.user_name)
		if self.synth_voice:
			Thread(target=self.speak, args=(response,)).start()
		if use_input == 0:
			print(f'\n{self.assistant_name}:\n{response}')
		else:
			return input(f'\n{self.assistant_name}:\n{response}')


	def run_loop(self):
		'''
		Starts assistant loop.
		'''
		self.startup_convo()
		try:
			while True:
				print(f'\n{self.user_name}:')
				user_input = input()
				if user_input == '':  # skips to beginning if no response is given
					continue
				# takes user_input and gets match information
				match_dict = self.phrase_matcher(user_input)
				if match_dict['tag'] == None:
					response = random.choice(self.unknown_msg_resp)
				elif 'responses' in match_dict.keys():
					response = random.choice(match_dict['responses'])
				# assistant actions
				if 'action' in match_dict.keys():
					# voice
					if 'talking' in match_dict['action']:
							if match_dict['action'] == 'start_talking':
								self.synth_voice = 1
							elif match_dict['action'] == 'stop_talking':
								self.synth_voice = 0
					# Hue lights and Smarthub Actions
					if match_dict['action'] == 'turn_on_lights':
						Action.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)

					if match_dict['action'] == 'turn_on_backlight':
						Action.Hue_Hub.run_scene('My Bedroom', 'Backlight', 1)

					elif match_dict['action'] == 'turn_off_lights':
						Action.Hue_Hub.set_group('My Bedroom', 'on', False)

					elif match_dict['action'] == 'toggle_heater':
						response = Action.toggle_heater(match_dict['pattern'])

					# Computer Control Actions
					elif match_dict['action'] == 'open_folder':
						folder = self.respond('What folder do you want to open?', use_input=1)
						Action.open_folder(folder)

					elif match_dict['action'] == 'run_script':
						script = self.respond('What script do you want to run?', use_input=1)
						Action.run_script(script)

					elif match_dict['action'] == 'set_audio_default':
						Action.set_audio_default(match_dict['pattern'])

					elif match_dict['action'] == 'display_switch':
						Action.display_switch(match_dict['pattern'])

					elif match_dict['action'] == 'start_vr':
						Action.Start_vr()

					# Informational Actions
					elif match_dict['action'] == 'date_time':
						response = Action.check_time_date(match_dict['pattern'])

					elif match_dict['action'] == 'what_is_tomorrow':
						response = Action.check_time_date(match_dict['pattern'])

					elif match_dict['action'] == 'time_till':
						if 'subject' in match_dict.keys():
							response = Action.time_till(
								day=match_dict['day'],
								month=match_dict['month'],
								subject=match_dict['subject'])
						else:
							# TODO find date in pattern
							response = Action.time_till_custom(match_dict['date'])

					if match_dict['action'] == 'exit':
						self.respond(response)
						exit()

				self.respond(response)
		except KeyboardInterrupt:
			print(f'Good bye {self.user_name}')


if __name__ == "__main__":
	Assistant().run_loop()
