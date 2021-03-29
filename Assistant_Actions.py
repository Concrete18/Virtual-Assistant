from pyHS100 import SmartPlug
from phue import Bridge
from ahk import AHK
from time import sleep
import datetime as dt
import subprocess
import sys
import re
import os
import random
import psutil


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


    @staticmethod
    def assistant_status(match_dict):
        '''
        Opens folder given as folder_dir.
        '''
        # TODO finish assistant_status function
        response = random.choice(match_dict['responses'])
        # virtual memory
        virtual_mem = psutil.virtual_memory()
        total_mem = virtual_mem.total
        used_mem = virtual_mem.used
        # battery ifno
        battery = psutil.sensors_battery()
        if battery != None:
            print('Percent:', battery.percent)
            print('Seconds Left:', battery.secsleft)
            print('Plugged In:', battery.power_plugged)
            print(battery)
            battery_info = f's'
            response += battery_info
        response = response.replace('{assistant_name}', self.assistant_name)
        return response


    @staticmethod
    def open_folder(folder):
        '''
        Opens folder given as folder_dir.
        '''
        # TODO finish open_folder function
        folders = {
            'Home Control Interface':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Home Control Interface.lnk',
            'Timed Sleep or Shutdown':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed Sleep or Shutdown.lnk',
            'Media Release Updater':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Media Release Updater.lnk'
        }
        for folder_name, folder_dir in folders.items():
            if folder in folder_name:
                subprocess.Popen(rf'explorer /select, {folder_dir}')
                return


    @staticmethod
    def run_script(script):
        '''
        Runs script based on given script name if it is in the scripts dictionary.
        '''
        # TODO finish run_script function
        scripts = {
            'Home Control Interface':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Home Control Interface.lnk',
            'Timed Sleep or Shutdown':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed Sleep or Shutdown.lnk',
            'Media Release Updater':r'D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Media Release Updater.lnk'
        }
        for script_name, script_dir in scripts.items():
            if script in script_name:
                subprocess.run([sys.executable, f'{script}.lnk'], cwd=os.path.dirname(script_dir))
                return
        print('No script found with that name.')


    def display_switch(self, pattern):
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
            self.ahk.run_script(self.ahk_speakers, blocking=False)
        else:
            self.ahk.run_script(self.ahk_tv, blocking=False)


    def set_audio_default(self, pattern):
        '''
        Sets the audio device depending on the device is mentioned in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'pc' in pattern:
            self.ahk.run_script(self.ahk_speakers, blocking=False)
        elif 'tv' in pattern:
            self.ahk.run_script(self.ahk_tv, blocking=False)
        else:
            self.ahk.run_script(self.ahk_headphones, blocking=False)


    def start_vr(self):
        '''
        Start VR Function.
        '''
        # runs SteamVR
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:  # turns on Lighthouse if it is off
            self.Lighthouse.turn_on()


    @staticmethod
    def check_time_date(pattern) -> str:
        '''
        Says the Date or time depending on which is in the pattern chosen.

        Arguments:

        pattern -- matched response from phrase_matcher
        '''
        if 'time' in pattern:
            current_time = dt.datetime.now().strftime("%I:%M %p")
            if current_time[0] == '0':
                current_time = current_time[1:]
            return f'It is {current_time}'
        elif 'tomorrow' in pattern:
            tomorrow = dt.datetime.today() + dt.timedelta(days=1)
            return f"It is {tomorrow.strftime('%A, %B %d, %Y')}"
        elif 'date' or 'day' in pattern:
            return f"It is {dt.datetime.now().strftime('%A, %B %d, %Y')}"


    @staticmethod
    def time_till(month, day, year=None, subject=None,):
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


    @staticmethod
    def time_till_custom(pattern):
        '''
        Gives the time till the given date arrives.
        '''
        date_entry = re.search(rf'/d', pattern)
        month, day, year = date_entry.split('-')
        if year == None:
            year = dt.datetime.now().year

        time_till = dt.datetime.strptime(f'{month}-{day}-{year}', f'%m-%d-%Y') - dt.datetime.now()

        return f'{time_till.days} days till {month}/{day}/{year}.'
