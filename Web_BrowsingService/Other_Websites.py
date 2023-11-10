from playwright.sync_api import sync_playwright
import time
import pygetwindow as gw

def OtherWebHandler(url):
    with sync_playwright() as p:
     browser = p.chromium.launch(headless=False)
     Other_page = browser.new_page()
     Other_page.set_viewport_size({"width": 1920, "height": 1080})

     Other_page.set_default_timeout(120000)  # 120 seconds timeout
     Other_page.goto(url)
    
      # Maximize the window using pygetwindow
     windows = gw.getWindowsWithTitle('')
     for window in windows:
            if "chromium" in window.title.lower():
                window.maximize()
                break
     time.sleep(2)
     #NetFlix_page.click('#signIn')
     time.sleep(3)
     input("Press any key to exit...")