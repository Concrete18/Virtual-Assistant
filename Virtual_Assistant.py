from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from gtts import gTTS
import playsound
from threading import Thread
import difflib
import random
import json
import os
import subprocess
import sys
import re
import psutil
from pyHS100 import SmartPlug
from phue import Bridge
from ahk import AHK
from time import sleep
import datetime as dt


class Action_class:

	# obj init
	Hue_Hub = Bridge('192.168.0.134')
	Heater = SmartPlug('192.168.0.146')
	Lighthouse = SmartPlug('192.168.0.196')
	ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
	# var init
	ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
	ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
	ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


	@staticmethod
	def assistant_status(match_dict, assistant_name):
		'''
		Opens folder given as folder_dir.
		'''
		# TODO finish assistant_status function
		response = ''
		# virtual memory
		virt_mem = psutil.virtual_memory()
		if virt_mem.used > virt_mem.total/2:
			response += 'I am a bit busy at the moment but it is fine.'
		# battery info
		battery = psutil.sensors_battery()
		if battery != None:
			print('Percent:', battery.percent)
			print('Seconds Left:', battery.secsleft)
			print('Plugged In:', battery.power_plugged)
			print(battery)
			if battery.power_plugged:
				battery_info = f'Battery is at {battery.percent}'
				response += battery_info
		if response == '':
			response = random.choice(match_dict['responses'])
		response = response.replace('{assistant_name}', assistant_name)
		return response


	@staticmethod
	def open_folder(folder):
		'''
        Opens folder given as folder_dir.
        '''
        # TODO finish open_folder function
		folders = {
            'Home Control Interface':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Home Control Interface.lnk',
            'Timed Sleep or Shutdown':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed Sleep or Shutdown.lnk',
            'Media Release Updater':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Media Release Updater.lnk'
		}
		for folder_name, folder_dir in folders.items():
			if folder in folder_name:
				subprocess.Popen(rf'explorer /select, {folder_dir}')
				return


	@staticmethod
	def run_script(script):
		'''
		Runs script based on given script name if it is in the scripts dictionary.
        '''
        # TODO finish run_script function
		scripts = {
            'Home Control Interface':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Home Control Interface.lnk',
            'Timed Sleep or Shutdown':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed Sleep or Shutdown.lnk',
            'Media Release Updater':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Media Release Updater.lnk'
        }
		for script_name, script_dir in scripts.items():
			if script in script_name:
				subprocess.run([sys.executable, f'{script}.lnk'], cwd=os.path.dirname(script_dir))
				return
		print('No script found with that name.')


	def display_switch(self, pattern):
		'''
        Switches display to the mode that matches the pattern argument. Works for PC and TV mode.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
		if 'TV' in pattern:
			mode = 'TV'
		else:
			mode = 'PC'
		subprocess.call([f'{os.getcwd()}/Batches/{mode} Mode.bat'])  # runs .bat for different modes
		sleep(10)
		if mode == 'PC':  # switches audio default via an AHK wrapper
			self.ahk.run_script(self.ahk_speakers, blocking=False)
		else:
			self.ahk.run_script(self.ahk_tv, blocking=False)


	def set_audio_default(self, pattern):
		'''
        Sets the audio device depending on the device is mentioned in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
		if 'pc' in pattern:
			self.ahk.run_script(self.ahk_speakers, blocking=False)
		elif 'tv' in pattern:
			self.ahk.run_script(self.ahk_tv, blocking=False)
		else:
			self.ahk.run_script(self.ahk_headphones, blocking=False)


	def start_vr(self):
		'''
        Start VR Function.
        '''
        # runs SteamVR
		subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")
		if self.Lighthouse.get_sysinfo()["relay_state"] == 0:  # turns on Lighthouse if it is off
			self.Lighthouse.turn_on()


	@staticmethod
	def check_time_date(pattern) -> str:
		'''
        Says the Date or time depending on which is in the pattern chosen.

        Arguments:

        pattern -- matched response from phrase_matcher
        '''
		if 'time' in pattern:
			current_time = dt.datetime.now().strftime("%I:%M %p")
			if current_time[0] == '0':
				current_time = current_time[1:]
			return f'It is {current_time}'
		elif 'tomorrow' in pattern:
			tomorrow = dt.datetime.today() + dt.timedelta(days=1)
			return f"It is {tomorrow.strftime('%A, %B %d, %Y')}"
		elif 'date' or 'day' in pattern:
			return f"It is {dt.datetime.now().strftime('%A, %B %d, %Y')}"


	@staticmethod
	def time_till(month, day, year=None, subject=None,):
		'''
        Gives the time till the given date arrives.
        '''
		if year == None:
			year = dt.datetime.now().year
        # time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
		time_till = dt.datetime.strptime(f'{month}-{day}-{year}', f'%m-%d-%Y') - dt.datetime.now()
		if subject != None:
			return f'{subject} is in {time_till.days} days.'
		else:
			return f'{time_till.days} days till {month}/{day}/{year}.'


	@staticmethod
	def time_till_custom(pattern):
		'''
        Gives the time till the given date arrives.
        '''
		date_entry = re.search(rf'/d', pattern)
		month, day, year = date_entry.split('-')
		if year == None:
			year = dt.datetime.now().year

		time_till = dt.datetime.strptime(f'{month}-{day}-{year}', f'%m-%d-%Y') - dt.datetime.now()

		return f'{time_till.days} days till {month}/{day}/{year}.'


