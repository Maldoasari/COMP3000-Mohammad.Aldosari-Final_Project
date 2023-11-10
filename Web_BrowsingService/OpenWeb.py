import speech_recognition as sr
from Voice_Assistant.Speak import Speak

def webHandler(webSite):
    cut_open = webSite.replace("open", "")
    cut_website = cut_open.replace("website", "")
    host = cut_website.replace(" ", "").lower()
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
