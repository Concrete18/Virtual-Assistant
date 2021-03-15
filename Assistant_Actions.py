from pyHS100 import SmartPlug
from phue import Bridge
from ahk import AHK
from time import sleep
import datetime as dt
import subprocess
import sys
import os


class Action:

	# obj init
    Hue_Hub = Bridge('192.168.0.134')
    Heater = SmartPlug('192.168.0.146')
    Lighthouse = SmartPlug('192.168.0.196')
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
    # var init
    ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
    ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
    ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    @classmethod
    def time_till(cls, month, day, year=None, subject=None,) -> str:
        '''
        Gives the time till the given date arrives.
        '''
        if year == None:
            year = dt.datetime.now().year
        # time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        time_till = dt.datetime.strptime(f'{month}-{day}-{year}', f'%m-%d-%Y') - dt.datetime.now()
        if subject != None:
            return f'{subject} is in {time_till.days} days.'
        else:
            return f'{time_till.days} days till {month}/{day}/{year}.'


    @classmethod
    def open_folder(cls, folder_dir):
        '''
        Opens folder given as folder_dir.
        '''
        subprocess.Popen(rf'explorer /select, {folder_dir}')
        # TODO add open_folder function


    @classmethod
    def run_script(cls, script):
        '''
        Runs script based on given script name if it is in the scripts dictionary.
        '''
        scripts = {
            'Home Control Interface':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Home Control Interface.lnk',
            'Timed Sleep or Shutdown':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed Sleep or Shutdown.lnk',
            'Media Release Updater':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Media Release Updater.lnk'
        }
        for script_name, script_dir in scripts.items():
            if script in script_name:
                subprocess.run([sys.executable, script], cwd=os.path.dirname(script_dir))
                return
        print('No script found with that name.')


    @classmethod
    def display_switch(cls, pattern):
        '''
        Switches display to the mode that matches the pattern argument. Works for PC and TV mode.

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
            cls.ahk.run_script(cls.ahk_speakers, blocking=False)
        else:
            cls.ahk.run_script(cls.ahk_tv, blocking=False)


    @classmethod
    def set_audio_default(cls, pattern):
        '''
        Sets the audio device depending on the device is mentioned in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'pc' in pattern:
            cls.ahk.run_script(cls.ahk_speakers, blocking=False)
        elif 'tv' in pattern:
            cls.ahk.run_script(cls.ahk_tv, blocking=False)
        else:
            cls.ahk.run_script(cls.ahk_headphones, blocking=False)


    @classmethod
    def toggle_heater(cls, pattern):
        '''
        Turns the heater on or off depending on if ON or OFF is in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'on' in pattern:
            cls.Heater.turn_on()
            return 'Turned on the heater.'
        elif 'of' in pattern:
            cls.Heater.turn_off()
            return 'Turned off the heater.'


    @classmethod
    def start_vr(cls):
        '''
        Start VR Function.
        '''
        # runs SteamVR
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")
        if cls.Lighthouse.get_sysinfo()["relay_state"] == 0:  # turns on Lighthouse if it is off
            cls.Lighthouse.turn_on()


    @classmethod
    def check_time_date(cls, pattern) -> str:
        '''
        Says the Date or time depending on which is in the pattern chosen.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'time' in pattern:
            current_time = dt.datetime.now().strftime("%I:%M %p")
            print(current_time[0])
            if current_time[0] == '0':
                current_time = current_time[1:]
            return f'It is {current_time}'
        elif 'date' or 'day' in pattern:
            return f"Today's date is {dt.datetime.now().strftime('%A, %B %d, %Y')}"