class Assistant:
	# module init
	stemmer = LancasterStemmer()
	Action = Action_class()

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
	verbose = data['settings']['verbose']
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
		self.voice_in_use = 1
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
		if os.path.exists(filename):  # removes old file if it exists due to error before it is deleted
			os.remove(filename)
		self.voice_in_use = 0


	def startup_convo(self):
		'''
		Startup conversation and any other setup.
		'''
		response = f"Hello {self.user_name}"
		if self.verbose:
			response += ', how can I help?'
		else:
			response += '.'
		print(f'{self.assistant_name}:\n{response}')
		if self.synth_voice:
			self.speak(response)
			# Thread(target=self.speak, args=(response,)).start()


	def respond(self, response, use_input=0):
		'''
		Replaces placeholders and prints/says responses.
		'''
		replacements = {
			'{assistant_name}':self.assistant_name,
			'{user_name}':self.user_name,
		}
		for placeholder, value in replacements.items():
			response = response.replace(placeholder, value)
		if self.synth_voice:
			while True:
				if self.voice_in_use == 0:
					Thread(target=self.speak, args=(response,)).start()
					break
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

				if 'action' in match_dict.keys():
					# assistant actions
					if match_dict['action'] == 'assistant_status':
						response = self.Action.assistant_status(match_dict, self.assistant_name)

					# voice
					if 'talking' in match_dict['action']:
							if match_dict['action'] == 'start_talking':
								self.synth_voice = 1
							elif match_dict['action'] == 'stop_talking':
								self.synth_voice = 0

					# Hue lights and Smarthub Actions
					if match_dict['action'] == 'turn_on_lights':
						self.Action.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)

					if match_dict['action'] == 'turn_on_backlight':
						self.Action.Hue_Hub.run_scene('My Bedroom', 'Backlight', 1)

					elif match_dict['action'] == 'turn_off_lights':
						self.Action.Hue_Hub.set_group('My Bedroom', 'on', False)

					elif match_dict['action'] == 'toggle_heater':
						if 'on' in match_dict['pattern']:
							self.Action.Heater.turn_on()
							response = 'Turned on the heater.'
						else:
							self.Action.Heater.turn_off()
							response = 'Turned off the heater.'

					# Computer Control Actions
					elif match_dict['action'] == 'open_folder':
						folder = self.respond('What folder do you want to open?', use_input=1)
						self.Action.open_folder(folder)

					elif match_dict['action'] == 'run_script':
						script = self.respond('What script do you want to run?', use_input=1)
						self.Action.run_script(script)

					elif match_dict['action'] == 'set_audio_default':
						self.Action.set_audio_default(match_dict['pattern'])

					elif match_dict['action'] == 'display_switch':
						self.Action.display_switch(match_dict['pattern'])

					elif match_dict['action'] == 'start_vr':
						self.Action.Start_vr()

					# Informational Actions
					elif match_dict['action'] == 'date_time':
						response = self.Action.check_time_date(match_dict['pattern'])

					elif match_dict['action'] == 'what_is_tomorrow':
						response = self.Action.check_time_date(match_dict['pattern'])

					elif match_dict['action'] == 'time_till':
						if 'subject' in match_dict.keys():
							response = self.Action.time_till(
								day=match_dict['day'],
								month=match_dict['month'],
								subject=match_dict['subject'])
						else:
							# TODO find date in pattern
							response = self.Action.time_till_custom(match_dict['date'])

					if match_dict['action'] == 'exit':
						self.respond(response)
						exit()

				self.respond(response)
		except KeyboardInterrupt:
			print('Good bye\n')
			print(f'{self.assistant_name}:\nGood bye {self.user_name}')
			exit()


if __name__ == "__main__":
	Assistant().run_loop()
