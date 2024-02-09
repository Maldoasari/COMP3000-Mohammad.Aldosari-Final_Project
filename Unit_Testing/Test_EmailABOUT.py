import os
import sys
import unittest
from unittest.mock import patch, MagicMock, create_autospec
import speech_recognition as sr
# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

# Importing functions from the modules
from EmailCreation.EmailAbout import (
    edit_message, checkmsg, Organise_Msg, ReadMsg
)

class TestEmailAbout(unittest.TestCase):
    @patch('EmailCreation.EmailAbout.recognizer.recognize_google')
    @patch('EmailCreation.EmailAbout.sr.Microphone')
    def test_ReadMsg(self, mock_mic, mock_recognize):
         # Create an autospec for AudioSource including necessary attributes
        mock_audio_source = create_autospec(sr.AudioSource, instance=True)
        mock_audio_source.stream = MagicMock()
        mock_audio_source.CHUNK = 1024
        mock_audio_source.SAMPLE_RATE = 44100
        mock_audio_source.SAMPLE_WIDTH = 2  

        #Test case 1: user confirms msg 
        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.side_effect = ["test message", 'yes']
        result = ReadMsg()
        self.assertEqual(result, "Test message")
        
        #Test case 2: user rewrite msg 
        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.side_effect = ["test message", 'no', 'new test message', 'yes']
        result = ReadMsg()
        self.assertEqual(result, "New test message")
 
        #Test Case 3: UnknownValueError msg and users tries to chnage the msg:
        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.side_effect = [sr.UnknownValueError, 'Msg', sr.UnknownValueError, "no", 'new test message', 'yes']
        result = ReadMsg()
        self.assertEqual(result, "New test message")
        
        #Test case 4: user want to modify msg:
        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.side_effect = ['this is the message', "edit", "1", 'new test message', 'yes']
        result = ReadMsg()
        self.assertEqual(result, "New test message")
        
         #Test case 4: user want to modify msg but chosses an invalid index:
        mock_mic.return_value.__enter__.return_value = mock_audio_source
        mock_recognize.side_effect = ['this is the message', "edit", "3", "1", 'new test message', 'yes']
        result = ReadMsg()
        self.assertEqual(result, "New test message")
        

    def test_organisinMSG(self):
        self.assertEqual(Organise_Msg("hello comma world"), "hello, world")
        self.assertEqual(Organise_Msg("end of sentence period"), "end of sentence.")
        self.assertEqual(Organise_Msg("start new line here"), "start \n here")
        self.assertEqual(Organise_Msg("start new line here comma"), "start \n here,")
        message = "first sentence period new line second sentence comma and more"
        expected = "first sentence. \n second sentence, and more"
        self.assertEqual(Organise_Msg(message), expected)
        
if __name__ == '__main__':
    unittest.main()