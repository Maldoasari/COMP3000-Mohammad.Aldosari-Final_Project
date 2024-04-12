import speech_recognition as sr
from playwright.sync_api import sync_playwright
from Voice_Assistant.Speak import Speak
from Web_BrowsingService.OpenWeb import click_button_by_text, extract_words_between, maximize_window, scroll_down_page, scroll_up_page, search_google
recognizer = sr.Recognizer()

def Website_Browsing_openPage_Handler(url):
    Speak("openning google serach engine. Just to give you a haeds up, if you want to exit say exit service", -1, 1.0)
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
                if "exit service" in recognized_text:
                    break
                elif "scroll up" in recognized_text:
                    scroll_up_page(page, recognized_text)
                    continue
                elif "scroll down" in recognized_text:
                    scroll_down_page(page, recognized_text)
                    continue
                elif "click on" in recognized_text and "button" in recognized_text:
                    extracted_word = extract_words_between(recognized_text, "click on", "button", "Inbetween")
                    click_button_by_text(page, extracted_word, "text")
                    print(extracted_word)
                    continue
                elif "search for" in recognized_text:
                    extracted_word = extract_words_between(recognized_text, "search for", " ", None)
                    print(extracted_word)
                    search_google(page, extracted_word, 1)
                    #print(f"Second link after searching for 'machine learning': {second_link}")
                    continue
                elif "go to" in recognized_text:    
                    continue
                else:
                    continue
             except sr.WaitTimeoutError:
                continue
             except sr.UnknownValueError:
                continue