from Assistant import Assistant
from Functions import Func


Func = Func()
Action = Assistant('Clara', 'Michael', 'Concrete', Func)


def Name_Test():
	names = ['Clara', 'Ezri', 'Elora', 'Era', 'Eowyn', 'Flora', 'Inara', 'Iris', 'Luna', 'Leta' ,'Cara', 'Sylvia']
	for name in names:
		Func.Speak(name)
	input()


# Name_Test()


def Main():
	'''Main Initialization function.'''
	# start_phrases = Func.phrase_data['other_responses']['start_phrases']
	# Func.Random_Response(f'{start_phrases}')
	start_phrase = f"I am {Action.assistant_name}, how can I help you?"
	print(start_phrase)
	Func.Speak(start_phrase)
	while True:
		tag = ''
		user_input = input()
		tag, responses = Func.Phrase_Matcher(user_input)
		print(responses)
		if tag == 'turn_on_lights':
			Action.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)
		elif tag == 'turn_off_lights':
			Action.Hue_Hub.set_group('My Bedroom', 'on', False)
		elif tag == 'set_audio_to_PC':
			Action.ahk.run_script(Action.ahk_speakers, blocking=False)
		elif tag == 'toggle_heater':
			Action.Toggle_Heater()
		elif tag == 'cyberpunk':
			Action.Time_Till('Cyberpunk 2077', 11,19,2020)
		elif tag == '':
			responses = Func.phrase_data['other_responses']['unknown']
		if responses[0] != '':
			Func.Random_Response(responses)
		if tag == 'goodbye':
			quit()


if __name__ == "__main__":
	Main()
