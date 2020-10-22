from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
import nltk
import datetime as dt
import difflib
import json
import os


class Func:


    def __init__(self):
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.voice_mode = self.phrase_data['settings']['voice_mode']
        self.preferred_mic = self.phrase_data['settings']['preferred_mic']
        self.similarity_req = self.phrase_data['settings']['similarity_req']
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
