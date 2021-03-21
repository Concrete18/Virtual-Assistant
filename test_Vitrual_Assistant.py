import unittest
from Virtual_Assistant import Assistant


class Test_Virtual_Assistant(unittest.TestCase):


    def test_phrase_matcher(self):
        '''
        Tests phrase_matcher to be sure it returns the proper tags.
        '''
        Test = Assistant()
        Test.debug = 0

        test_strings = {
        'Can you turn on my lights please?':'turn_on_lights',
        'would you turn off my lights?':'turn_off_lights',
        'would you turn on backlight?':'backlight',
        'Do you have any good jokes?':'joke',
        'would you kindly turn on my heater?':'toggle_heater',
        'switch audio to my pc please?':'set_audio_default',
        'how are you doing today?':'ask_about_assistant',
        'thanks for all the help?':'appreciation',
        'thanks.':'appreciation',
        'thanks!':'appreciation',
        'Hello assistant':'greeting',
        'start vr':'start_vr',
        'what is todays date?':'date_time',
        'what time is it?':'date_time',
        'When is Christmas?':'time_till_christmas',
        'When is Thanksgiving':'time_till_thanksgiving',
        'How many days till 12-10?':'time_till_custom',
        'How many days till 2-8?':'time_till_custom',
        "How long till March 8th":'time_till_custom',
        'How many days till March 8th?':'time_till_custom',
        }
        for string, tag in test_strings.items():
            self.assertEqual(Test.phrase_matcher(string)['tag'], tag)


if __name__ == '__main__':
    unittest.main()
