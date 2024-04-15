import asyncio
import speech_recognition as sr
from playwright.async_api import async_playwright
from Web_BrowsingService.OpenWeb import click_button_by_text, extract_words_between, search_google
from Voice_Assistant.Speak import Speak
recognizer = sr.Recognizer()
status = None
    
async def reading_highlighted_text(page):
    highlighted_text = await page.evaluate('''() => {
       
        return document.getSelection().toString();
    }''')
    Speak(f"{highlighted_text}", -1, 1.0)            
async def listening(page, timeout):
    global status
    while True:
        page.set_default_timeout(timeout)
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            recognized_text = recognizer.recognize_google(audio)
            if "exit service" in recognized_text:
                status = True
                Speak("exiting service", -1, 1.0)
                break
            elif "scroll up" in recognized_text:
                break
            elif "scroll down" in recognized_text:
                break
            elif "click on" in recognized_text and "button" in recognized_text:
                extracted_word = await extract_words_between(recognized_text, "click on", "button", "Inbetween")
                click_button_by_text(page, extracted_word, "text")
                break
            elif "search for" in recognized_text:
                extracted_word = await extract_words_between(recognized_text, "search for", " ", None)
                await search_google(page, extracted_word, 1)
                status = False
                await asyncio.sleep(1)
                break
            elif "read this" in recognized_text:
                await reading_highlighted_text(page) 
                status = False
                break
            elif "go to" in recognized_text:    
                break
            else:
                break
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue

async def Website_Browsing_openPage_Handler(url):
    global status
    status = False
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch(headless=False)
            page = await browser.new_page()
            timeout = 120000
            page.set_default_timeout(timeout) 
            
            await page.goto(url)
            while True:
             if not status:
                await asyncio.sleep(1)
                await listen_for_Taylor()
                await listening(page, timeout)
                continue
             else:   
                break
            return  

async def listen_for_Taylor():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
             audio = recognizer.listen(source, timeout=1)
            except sr.WaitTimeoutError:
                continue
        try:
            text = recognizer.recognize_google(audio)
            if "Taylor" in text:
                Speak("yes!", -1, 1.0)
                break
            else:
                pass
        except sr.UnknownValueError:
            pass