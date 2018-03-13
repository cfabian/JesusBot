import random
from random import randint
from datetime import datetime
import urllib
from urllib import request

def getCat():
    url = "http://thecatapi.com/api/images/get?format=src&type=jpg"
    req = urllib.request.urlretrieve(url, "images/cat.jpg")
    
def getCatGif():
    url = "http://thecatapi.com/api/images/get?format=src&type=gif"
    req = urllib.request.urlretrieve(url, "images/cat.gif")
        
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
            
redditIndex = 45000
def getRedditImage(subreddit, nsfw):
    global redditIndex
    # url = "https://www.reddit.com/r/dankmemes/"
    # url = "https://www.reddit.com/r/corgis/"
    url = 'https://www.reddit.com/r/' + subreddit + '/'
    if nsfw:
        req = urllib.request.Request(url, headers = {'User-agent': 'Jesus', 'cookie': 'over18=1'})
        
    else:
        req = urllib.request.Request(url, headers = {'User-agent': 'Jesus'})
        
    extension = ''
    try:
        with urllib.request.urlopen(req) as response:
            if response.url[ : 35] == 'https://www.reddit.com/over18?dest=':
                return 0
                
            page = response.read().decode('utf-8')
            badCount = 0
            
            while(extension != 'jpg' and extension != 'png'):
                if badCount > 20:
                    return -1
                
                begining_index = page.find("link", redditIndex)
                redditIndex = begining_index
                begining_index = page.find("data-url=", redditIndex) + 10
                redditIndex = begining_index
                
                ending_index = page.find("\"", redditIndex)
                
                rank = page.find("data-rank", redditIndex) + 11
                if page[rank : rank + 2] == "25":
                    redditIndex = 45000
                
                image = page[begining_index : ending_index]
                extension = image[-3 : ]
                badCount += 1
            
            urllib.request.urlretrieve(image, "images/" + subreddit + ".jpg")
            return 1
            
    except:
        return -1