# from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from pyHS100 import SmartPlug
from phue import Bridge
import datetime as dt
from ahk import AHK
from Functions import Func
import json
import subprocess
import playsound
import threading
from gtts import gTTS
from time import sleep
import os
from roku import Roku
import random


class Actions:


    def __init__(self, assistant_name, user_name, user_nickname, func_obj):
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.assistant_name = assistant_name
        self.user_name = user_name
        self.user_nickname = user_nickname
        self.func_obj = func_obj
        self.disable_voice_without_pref_mic = self.phrase_data['settings']['disable_voice_without_pref_mic']
        self.voice_response = self.phrase_data['settings']['voice_response']
        self.text_response = self.phrase_data['settings']['text_response']
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.Lighthouse = SmartPlug('192.168.0.196')
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    def Speak(self, text):
        '''Using gTTS, verbally says the text variable with Text-To-Speech Text-To-Speech

        Arguments:

        text -- text to be spoken using Google Text-To-Speech
        '''
        def text_to_speech(text):
            tts = gTTS(text=text, lang='en')
            filename = 'voice.mp3'
            if os.path.exists(filename):  # removes old file if it exists due to error before it is deleted
                os.remove(filename)
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        try:
            thread = threading.Thread(target=text_to_speech(text))
            thread.start()
        except:
            pass


    def Respond(self, responses):
        '''Prints the assistant response by picking a random response from the responses argument

        Arguments:

        responses -- response list that has a random index chosen to be used in the Speak Method
        '''
        if type(responses) == str:
            choice = responses
        else:
            choice = responses[random.randrange(0, len(responses))]
        # WIP translation of json strings to turn {} words into usable variables
        # if '{' in choice:
        #     self.Speak(choice.format(name=App.name))
        if self.text_response:  # prints response if setting is enabled
            print(f'{self.assistant_name}: {choice}\n')
        if self.voice_response:  # speaks response if setting is enabled
            self.Speak(choice)


    def Time_Till(self, subject, month, day, year):
        '''Speaks and says how many days til the subject releases.

        Arguments:

        subject -- Subject that is released

        month -- Subject's month of release

        day -- Subject's day of release

        year -- Subject's year of release
        '''
        time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        text = f'{subject} is out in {time_till.days} days.'
        self.Respond(text)


    def Display_Switch(self, pattern):
        '''Switches display to the mode that matches the pattern argument. Works for PC and TV mode.

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


    def Set_Audio_Default(self, pattern):
        '''Sets the audio device depending on the device is mentioned in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'pc' in pattern:
            self.ahk.run_script(self.ahk_speakers, blocking=False)
        elif 'tv' in pattern:
            self.ahk.run_script(self.ahk_tv, blocking=False)
        else:
            self.ahk.run_script(self.ahk_headphones, blocking=False)


    def Toggle_heater(self, pattern):
        '''Turns the heater on or off depending on if ON or OFF is in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'on' in pattern:
            self.Heater.turn_on()
        elif 'off' in pattern:
            self.Heater.turn_off()


    def Start_VR(self):
        '''Start VR Function.'''
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:  # turns on Lighthouse if it is off
            self.Lighthouse.turn_on()
        # runs SteamVR
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    def Check_Time_Date(self, pattern):
        '''Says the Date or time depending on which is in the pattern chosen.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        response = ''
        if 'time' in pattern:
            response = f'It is {dt.datetime.now().strftime("%I:%M %p")}'
        elif 'date' or 'day' in pattern:
            response = f"Today's date is {dt.datetime.now().strftime('%A, %d %B %Y')}"
        self.Respond(response)


    def Roku_to_ABC(self):
        '''Changes Roku to ABC on Youtube TV'''
        roku = Roku('192.168.0.131')
        def Callback():
            self.Respond('Switching to ABC')
            youtube = roku['YouTube TV']
            youtube.launch()
            sleep(10)
            roku.right()
            sleep(1)
            for _ in range(2):
                roku.down()
                sleep(.5)
            roku.enter()
            if 'YouTube TV' in str(roku.active_app):
                self.Respond('I set the Roku to ABC News.')
            else:
                self.Respond('I was unable to set the Roku to ABC News.')
        ABC = threading.Thread(target=Callback)
        ABC.start()
