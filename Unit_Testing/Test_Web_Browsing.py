import os
import sys
from tkinter import messagebox
import unittest
from unittest.mock import patch
import speech_recognition as sr
import json
# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)
from Voice_Assistant.Speak import Speak
# Importing functions from the modules
from Web_BrowsingService.OpenWeb import (
   extract_words_between, webNameHandler, web_Search, 
   Website_openPage_Handler, 
   extract_words_between
)

class TestWebBrowsingService(unittest.TestCase):

    def test_extract_words_between(self):
        text = "open some website"
        result = extract_words_between(text, "open", "website")
        self.assertEqual(result, "some")

    def test_webNameHandler(self):
        webSite = "open netflix website"
        result = webNameHandler(webSite)

        Speak("opening netflix...", 0, 1.0)
        self.assertEqual(result, "https://www.netflix.com")

    def test_web_Search(self):
        url = "https://www.netflix.com"
        result = web_Search(url)
        self.assertEqual(result, url)

    @patch('Web_BrowsingService.OpenWeb.maximize_window')
    def test_Website_openPage_Handler(self, mock_maximize_window):
        url = "https://www.netflix.com"
        Website_openPage_Handler(url)
        mock_maximize_window.assert_called_once()

if __name__ == '__main__':
    unittest.main()