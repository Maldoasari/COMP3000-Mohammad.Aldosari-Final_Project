import re
import speech_recognition as sr
from Voice_Assistant.Speak import Speak

def extract_words_between(text, first_word, second_word):
    pattern = fr"{first_word}\s+((?:\w+\s*)+?){second_word}"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        return "Words not found"
    
def webHandler(webSite):
    get_web = extract_words_between(webSite, "open", "website")
    #cut_open = webSite.replace("open", "")
    #cut_website = cut_open.replace("website", "")
    host = get_web.replace(" ", "").lower()
    print(host)
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
    
#openWeb()
