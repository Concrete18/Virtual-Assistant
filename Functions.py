from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import nltk
from gtts import gTTS
import datetime as dt
import playsound
import threading
import difflib
import random
import json
import os


class Func:


    def __init__(self):
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.voice_mode = self.phrase_data['settings']['voice_mode']
        self.preferred_mic = self.phrase_data['settings']['preferred_mic']
        self.similarity_req = self.phrase_data['settings']['similarity_req']
        self.disable_voice_without_pref_mic = self.phrase_data['settings']['disable_voice_without_pref_mic']
        self.voice_response = self.phrase_data['settings']['voice_response']
        self.text_response = self.phrase_data['settings']['text_response']
        self.debug = self.phrase_data['settings']['debug']


    def Phrase_Matcher(self, phrase):
        '''Matches phrases to patterns in intent.json'''
        intents = self.phrase_data['intents']
        max_similarity = 0
        matched_pattern = ''
        tag = ''
        responses = ''
        prepped_phrase = self.Simplify_Phrase(phrase)
        example_sent = "This is a sample sentence, showing off the stop words filtration."
        for item in intents:
            for pattern in item['patterns']:
                prepped_pattern = self.Simplify_Phrase(pattern)
                similarity = difflib.SequenceMatcher(None, prepped_pattern, prepped_phrase).ratio()
                if similarity > max_similarity and similarity > self.similarity_req:
                    max_similarity = similarity
                    tag = item['tag']
                    matched_pattern = pattern.lower()
                    responses = item['responses']
        if self.debug == 1:
            print(f'Final pick is: {tag} with similarity:{max_similarity}\n{matched_pattern}\n')
        return tag, responses, matched_pattern


    def Speak(self, text):
        '''Using gTTS, verbally says the text variable with Text-To-Speech '''
        def text_to_speech(text):
            tts = gTTS(text=text, lang='en')
            filename = 'voice.mp3'
            if os.path.exists(filename):
                os.remove(filename)
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        try:
            thread = threading.Thread(target=text_to_speech(text))
            thread.start()
        except:
            pass


    def Random_Response(self, responses):
        '''Randomly picks a response from a list of given responses.
        Speaks and/or prints the selected response depending on the config settings.

        arg: text is what is output in verval and/or text form

        "voice_response": 1,

        "text_response": 1'''
        choice = responses[random.randrange(0, len(responses))]
        # if '{' in choice:
        #     self.Speak(choice.format(name=App.name))
        if self.text_response:
            print(choice)
        if self.voice_response:
            self.Speak(choice)
        print('')


    def Simplify_Phrase(self, sentence):
        '''Uses NLTK to and a stopwords list to stem and shorten
        the inputted sentence to remove unneeded information.'''
        with open("stopwords.txt", "r") as f:
            stopwords = f.read()
        stemmer = LancasterStemmer()
        sentence = stemmer.stem(sentence.lower())
        # stop_words = set(stopwords.words('english'))
        stop_words = set(stopwords)
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        # print(f'filtered sentence: {filtered_sentence}')
        return filtered_sentence
