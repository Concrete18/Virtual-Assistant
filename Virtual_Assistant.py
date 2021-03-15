from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import difflib
import random
import json
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
	similarity_req = data['settings']['similarity_req']
	debug = data['settings']['debug']


	@classmethod
	def simplify_phrase(cls, sentence) -> list:
		sentence = cls.stemmer.stem(sentence.lower())
		word_tokens = word_tokenize(sentence)
		return [word for word in word_tokens if not word in cls.stop_words]


	@classmethod
	def phrase_matcher(cls, phrase) -> dict:
		max_similarity = 0
		prepped_phrase = cls.simplify_phrase(phrase)
		match_dict = {'tag':None}
		for item in cls.intents:
			for pattern in item['patterns']:
				prepped_pattern = cls.simplify_phrase(pattern)
				similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
				# print(pattern, similarity)
				if similarity > max_similarity and similarity > cls.similarity_req:
					if cls.debug == 1:
						print(f'\nPattern: {pattern}\n{similarity}')
					max_similarity = similarity
					match_dict = item
					match_dict['pattern'] = pattern.lower()
		if cls.debug == 1 and 'tag' in match_dict.keys():
			print(f'\nTag: {match_dict["tag"]}\nSimilarity:{max_similarity}')
		return match_dict


	@classmethod
	def startup_convo(cls):
		print(f"{cls.assistant_name}:\nHello {cls.user_name}, How can I help?")


	@classmethod
	def respond(cls, response, use_input=0) -> str:
		response = response.replace('{assistant_name}', cls.assistant_name)
		response = response.replace('{user_name}', cls.user_name)
		if use_input == 0:
			print(f'\n{cls.assistant_name}:\n{response}')
		else:
			return input(f'\n{cls.assistant_name}:\n{response}')


	@classmethod
	def run_loop(cls):
		'''
		Starts assistant loop.
		'''
		cls.startup_convo()
		while True:
			print(f'\n{cls.user_name}:')
			user_input = input()
			if user_input == '':  # skips to beginning if no response is given
				continue
			# takes user_input and gets match information
			match_dict = cls.phrase_matcher(user_input)
			if match_dict['tag'] == None:
				response = random.choice(cls.unknown_msg_resp)
			elif 'responses' in match_dict.keys():
				response = random.choice(match_dict['responses'])
			# assistant actions
			if 'action' in match_dict.keys():
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
					folder = cls.respond('What folder do you want to open?', use_input=1)
					Action.open_folder(folder)

				elif match_dict['action'] == 'run_script':
					script = cls.respond('What script do you want to run?', use_input=1)
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

				elif match_dict['action'] == 'time_till':
					if 'subject' in match_dict.keys():
						response = Action.time_till(
							day=match_dict['day'],
							month=match_dict['month'],
							subject=match_dict['subject'])
					else:
						# TODO find date in pattern
						print(match_dict['pattern'])
						response = Action.time_till(match_dict['date'])

				if match_dict['action'] == 'exit':
					exit()

			cls.respond(response)


if __name__ == "__main__":
	Assistant.run_loop()
