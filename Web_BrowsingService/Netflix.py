import re
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
         elif "scroll up" in recognized_text:
                    scroll_up_page(NetFlix_page, recognized_text)
                    continue
         elif "scroll down" in recognized_text:
                    scroll_down_page(NetFlix_page, recognized_text)
                    continue
         elif "click on" in recognized_text and "button" in recognized_text:
                    extracted_word = extract_words_between(recognized_text, "click on", "button")
                    click_button_by_text(NetFlix_page, extracted_word)
                    continue
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
    
def scroll_up_page(page, text):
    numbers = re.findall(r'\b\d+\b', text)
    int_numbers = [int(nums) for nums in numbers]
    if int_numbers:
      for _ in range(30):
        page.evaluate(f"window.scrollBy(0, -{int_numbers});")
        time.sleep(0.2)
    else:
      for _ in range(30):
        page.evaluate("window.scrollBy(0, -200);")
        time.sleep(0.2)
    #page.evaluate("window.scrollBy(0, -300);")
    
def scroll_down_page(page, text):
    numbers = re.findall(r'\b\d+\b', text)
    int_numbers = [int(nums) for nums in numbers]
    print(int_numbers)
    if int_numbers:
      for _ in range(30):
        page.evaluate(f"window.scrollBy(0, {int_numbers});")
        time.sleep(0.2)
    else:
      for _ in range(30):
        page.evaluate("window.scrollBy(0, 200);")
        time.sleep(0.2)
        
def click_button_by_text(page, button_text):
    print(button_text)
    page.click(f"text={button_text}")

def extract_words_between(text, first_word, second_word):
    pattern = fr"{first_word}\s+((?:\w+\s*)+?){second_word}"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        return "Words not found"

  