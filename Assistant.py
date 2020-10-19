# from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from pyHS100 import SmartPlug
from phue import Bridge
import datetime as dt
from ahk import AHK
import json


class Assistant:

    def __init__(self, assistant_name, user_name, user_nickname, func_obj):
        self.assistant_name = assistant_name
        self.user_name = user_name
        self.user_nickname = user_nickname
        self.func_obj = func_obj
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.Lighthouse = SmartPlug('192.168.0.196')
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    def Time_Till(self, subject, month, day, year):
        '''Speaks and says how many days til the subject releases.'''
        time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        text = f'{subject} is out in {time_till.days} days.'
        self.func_obj.Speak(text)
        print(text)


    def Toggle_Heater(self):
        try:
            if self.Heater.get_sysinfo()["relay_state"] == 0:
                self.Heater.turn_on()
            else:
                self.Heater.turn_off()
        except:
            print('Heater Error')


    def Set_Volume(self, level):
        pass


    def Roku(self, action):
        pass
