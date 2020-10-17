# from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from pyHS100 import SmartPlug
from phue import Bridge
from gtts import gTTS
import datetime as dt
from ahk import AHK
import playsound
from io import BytesIO
import os


class Assistant:

    def __init__(self, assistant_name, data):
        self.name = assistant_name
        self.phrase_data = data
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.Lighthouse = SmartPlug('192.168.0.196')
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'

    def Speak(self, text):
        tts = gTTS(text=text, lang='en')
        date_string = dt.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = f'voice{date_string}.mp3'
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)


    def Set_Scene(self, scene):
        print('Set Scene to {scene}')
        pass


    def Turn_Off_Lights(self):
        print('Turned lights off.')
        pass


    def Toggle_Heater(self):
        pass


    def Set_Volume(self, level):
        pass


    def Roku(self, action):
        pass
