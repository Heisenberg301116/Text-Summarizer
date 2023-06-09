# ========================================================================    Fetching API key from .env file    ==================================================

from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('api_key')      # fetching API key

# ========================================================================    Main    =============================================================================

import sys

#print("File name = ", sys.argv[0])
link = ""
topic = ""
file_name = ""
model_name = ""

for i in range(1, len(sys.argv)):
    j = sys.argv[i]
    #print("j = ", j , " and type of j = ", type(j))
    
    if j=='--link':
        link = sys.argv[i+1]

    elif j=='--keywords':
        topic = sys.argv[i+1]

    elif j=='--out':
        file_name = sys.argv[i+1]

    elif j=='--model':
        model_name = sys.argv[i+1]

# ========================================================================    Selenium     =============================================================================

from selenium import webdriver      # to automatically make selenium open up the web browser
from selenium.webdriver.common.by import By     # for explicit wait to represent the class name
from selenium.webdriver.support.ui import WebDriverWait     # for explicit wait
from selenium.webdriver.support import expected_conditions as EC     # for explicit wait to mention the condition until which if not satisfied you have to wait
import time
from selenium.webdriver.common.keys import Keys


import os       # to specify chrome driver directory to selenium
os.environ['PATH'] += r"D:\5th Sem\Intern Project\Web Scrapping Python 3.9\Selenium\Selenium Drivers"

web = webdriver.Chrome()       # Instantiating the class of chrome driver because we want to automate our chrome browser using selenium

web.maximize_window() 
#web.get("https://www.wikipedia.org/")       # fetching wiki website
web.get(link)

# Typing 'India' inside search box of wiki
web.implicitly_wait(5)
Search_box = web.find_element("id", "searchInput")
Search_box.send_keys("India")

# Clicking on the search button:
search_button = web.find_element("xpath", "/html/body/div[3]/form/fieldset/button")
search_button.click()

url = web.current_url       # to fetch url of the current page

# =======================================================================    Open AI Summarization script   ============================================================
import os
import openai

def Summarize(chunk, model_name):
    #print("chunk = ",chunk)
    openai.api_key = (f'{key}')

    if(model_name == "gpt-3.5-turbo"):
        chunk = chunk + "\n\nTl;dr",

        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": chunk[0]}],
        max_tokens=193,
        temperature=0,
        )
        return (response.choices[0]['message'])['content']
    
    else:               # if the model is ada or davinci
        response = openai.Completion.create(
        #model="text-davinci-003",
        #model="text-ada-001",
        model = model_name,
        prompt = chunk + "\n\nTl;dr",
        temperature = 0.7,
        max_tokens = 500,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 1
        )
        #print("chunk summary = ", response["choices"][0]["text"])
        return (response["choices"][0]["text"])

# =======================================================================    Beautiful Soup     ======================================================================================

import requests     # this module is used to use http GET and POST requests
from bs4 import BeautifulSoup   
import sys      # to display the html content as the default print() statement can't be used to display html encoded content
import re

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


r = requests.get(url)       # <Response [200]>
soup = BeautifulSoup(r.text, "html.parser")        # soup contains html content of the page      

content = ""
chunk = ""

tag = soup.find_all('h2')
content = ""        # content will contain our final text under Bio-diversity section
for i in tag:       # 'i' represents the HTML code of all the 'h2' html tags
    if i.text == topic:        # if any h2 tag has text 'Biodiversity' => it is our required search container
        for j in i.next_siblings:       # under 'h2' tags are 'p' tags which actually contains all the text content of 'Biodiversity' section of wiki page
            if j.name == 'h2':     # once all the 'p' tags are iterated, we will encounter the next 'h2' tag of 'Politics' section. => break out of loop as our scrapping is completed
                break
            elif j.name == 'p':     # if it is a 'p' tag extract info from it
                content = content + j.text

# ===================================================== Splitting content into chunks and finding summary for each chunk ================================================

import re

def split(delimiters, string, maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)

delimiters = ". ", "\n"
chunks = split(delimiters, content)

summary = ""
for chunk in chunks:
    #print("===============================> type chunnk = ", type(chunk))
    summary = summary + Summarize(chunk, model_name)

print("Summary of the context = ", summary)     # overall summary of the whole bio-diversity section


# ============================================================ Exporting content into json file ========================================================================

if(file_name != ""):      # if 'out' flag was passed as a command line in the terminal
    import json

    data = {
        "link": link,
        "keywords": topic,
        "summary": summary
    }

    with open(file_name, 'w') as fp:
        json.dump(data, fp)

exit()