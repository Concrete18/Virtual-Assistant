from Actions import Actions
from Functions import Func

func = Func()
Action = Actions(assistant_name='Clara', user_name='Michael', user_nickname='Concrete', func_obj=func)


def Main():
	'''Main Initialization function.'''
	print(f"{Action.assistant_name}: Hello, I'm {Action.assistant_name}.")
	Action.Speak(f"Hello, I'm {Action.assistant_name}.")
	while True:
		tag = ''
		if Action.voice_mode == 1:
			user_input = Action.speech_recognition()
		else:
			user_input = input()
			if user_input == '':  # allows for skipping to beginingg if no response
				continue
		print()
		tag, responses, pattern = func.Phrase_Matcher(user_input)  # takes user_input and gets match information
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
		elif tag == 'roku_abc':
			Action.Roku_to_ABC()
		# End of Actions
		elif tag == '':
			responses = func.phrase_data['other_responses']['unknown']
		if responses[0] != '':  # This is for blocking the response if an Action handles it.
			Action.Respond(responses)
		if tag == 'goodbye':
			quit()


if __name__ == "__main__":
	Main()
