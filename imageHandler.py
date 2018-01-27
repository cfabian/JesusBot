import random
from random import randint
from datetime import datetime
import urllib
from urllib import request

def getCat():
    url = "http://random.cat/meow"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
        image = page[9 : -2].replace("\\", "")
        urllib.request.urlretrieve(image, "images/cat.jpg")
        
def getDog():
    url = "https://random.dog"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
        begining_index = page.find("<img id=") + 23
        ending_index = page.find(".jpg") + 4
        if begining_index == 22 or ending_index == 3:
            getDog()
        
        else :
            image = page[begining_index : ending_index]
            urllib.request.urlretrieve(url + "/" + image, "images/dog.jpg")
            
dankIndex = 45000
def getDankmeme():
    global dankIndex
    url = "https://www.reddit.com/r/dankmemes/"
    req = urllib.request.Request(url, headers = {'User-agent': 'Jesus'})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
        
        begining_index = page.find("link", dankIndex)
        dankIndex = begining_index
        begining_index = page.find("data-url=", dankIndex) + 10
        dankIndex = begining_index
        
        ending_index = page.find("\"", dankIndex)
        
        rank = page.find("data-rank", dankIndex) + 11
        if page[rank : rank + 2] == "25":
            dankIndex = 45000
        
        image = page[begining_index : ending_index]
        print(image)
        extension = image[-3 : ]
        
        urllib.request.urlretrieve(image, "images/dankmeme.jpg")