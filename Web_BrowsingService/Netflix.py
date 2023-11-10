from playwright.sync_api import sync_playwright
import time
import pygetwindow as gw
import speech_recognition as sr
from  Voice_Assistant.Speak  import Speak

recognizer = sr.Recognizer()

def NetflixHandler(url):
    Speak("Just to give you a haeds up, if you want to exit say exit netflix", -1, 1.0)
    with sync_playwright() as p:
     timeout = 120000
     browser = p.chromium.launch(headless=False)
     NetFlix_page = browser.new_page()
     NetFlix_page.set_default_timeout(timeout)  # 120 seconds timeout
     NetFlix_page.goto(url)
     
       # Maximize the window using pygetwindow
     windows = gw.getWindowsWithTitle('')
     for window in windows:
            if "chromium" in window.title.lower():
                window.maximize()
                break
     while True:
       time1 = timeout
       NetFlix_page.set_default_timeout(time1)
       with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:    
         recognized_text = recognizer.recognize_google(audio) 
         if"exit" in recognized_text:
           break
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
    
   
    
