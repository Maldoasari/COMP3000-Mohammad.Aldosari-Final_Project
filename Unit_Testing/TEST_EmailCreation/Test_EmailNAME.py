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
from EmailCreation.EmailName import (
    checkName, ReadName
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestReadName(unittest.TestCase):

    @patch('EmailCreation.EmailName.recognizer.recognize_google')
    @patch('EmailCreation.EmailName.sr.Microphone')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('EmailCreation.EmailName.checkName')
    def test_read_name(self, mock_check_name, mock_speak, mock_microphone, mock_recognize_google):
          # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  # Set the sample width (2 bytes for 16-bit audio)

        mock_microphone.return_value.__enter__.return_value = mock_audio_source
        # test case 1: Simulate successful recognition of the name
        mock_recognize_google.return_value = 'john doe'
        mock_check_name.return_value = 'John Doe'
        result = ReadName()
        self.assertEqual(result, 'John Doe')
        print("Success test: Simulate successful recognition of the name\n")
        # test case 2: Simulate UnknownValueError
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'jane doe']
        mock_check_name.return_value = 'Jane Doe'
        result = ReadName()
        self.assertEqual(result, 'Jane Doe')
        print("Success test: Simulate UnknownValueError\n")
        # test case 3: Simulate RequestError
        mock_recognize_google.side_effect = [sr.RequestError("API unavailable"), 'alex smith']
        mock_check_name.return_value = 'Alex Smith'
        result = ReadName()
        self.assertEqual(result, 'Alex Smith')
        print("Success test: Simulate RequestError\n")

    
    @patch('EmailCreation.EmailName.recognizer.recognize_google')
    @patch('EmailCreation.EmailName.sr.Microphone')
    @patch('Voice_Assistant.Speak.Speak')
    @patch('EmailCreation.EmailName.ReadName')
    def test_check_name(self, mock_read_name, mock_speak, mock_microphone, mock_recognize_google):
          # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  # Set the sample width (2 bytes for 16-bit audio)

        mock_microphone.return_value.__enter__.return_value = mock_audio_source
         # Test case 1: user confirms the name
        mock_recognize_google.return_value = 'yes'
        result = checkName("john space doe")
        self.assertEqual(result, 'John Doe')
        print("Success test: user confirms the name\n")
         # Test case 2: user rewrites the name
        mock_recognize_google.side_effect = ['no', 'yes']
        mock_read_name.return_value = 'Jane Doe'
        result = checkName("john space doe")
        self.assertEqual(result, 'Jane Doe')
        print("Success test: user rewrites the name\n")
         # Test case 3: speech recognition error
        mock_recognize_google.side_effect = [sr.UnknownValueError(), 'yes']
        result = checkName("john space doe")
        self.assertEqual(result, 'John Doe')
        print("Success test: speech recognition error\n")
if __name__ == '__main__':
    unittest.main()