import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

from EmailCreation.EmailWho import whoIStheR
from EmailCreation.EmailWho import checkWho
from EmailCreation.EmailWho import word_to_number
from EmailCreation.EmailWho import ChangerTool
from EmailCreation.EmailWho import ChangerToolAdd
from EmailCreation.EmailWho import Top_level_domain
from EmailCreation.EmailWho import AddNew_or_ChooseFromStorage
from EmailCreation.EmailWho import list_emails, choose_email, storage, storageCheck
from EmailCreation.EmailWho import top_level_domain, num

#TEST starts here
import unittest
from unittest.mock import patch, MagicMock


class TestEmailWHO(unittest.TestCase):
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('EmailCreation.EmailWho.checkWho')
    @patch('Voice_Assistant.Speak.Speak')
    def test_who_is_the_r(self, mock_speak, mock_check_who, mock_recognize_google):
        #test cases 
        test_cases = [
            ("john.doe", "john.doe@example.com"),
            ("jane.smith", "jane.smith@example.com"),
            ("alex-jones", "alex-jones@example.com")
        ]

        for spoken_name, expected_email in test_cases:
            # Reset mocks for each iteration
            mock_recognize_google.reset_mock()
            mock_check_who.reset_mock()

            # Setup mocks for this iteration
            mock_recognize_google.return_value = spoken_name
            mock_check_who.return_value = expected_email

            # Call the function
            result = whoIStheR()

            # Check that the functions were called as expected
            mock_recognize_google.assert_called()
            mock_check_who.assert_called_with(spoken_name)

            # Check the result
            self.assertEqual(result, expected_email)

    #more tests will be added for different scenarios, like handling exceptions abd other functions

if __name__ == '__main__':
    unittest.main()