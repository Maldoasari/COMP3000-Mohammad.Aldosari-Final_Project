import re
import speech_recognition as sr
from playwright.sync_api import sync_playwright
import time
import pygetwindow as gw
from  Voice_Assistant.Speak  import Speak

def extract_words_between(text, first_word, second_word):
    pattern = fr"{first_word}\s+((?:\w+\s*)+?){second_word}"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        return "Words not found"
    
def webNameHandler(webSite):
    get_web = extract_words_between(webSite, "open", "website",  "Inbetween")
    #cut_open = webSite.replace("open", "")
    #cut_website = cut_open.replace("website", "")
    host = get_web.replace(" ", "").lower()
    #host = Clone_Name.split()[-2]
    url = f"https://www.{host}.com"
    Speak(f"opening {host}...", 0, 1.0)
    return url
    

def web_Search(url):
    if(url == "https://www.netflix.com"):
        url = url
        #NetflixHandler(url)
    elif(url == "https://www.primevideo.com"):
        url = url
    else:
        url = url
        #print("no url found")
     #browser.close()
    return url

recognizer = sr.Recognizer()

def maximize_window():
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if "chromium" in window.title.lower():
            window.maximize()
            break

def Website_openPage_Handler(url):
    Speak("Just to give you a haeds up, if you want to exit say exit", -1, 1.0)
    with sync_playwright() as p:
        timeout = 120000
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(timeout)  
        page.goto(url)

        maximize_window()  

        while True:
            time1 = timeout
            page.set_default_timeout(time1)
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                try:
                    recognized_text = recognizer.recognize_google(audio)
                    if "exit" in recognized_text:
                        break
                    elif "scroll up" in recognized_text:
                        scroll_up_page(page, recognized_text)
                        continue
                    elif "scroll down" in recognized_text:
                        scroll_down_page(page, recognized_text)
                        continue
                    elif "click on" in recognized_text and "button" in recognized_text:
                        extracted_word = extract_words_between(recognized_text, "click on", "button", "Inbetween")
                        click_button_by_text(page, extracted_word)
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
    if int_numbers:
      for _ in range(30):
        page.evaluate(f"window.scrollBy(0, {int_numbers});")
        time.sleep(0.2)
    else:
      for _ in range(30):
        page.evaluate("window.scrollBy(0, 200);")
        time.sleep(0.2)
        
def click_button_by_text(page, button_text):
    page.click(f"text={button_text}")

def extract_words_between(text, first_word, second_word=None, type=None):
    if type == "Inbetween" and second_word:
        pattern = fr"{first_word}\s+((?:\w+\s*)+?){second_word}"
    else:
        pattern = fr"{first_word}\s+((?:\w+\s*)+)"
    
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        return None
    
def search_google(page, query, n):
    input_locator = page.locator("textarea[name='q']")
    input_locator.type(f"{query}")
    input_locator.press("Enter")
    
    
def get_nth_link_after_search(page, n):
    nth_link = page.locator('a').nth(n)
    return nth_link.get_attribute('href') if nth_link else None

    
    

  
