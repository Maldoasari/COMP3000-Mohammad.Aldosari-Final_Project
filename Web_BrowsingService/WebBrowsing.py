import asyncio
import re
import playwright
import speech_recognition as sr
from playwright.async_api import async_playwright

from Web_BrowsingService.OpenWeb import click_button_by_text, extract_words_between, search_google

recognizer = sr.Recognizer()
status = False
prev_url = None
async def handle_url_change(new_url):
    print("New URL:", new_url)
    
async def handle_navigation(request):
    global prev_url
    for key, value in request.headers.items():
        if key == "referer":
          prev_url = value
              #print(f"{key}: {value}")
              
async def listening(page, timeout):
    global status
    global prev_url
    while True:
        time1 = timeout
        page.set_default_timeout(time1)
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            recognized_text = recognizer.recognize_google(audio)
            print(recognized_text)
            if "exit service" in recognized_text:
                status = True
                break
            elif "scroll up" in recognized_text:
                continue
            elif "scroll down" in recognized_text:
                continue
            elif "click on" in recognized_text and "button" in recognized_text:
                extracted_word = await extract_words_between(recognized_text, "click on", "button", "Inbetween")
                click_button_by_text(page, extracted_word, "text")
                continue
            elif "search for" in recognized_text:
                geturl = prev_url
                extracted_word = await extract_words_between(recognized_text, "search for", " ", None)
                await search_google(page, extracted_word, 1, geturl)
                status = False
                break
            elif "go to" in recognized_text:    
                continue
            else:
                continue
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue

async def Website_Browsing_openPage_Handler(url):
    global status
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch(headless=False)
            page = await browser.new_page()
            timeout = 120000
            page.set_default_timeout(timeout) 
            page.on('request', handle_navigation)
            # Navigate to the initial URL
            await page.goto(url)
            while True:
             if not status:
                await asyncio.sleep(1)
                await listening(page, timeout)
                await asyncio.sleep(3)
                continue
             else:   
                break
            return  

