import unittest
from Assistant import Assist


class Test_Phrase_Matcher(unittest.TestCase):


    def test_Phrase_Matcher(self):
        '''Tests Phrase_Matcher to be sure it returns the proper tags.'''
        test = Assist('Clara', 'Michael', 'Concrete')
        test.debug = 0

        test_strings = {
        'Can you turn on my lights please?':'turn_on_lights',
        'would you turn off my lights?':'turn_off_lights',
        'would you turn on backlight?':'backlight',
        'Do you have any good jokes?':'joke',
        'would you kindly turn on my heater?':'toggle_heater',
        'switch audio to my pc please?':'set_audio_default',
        'how are you doing today?':'ask_about_assistant',
        'thanks for all the help?':'appreciation',
        'Hello assistant':'greeting',
        'start vr':'start_vr',
        'what is todays date?':'date_time',
        'what time is it?':'date_time',
        }
        for string, tag in test_strings.items():
            self.assertEqual(test.phrase_matcher(string)['tag'], tag)


if __name__ == '__main__':
    unittest.main()
