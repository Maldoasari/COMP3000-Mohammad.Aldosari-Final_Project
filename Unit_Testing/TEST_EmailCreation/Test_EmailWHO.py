import os
import sys
import unittest
from unittest.mock import patch, MagicMock, create_autospec
import speech_recognition as sr
import json
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
    """""
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
    def test_check_who(self, mock_post, mock_who_is_the_r, mock_changer_tool_add, mock_changer_tool, mock_top_level_domain, mock_speak, mock_recognize_google):
        # Test case 1: User confirms the email
        mock_recognize_google.return_value = 'yes'
        result = checkWho('john')
        self.assertEqual(result, 'john@gmail.com')
        print("Success test: User confirms the email\n")
         # Test case 2: User wants to change the email
        mock_recognize_google.side_effect = ['no', 'confirm']
        result = checkWho('jane')
        self.assertEqual(result, 'janemodified@gmail.com')
        print("Success test: User wants to change the email\n")
         # Test case 3: User wants to add letters to the email
        mock_recognize_google.side_effect = ['add a letter', 'confirm']  # First call returns 'add a letter', second call returns 'confirm'
        result = checkWho('a')
        self.assertEqual(result, 'aadded@gmail.com')
        print("Success test:  User wants to add letters to the email\n")
        
        # Test case 5: Speech recognition does not understand the audio
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'confirm']
        result = checkWho('unknown')
        self.assertEqual(result, 'unknown@gmail.com')  
        print("Success test: Speech recognition does not understand the audio check\n")
       
         # Test case 6: User retries
        mock_recognize_google.side_effect = ["try again", "confirm"]
        result = checkWho('mack')
        self.assertEqual(result, 'newuser@gmail.com')  
        print("Success test:  User retries\n")
        
        # Test case 7: API error
        mock_recognize_google.side_effect = [sr.RequestError(), "confirm"]
        result = checkWho('apierror')
        self.assertEqual(result, 'apierror@gmail.com')  # Assuming ChangerTool is called after RequestError
        print("Success test: API error check\n")

    def test_valid_numbers(self):
        test_cases =  {
        "zero": 0,
        "hero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11
    }
        for word, expected_number in test_cases.items():
            with self.subTest(word=word):
                self.assertEqual(word_to_number(word), expected_number)
        print("Success test: word to number functionality\n")

    def test_invalid_number(self):
        # Test case for an invalid number word
        self.assertIsNone(word_to_number("invalid"))
    
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    def test_ChangerTool(self, mock_post, mock_speak, mock_recognize_google):
        
        # Test case 1.0: Replace a letter in the string
        mock_recognize_google.side_effect = ['two', 'b']  # Replace third letter with 'b'
        result = ChangerTool('cat')
        self.assertEqual(result, 'cab')
        # Test case 1.1: Replace a letter in the string
        mock_recognize_google.side_effect = ['zero', 'x']  # Replace third letter with 'b'
        result = ChangerTool('Hello My Amigo')
        self.assertEqual(result, 'xello My Amigo')
        
        # Test case 2.0: User provides an invalid index
        mock_recognize_google.side_effect = ['five', 'confirm']  # 'five' is out of range for 'cat'
        result = ChangerTool('cat')
        self.assertEqual(result, 'cat')
        
        # Test case 2.1: User provides an invalid index
        mock_recognize_google.side_effect = ['2', 'confirm']  # 'five' is out of range for 'cat'
        result = ChangerTool('hi')
        self.assertEqual(result, 'hi')
        
        # Test case 3: Speech recognition fails to understand audio
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'two', 'b']
        result = ChangerTool('dog')
        self.assertEqual(result, 'dob')
    
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    def test_ChangerToolAdd(self, mock_post, mock_speak, mock_recognize_google):
        # Test case 1.0: Add a letter in the string
        mock_recognize_google.side_effect = ['1 and 2', 'b']  
        result = ChangerToolAdd('cat')
        self.assertEqual(result, 'cabt')
        
        # Test case 1.0: Add a number in the string
        mock_recognize_google.side_effect = ['0 and 1', '3'] 
        result = ChangerToolAdd('cat')
        self.assertEqual(result, 'c3at')
        
        # Test case 2: User provides an invalid index
        mock_recognize_google.side_effect = ['3 and 9', '1 and 3', "0 and 1", "d"] 
        result = ChangerToolAdd('cat')
        self.assertEqual(result, 'cdat')
        
        # Test case 3: Speech recognition fails to understand audio
        mock_recognize_google.side_effect = [sr.UnknownValueError(), '0 and 1', 'b']
        result = ChangerToolAdd('dog')
        self.assertEqual(result, 'dbog')
    
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('EmailCreation.EmailWho.recognizer.listen') 
    @patch('EmailCreation.EmailWho.sr.Microphone')  
    def test_AddNew_or_ChooseFromStorage(self, mock_microphone, mock_listen, mock_recognize_google):
         # Test case 1: choosing to add new
        mock_recognize_google.side_effect = ['add new']
        result = AddNew_or_ChooseFromStorage()
        self.assertEqual(result, 'add')
        
         # Test case 2: choosing storage
        mock_recognize_google.side_effect = ['storage']
        result = AddNew_or_ChooseFromStorage()
        self.assertEqual(result, 'storage')

        # Test case 3: an unrecognized command
        mock_recognize_google.side_effect = ['unrecognized command']
        result = AddNew_or_ChooseFromStorage()
        self.assertEqual(result, 'badRequest')
        
         # Test case 4: speech recognition error handling
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'add new']
        result = AddNew_or_ChooseFromStorage()
        self.assertIn(result, 'add')
    @patch('EmailCreation.EmailWho.open')
    def test_list_emails(self, mock_open):
        # Sample data to be returned by the mock
        sample_data = [
            {"email": "email1@example.com"},
            {"email": "email2@example.com"}
        ]
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(sample_data)
        emails, email_list_str, count = list_emails()
        self.assertEqual(emails, ["email1@example.com", "email2@example.com"])
        self.assertEqual(count, 2)
        expected_string = "1. email1@example.com \n 2. email2@example.com \n"
        self.assertEqual(email_list_str, expected_string)
    
    @patch('EmailCreation.EmailWho.recognizer.recognize_google')
    @patch('EmailCreation.EmailWho.sr.Microphone')
    def test_choose_email(self, mock_microphone, mock_recognize_google):
         # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  # Set the sample width (2 bytes for 16-bit audio)

        mock_microphone.return_value.__enter__.return_value = mock_audio_source

        # test case 1: Setup for choosing the first email
        mock_recognize_google.return_value = 'one'
        emails = ['email1@example.com', 'email2@example.com']
        result = choose_email(emails, "Email list", 2)
        self.assertEqual(result, 'email1@example.com')
         #test case 2:  Setup for an invalid input followed by a valid one
        mock_recognize_google.side_effect = ['invalid', 'two']
        emails = ['email1@example.com', 'email2@example.com']
        result = choose_email(emails, "Email list", 2)
        self.assertEqual(result, 'email2@example.com')
        
        # test case 3: Setup for speech recognition failure followed by success
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'one']
        emails = ['email1@example.com', 'email2@example.com']
        result = choose_email(emails, "Email list", 2)
        self.assertEqual(result, 'email1@example.com')
    
    @patch('EmailCreation.EmailWho.list_emails')
    @patch('EmailCreation.EmailWho.choose_email')
    def test_storage(self, mock_choose_email, mock_list_emails):
        #test case 1: chosing a valid email
        mock_list_emails.return_value = (['email1@example.com', 'email2@example.com'], "1. email1@example.com\n2. email2@example.com", 2)
        mock_choose_email.return_value = 'email1@example.com'
        result = storage()
        self.assertEqual(result, 'email1@example.com')
        
        # test case 2: choosing invalid email:
        mock_choose_email.return_value = None
        result = storage()
        self.assertIsNone(result, None)
    """""
    
    @patch('EmailCreation.EmailWho.list_emails')
    def test_storageCheck(self, mock_list_emails):
         # Test case 1:  when list_emails returns an empty list or a list with a single email
        for email_list in ([], ['email1@example.com']):
            mock_list_emails.return_value = email_list
            result = storageCheck()
            self.assertIsNone(result)
         #Test case 2: when list_emails returns a list with multiple emails
        mock_list_emails.return_value = ['email1@example.com', 'email2@example.com']
        result = storageCheck()
        self.assertEqual(result, ['email1@example.com', 'email2@example.com'])

# Running the tests
if __name__ == '__main__':
    unittest.main()
