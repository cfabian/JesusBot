import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from datetime import datetime
import urllib
from urllib import request

from lists import *

postCount = 0
postCountEnd = randint(1, 9)

dankIndex = 45000

bot = commands.Bot(command_prefix = "", description = "")

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
            
def getdankmeme():
    global dankIndex
    url = "https://www.reddit.com/r/dankmemes/"
    req = urllib.request.Request(url, headers = {'User-agent': 'Jesus'})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
        
        begining_index = page.find("link", dankIndex)
        dankIndex = begining_index
        begining_index = page.find("data-url=", dankIndex) + 10
        dankIndex = begining_index
        
        ending_index = page.find("data-domain", dankIndex) - 2
        
        rank = page.find("data-rank", dankIndex) + 11
        if page[rank : rank + 2] == "25":
            dankIndex = 45000
        
        image = page[begining_index : ending_index]
        extension = image[-3 : ]
        
        urllib.request.urlretrieve(image, "images/dankmeme.jpg")
        
def getLine(servername, linenum):
    with open(servername + ".log", "r") as log:
        l = log.readlines()
        line = len(l) - linenum - 1
        return str(l[line])

@bot.event
async def on_ready():
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------")
    #await bot.change_presence (game = discord.Game (name = "with mankind"))
    #await bot.send_message (discord.Object (id = "298873991723089920"), "Beep Boop, I am a bot!")
    #await bot.send_message (discord.Object (id = "298873991723089920"), "For a list of commands say '@Jesus help me'")
    await bot.change_presence(game = discord.Game(name = "TEST"))
    await bot.send_message(discord.Object(id = "299195204957896716"), "Beep Boop, I am a bot!\nFor a list of commands say '@Jesus help me'")
    
@bot.event
async def on_message(message):
    
    bot_mention = "<@" + bot.user.id + ">"
    
    global postCount, postCountEnd
    #print(message.channel)
    #print(message.author)
    #print(message.server)
    #print(str(message.attachments))
    
    if str(message.author) != bot.user:
        with open(str (message.server) + ".log", "a") as log:
            log.write((str(message.timestamp) + ",").ljust(30) + (str(message.author) + ",").ljust(20) + (str(message.channel) + ",").ljust(20))
            if message.attachments:
                log.write("[IMAGE],\n")
                
            else:
                log.write(str(message.content) + ",\n")
            
        if str(message.author) == loserName:
            postCount += 1
            if postCount == postCountEnd:
                postCount = 0
                postCountEnd = randint(1, 9)
                await bot.send_message(message.channel, message.author.mention + " " + random.choice(insults))
            
        
        if message.content.startswith(greetings):
            await bot.send_message(message.channel, "Sup you goddamn degenerate")
            
        elif message.content.startswith(cat):
            getCat()
            await bot.send_file(message.channel, "images/cat.jpg")
            
        elif message.content.startswith(dog):
            getDog()
            await bot.send_file(message.channel, "images/dog.jpg")
            
        elif message.content.startswith(DANK):
            getdankmeme()
            await bot.send_file(message.channel, "images/dankmeme.jpg")
            
        elif message.content.startswith("timecube"):
            line = random.choice(open("timecube.txt").readlines())
            await bot.send_message(message.channel, line)
            await bot.send_message(message.channel, "http://timecube.2enp.com/")
            
        elif message.content.startswith(bot_mention):
            m = message.content.split()
            if len(m) == 1:
                await bot.send_message(message.channel, "Hey gurl : )")
                
            elif m[1] == "help" and m[2] == "me":
                if randint(1, 9) == 7:
                    await bot.send_message(message.channel, "FUCK OFF!")
                    
                else:
                    await bot.send_message(message.channel, "For a cat picture say 'cat'\nFor a dog picture say 'dog'\nFor a diggity dank may may say 'dank meme'\nTo bully someone say '@Jesus bully @username'\nFor religious guidance say 'timecube'\nTo get a log dump say '@Jesus logdump number_of_messages'")
                
            elif m[1] == "bully":
                if randint(1, 9) == 2:
                    await bot.delete_message(message)
                    await bot.send_message(message.channel, message.author.mention + " " + random.choice(insults))
                    await bot.send_message(message.channel, "HEY " + message.author.mention + " HOW DO YOU LIKE BEING BULLIED!!!!!")
                    
                else:
                    await bot.delete_message(message)
                    await bot.send_message(message.channel, m[2] + " " + random.choice(insults))
                    
            elif m[1] == "logdump":
                if len(m) > 2:
                    if m[2].isdigit():
                        num = int(m[2])
                        await bot.send_message(message.channel, "Last " + str(num) + " messages:")
                        logs = ""
                        for i in range(num - 1, -1, -1):
                            logs += getLine(str(message.server), i)
                            
                        await bot.send_message(message.channel, logs)
                        
                    else:
                        await bot.send_message(message.channel, "You're retarded! Type in a fucking number next time.")
                    
                else:
                    await bot.send_message(message.channel, "I see you couldn't make up your mind about how many messages you wanted me to show.\nThat's okay, we can't all be intelligent like me.\nLast 5 messages:")
                    logs = ""
                    for i in range(4, -1, -1):
                        logs += getLine(str(message.server), i)
                        
                    await bot.send_message(message.channel, logs)
                        
            else:
                await bot.send_message(message.channel, "I'm sorry " + message.author.mention + " but I am currently not smart enough to fulfill your request of:\n~" + str(message.content[len(bot_mention) + 1 : ]) + "\nHowever, I can provide you with a picture of a cat.")
                getCat()
                await bot.send_file(message.channel, "images/cat.jpg")
    
      
      
# Initialize the bot for the server!
# confFileName = 'Jesus.conf'
confFileName = 'Jesus.conf'
print('Reading %s...' % (confFileName))
with open(confFileName) as f:
    conf = f.read()
    
line = conf[conf.find('botId') : ]
botId = line[line.find(': ') + 3 : line.find('\n') - 2]
print('Bot Id: %s' % (botId))
line  = conf[conf.find('loserName') : ]
loserName = line[line.find(': ') + 3 : line.find('\n') - 2]
print('Loser Name: %s' % (loserName))
bot.run(botId)