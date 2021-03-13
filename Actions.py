from pyHS100 import SmartPlug
from phue import Bridge
import datetime as dt
from ahk import AHK
import json
import subprocess
import threading
from time import sleep
import os
import random


class Actions:

    Hue_Hub = Bridge('192.168.0.134')
    Heater = SmartPlug('192.168.0.146')
    Lighthouse = SmartPlug('192.168.0.196')
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
    ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
    ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
    ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    def __init__(self, assistant_name, user_name, user_nickname, func_obj):
        with open("intents.json") as file:
            self.phrase_data = json.load(file)
        self.assistant_name = assistant_name
        self.user_name = user_name
        self.user_nickname = user_nickname
        self.func_obj = func_obj
        self.text_response = self.phrase_data['settings']['text_response']


    def respond(self, responses):
        if type(responses) == str:
            choice = responses
        else:
            choice = responses[random.randrange(0, len(responses))]
        # if '{' in choice:
        #     self.Speak(choice.format(name=App.name))
        if self.text_response:
            print(f'{self.assistant_name}: {choice}\n')


    def time_till(self, subject, month, day, year):
        '''
        Speaks and says how many days til the subject releases.
        '''
        time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        text = f'{subject} is out in {time_till.days} days.'
        self.respond(text)


    def display_switch(self, pattern):
        '''Switches display to the mode entered as an argument. Works for PC and TV mode.'''
        if 'TV' in pattern:
            mode = 'TV'
        else:
            mode = 'PC'
        subprocess.call([f'{os.getcwd()}/Batches/{mode} Mode.bat'])
        sleep(10)
        if mode == 'PC':
            self.ahk.run_script(self.ahk_speakers, blocking=False)
        else:
            self.ahk.run_script(self.ahk_tv, blocking=False)


    def set_audio_default(self, pattern):
        '''Sets the audio device depending on the device is mentioned in the pattern.'''
        if 'pc' in pattern:
            self.ahk.run_script(self.ahk_speakers, blocking=False)
        elif 'tv' in pattern:
            self.ahk.run_script(self.ahk_tv, blocking=False)
        else:
            self.ahk.run_script(self.ahk_headphones, blocking=False)


    def toggle_heater(self, pattern):
        '''Turns the heater on or off depending on if ON or OFF is in the pattern.'''
        if 'on' in pattern:
            self.Heater.turn_on()
        elif 'off' in pattern:
            self.Heater.turn_off()


    def start_vr(self):
        '''Start VR Function.'''
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:
            self.Lighthouse.turn_on()
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    def check_time_date(self, pattern):
        '''Says the Date or time depending on which is in the pattern chosen.'''
        response = ''
        if 'time' in pattern:
            response = f'It is {dt.datetime.now().strftime("%I:%M %p")}'
        elif 'date' or 'day' in pattern:
            response = f"Today's date is {dt.datetime.now().strftime('%A, %d %B %Y')}"
        self.respond(response)
