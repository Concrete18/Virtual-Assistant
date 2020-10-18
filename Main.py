from Assistant import Assistant
import speech_recognition as sr
import difflib
import random
import nltk

App = Assistant('Clara', 'Michael', 'Concrete')

# names = ['Clara', 'Eretria', 'Echo', 'Ezri','Elora', 'Era','Eowyn', 'Flora', 'Inara', 'Iris', 'Luna', 'Leta' ,'Cara',
# 		'Sylvia','Tallulah','Zephyra','Zyla']

# for name in names:
# 	App.Speak(name)
# input()


def Phrase_Matcher(phrase):
	'''Matches phrases to patterns in intent.json'''
	intents = App.phrase_data['intents']
	max_similarity = 0
	matched_pattern = ''
	tag = ''
	response = ''
	prepped_phrase = App.Simplify_Phrase(phrase)
	example_sent = "This is a sample sentence, showing off the stop words filtration."
	for item in intents:
		for pattern in item['patterns']:
			prepped_pattern = App.Simplify_Phrase(pattern)
			similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
			if similarity > max_similarity and similarity > .6:
				max_similarity = similarity
				tag = item['tag']
				matched_pattern = pattern
				response = item['responses']
	if App.debug == 1:
		print('Final pick is:', tag, '\n', max_similarity,'\n', matched_pattern, '\n')
	return tag, response


def Random_Response(responses):
	'''
	Randomly picks a response from a list of given responses.
	Speaks and/or prints the selected response depending on the config settings.

	arg: text is what is output in verval and/or text form

	"voice_response": 1,

	"text_response": 1
	'''
	index = random.randrange(len(responses))
	if App.text_response:
		print(responses[index])
	if App.voice_response:
		App.Speak(responses[index])
	print('')


def Main():
	'''Main Initialization function.'''
	# start_phrases = App.phrase_data['other_responses']['start_phrases']
	# Random_Response(start_phrases)
	start_phrase = f"I am {App.assistant_name}, how can I help you?"
	print(start_phrase)
	App.Speak(start_phrase)
	while True:
		tag = ''
		response = input()
		tag, response = Phrase_Matcher(response)
		if tag == 'turn_on_lights':
			App.Hue_Hub.run_scene('My Bedroom', 'Bright', 1)
		elif tag == 'turn_off_lights':
			App.Hue_Hub.set_group('My Bedroom', 'on', False)
		elif tag == 'set_audio_to_PC':
			App.ahk.run_script(App.ahk_speakers, blocking=False)
		elif tag == 'cyberpunk':
			App.Time_Till('Cyberpunk 2077', 11,19,2020)
		elif tag == '':
			response = App.phrase_data['other_responses']['unknown']
		if len(response) != 0:
			Random_Response(response)
		if tag == 'goodbye':
			quit()


if __name__ == "__main__":
	Main()
