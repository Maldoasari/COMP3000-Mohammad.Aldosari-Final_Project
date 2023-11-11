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
from EmailCreation.EmailCheck import check
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestEmailCheck(unittest.TestCase):
    @patch('EmailCreation.EmailCheck.recognizer.recognize_google')
    @patch('EmailCreation.EmailCheck.sr.Microphone')
    def test_check(self, mock_mic, mock_recognize):
        
         # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  # Set the sample width (2 bytes for 16-bit audio)

        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.return_value = "yes"
        result = check()
        self.assertTrue(result, True)
        

if __name__ == '__main__':
    unittest.main()