from Actions import Actions
from Functions import Func


func = Func()
Action = Actions('Clara', 'Michael', 'Concrete', func)


def Main():
	'''Main Initialization function.'''
	# start_phrases = func.phrase_data['other_responses']['start_phrases']
	# func.Random_Response(f'{start_phrases}')
	start_phrase = f"Hello, I'm {Action.assistant_name}."
	print(start_phrase)
	func.Speak(start_phrase)
	while True:
		tag = ''
		user_input = input()
		tag, responses, pattern = func.Phrase_Matcher(user_input)
		# Hue lights and Smarthub Actions
		if tag == 'turn_on_lights':
			Action.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)
		if tag == 'backlight':
			Action.Hue_Hub.run_scene('My Bedroom', 'Backlight', 1)
		elif tag == 'turn_off_lights':
			Action.Hue_Hub.set_group('My Bedroom', 'on', False)
		elif tag == 'toggle_heater':
			Action.Toggle_heater(pattern)
		# Computer Control Actions
		elif tag == 'set_audio_default':
			Action.Set_Audio_Default(pattern)
		elif tag == 'display_switch':
			Action.Display_Switch(pattern)
		elif tag == 'start_vr':
			Action.Start_VR()
		# Informational Actions
		elif tag == 'date_time':
			Action.Check_Time_Date(pattern)
		elif tag == 'cyberpunk':
			Action.Time_Till('Cyberpunk 2077', 11,19,2020)
		# End of Actions
		elif tag == '':
			responses = func.phrase_data['other_responses']['unknown']
		if responses[0] != '':  # This is for blocking the response if an Action handles it.
			func.Random_Response(responses)
		if tag == 'goodbye':
			quit()


if __name__ == "__main__":
	Main()
