import asyncio
import time
import speech_recognition as sr
from playwright.async_api import async_playwright
from Voice_Assistant.Audio_Processor import IsSpeech, save_audio_as_wav
from Web_BrowsingService.OpenWeb import click_button_by_text, extract_words_between, search_google
from Voice_Assistant.Speak import Speak
recognizer = sr.Recognizer()
status = None
highlightedText = None
async def reading_highlighted_text(page):
    global highlightedText
    highlighted_text = await page.evaluate('''() => {
       
        return document.getSelection().toString();
    }''')
    if (len(highlighted_text) <= 0):
        highlightedText = None
    else:
        highlightedText = highlighted_text
                
async def listening(page, timeout):
    global status
    global highlightedText
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
                break
            elif "read this" in recognized_text:
                await reading_highlighted_text(page) 
                if (highlightedText == None):
                    Speak("You are not selecting any text", -1, 1.0)
                    break
                else:
                    Speak(f"{highlightedText}", -1, 1.0)  
                status = False
                break
            elif "search this" in recognized_text:
                status = False
                await reading_highlighted_text(page) 
                if (highlightedText == None):
                    Speak("You are not selecting any text", -1, 1.0)
                    break
                await search_google(page, highlightedText, 1)
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
             await asyncio.sleep(1)
             if not status:
                listen_for_Taylor()
                await listening(page, timeout)
                continue
             else:   
                break
            return  


def listen_for_Taylor():
    while True:
        with sr.Microphone() as source:
            try:
                audio_data = recognizer.listen(source, timeout=2, phrase_time_limit=2) 
                text = recognizer.recognize_google(audio_data)
                if "Taylor" in text or "Tyler" in text:
                    Speak("yes!", -1, 1.0)
                    break
                else:
                    continue
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue


 