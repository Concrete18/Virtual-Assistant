import unittest
from Functions import Func


class Test_Phrase_Matcher(unittest.TestCase):


    def test_Phrase_Matcher(self):
        '''Tests Phrase_Matcher to be sure it returns the proper tags.'''
        func = Func()
        func.debug = 0

        test_strings = {
        'Can you turn on my lights please?':'turn_on_lights',
        'would you turn off my lights?':'turn_off_lights',
        'would you turn on backlight?':'backlight',
        'Do you have any good jokes?':'joke',
        'would you kindly turn on my heater?':'toggle_heater',
        'switch audio to my pc please?':'set_audio_default',
        'When does cyberpunk release?':'cyberpunk',
        'When does Cyberpunk 2077 come out?':'cyberpunk',
        'how are you doing today?':'ask_about_assistant',
        'thanks for all the help?':'appreciation',
        'Hello assistant':'greeting',
        'start vr':'start_vr',
        }
        for string, tag in test_strings.items():
            self.assertEqual(func.Phrase_Matcher(string)[0], tag)


if __name__ == '__main__':
    unittest.main()