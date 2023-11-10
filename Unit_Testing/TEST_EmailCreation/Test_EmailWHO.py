import os
import sys
import unittest
from unittest.mock import patch
import speech_recognition as sr

# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

# Importing functions from the modules
from EmailCreation.EmailWho import (
    whoIStheR, checkWho, word_to_number, ChangerTool,
    ChangerToolAdd, Top_level_domain, AddNew_or_ChooseFromStorage,
    list_emails, choose_email, storage, storageCheck, top_level_domain, num
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

# Unit test class
class TestEmailWHO(unittest.TestCase):

    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('EmailCreation.EmailWho.checkWho')
    @patch('Voice_Assistant.Speak.Speak')
    def test_whoIStheR(self, mock_speak, mock_check_who, mock_recognize_google):
        # Test cases for whoIStheR function
        test_cases = [
            ("john.doe", "john.doe@example.com"),
            ("jane.smith", "jane.smith@example.com"),
            ("alex-jones", "alex-jones@example.com")
        ]

        for spoken_name, expected_email in test_cases:
            mock_recognize_google.reset_mock()
            mock_check_who.reset_mock()

            mock_recognize_google.return_value = spoken_name
            mock_check_who.return_value = expected_email

            result = whoIStheR()

            mock_recognize_google.assert_called()
            mock_check_who.assert_called_with(spoken_name)

            self.assertEqual(result, expected_email)

    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('EmailCreation.EmailWho.Top_level_domain', return_value='gmail')
    @patch('EmailCreation.EmailWho.ChangerTool', side_effect=lambda x: x + 'modified')
    @patch('EmailCreation.EmailWho.ChangerToolAdd', side_effect=lambda x: x + 'added')
    @patch('EmailCreation.EmailWho.whoIStheR', return_value='newuser@gmail.com')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    def test_check_who_yes(self, mock_post, mock_who_is_the_r, mock_changer_tool_add, mock_changer_tool, mock_top_level_domain, mock_speak, mock_recognize_google):
        # Test case 1: User confirms the email
        mock_recognize_google.return_value = 'yes'
        result = checkWho('john')
        self.assertEqual(result, 'john@gmail.com')
        
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('EmailCreation.EmailWho.Top_level_domain', return_value='gmail')
    @patch('EmailCreation.EmailWho.ChangerTool', side_effect=lambda x: x + 'modified')
    @patch('EmailCreation.EmailWho.ChangerToolAdd', side_effect=lambda x: x + 'added')
    @patch('EmailCreation.EmailWho.whoIStheR', return_value='newuser@gmail.com')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    def test_check_who_no(self, mock_post, mock_who_is_the_r, mock_changer_tool_add, mock_changer_tool, mock_top_level_domain, mock_speak, mock_recognize_google):
      # Test case 2: User wants to change the email
     mock_recognize_google.side_effect = ['no', 'confirm']
     result = checkWho('jane')
     self.assertEqual(result, 'janemodified@gmail.com')
      
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('EmailCreation.EmailWho.Top_level_domain', return_value='gmail')
    @patch('EmailCreation.EmailWho.ChangerTool', side_effect=lambda x: x + 'modified')
    @patch('EmailCreation.EmailWho.ChangerToolAdd', side_effect=lambda x: x + 'added')
    @patch('EmailCreation.EmailWho.whoIStheR', return_value='newuser@gmail.com')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    def test_check_who_insert_letters(self, mock_post, mock_who_is_the_r, mock_changer_tool_add, mock_changer_tool, mock_top_level_domain, mock_speak, mock_recognize_google):
    # Test case 3: User wants to add letters to the email
     mock_recognize_google.side_effect = ['add a letter', 'confirm']  # First call returns 'add a letter', second call returns 'confirm'
     result = checkWho('a')
     self.assertEqual(result, 'aadded@gmail.com')

   
# Uncomment and complete these methods for further tests
#    def test_word_to_number(self):
#        pass
#    def test_ChangerTool(self):
#        pass
#    def test_ChangerToolAdd(self):
#        pass
#    def test_AddNew_or_ChooseFromStorage(self):
#        pass
#    def test_list_emails(self):
#        pass
#    def test_choose_email(self):
#        pass
#    def test_storage(self):
#        pass
#    def test_storageCheck(self):
#        pass

# Running the tests
if __name__ == '__main__':
    unittest.main()
