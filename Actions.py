from time import sleep
import datetime as dt
import subprocess

class Actions:

    def time_till(self, subject, month, day, year):
        '''Speaks and says how many days til the subject releases.

        Arguments:

        subject -- Subject that is released

        month -- Subject's month of release

        day -- Subject's day of release

        year -- Subject's year of release
        '''
        time_till = dt.datetime(month=month, day=day, year=year) - dt.datetime.now()
        text = f'{subject} is out in {time_till.days} days.'
        self.respond(text)


    def display_switch(self, pattern):
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


    def set_audio_default(self, pattern):
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


    def toggle_heater(self, pattern):
        '''Turns the heater on or off depending on if ON or OFF is in the pattern.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        if 'on' in pattern:
            self.Heater.turn_on()
        elif 'off' in pattern:
            self.Heater.turn_off()


    def start_vr(self):
        '''Start VR Function.'''
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:  # turns on Lighthouse if it is off
            self.Lighthouse.turn_on()
        # runs SteamVR
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    def check_time_date(self, pattern):
        '''Says the Date or time depending on which is in the pattern chosen.

        Arguments:

        pattern -- matched response from Phrase_Matcher
        '''
        response = ''
        if 'time' in pattern:
            response = f'It is {dt.datetime.now().strftime("%I:%M %p")}'
        elif 'date' or 'day' in pattern:
            response = f"Today's date is {dt.datetime.now().strftime('%A, %d %B %Y')}"
        self.respond(response)
