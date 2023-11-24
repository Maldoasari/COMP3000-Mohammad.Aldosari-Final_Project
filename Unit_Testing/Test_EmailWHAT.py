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
from EmailCreation.EmailWhat import (
    checkSub, Subject
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestEmailWHAT(unittest.TestCase):
    @patch('EmailCreation.EmailWhat.recognizer.recognize_google')
    @patch('EmailCreation.EmailWhat.recognizer.listen')
    @patch('EmailCreation.EmailWhat.sr.Microphone')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    @patch('EmailCreation.EmailWhat.checkSub')
    def test_subject(self, mock_check_sub, mock_post, mock_speak, 
                     mock_microphone, mock_listen, 
                     mock_recognize_google):
        # test case 1: Simulate successful recognition
        mock_recognize_google.return_value = 'test subject'
        mock_check_sub.return_value = 'test subject'
        result = Subject()
        self.assertEqual(result, 'test subject')
        print("Success test: Simulate successful recognitionl\n")
        # test case 2: Simulate UnknownValueError
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'test subject retry']
        mock_check_sub.return_value = 'test subject retry'
        result = Subject()
        self.assertEqual(result, 'test subject retry')
        print("Success test: Simulate UnknownValueError\n")
        # test case 3: Simulate RequestError
        mock_recognize_google.side_effect = [sr.RequestError("API unavailable"), 'test subject retry']
        mock_check_sub.return_value = 'test subject retry'
        result = Subject()
        self.assertEqual(result, 'test subject retry')
        print("Success test: Simulate RequestError\n")
    
    @patch('EmailCreation.EmailWhat.recognizer.recognize_google')
    @patch('EmailCreation.EmailWhat.sr.Microphone')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('Voice_Assistant.Read_Email_Voice_Inputs.POST')
    @patch('EmailCreation.EmailWhat.Subject')
    def test_check_subject(self, mock_subject, mock_post, mock_speak, mock_microphone, mock_recognize_google):
         # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  # Set the sample width (2 bytes for 16-bit audio)

        mock_microphone.return_value.__enter__.return_value = mock_audio_source
         # Test case 1: user confirms the subject
        mock_recognize_google.return_value = 'yes'
        result = checkSub("test subject")
        self.assertEqual(result, 'Test subject')
        print("Success test: user confirms the subject\n")
        # Test case 2: user rewrites the subject
        mock_recognize_google.side_effect = ['no', 'yes']
        mock_subject.return_value = 'new subject'
        result = checkSub("test subject")
        self.assertEqual(result, 'new subject')
        print("Success test: user rewrites the subject\n")
         # Test case 3: speech recognition error
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'yes']
        result = checkSub("test subject")
        self.assertEqual(result, 'Test subject')
        print("Success test: speech recognition error\n")
 
if __name__ == '__main__':
    unittest.main()