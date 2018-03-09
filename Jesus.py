import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from datetime import datetime
import urllib
from urllib import request

# from lists import *
from fileHandler import *
from imageHandler import *

postCount = 0
postCountEnd = randint(1, 9)

bot = commands.Bot(command_prefix = "", description = "")

# Initialize the bot for the server!
# confFileName = 'test-bot.conf'
confFileName = 'Jesus.conf'
conf = readConf(confFileName)
print('Bot Id: %s' % (conf['botId']))
loserName = conf['loserName']

lists = readLists()
greetings = tuple(lists['greetings'])
insults = tuple(lists['insults'])
DANK = tuple(lists['DANK'])
cat = tuple(lists['cat'])
dog = tuple(lists['dog'])
        
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
    if bot.user.name == 'test-bot':
        await bot.change_presence(game = discord.Game(name = "TEST"))
        await bot.send_message(discord.Object(id = "299195204957896716"), "Beep Boop, I am a bot!\nhttps://github.com/cfabian/JesusBot\nFor a list of commands say '@test-bot help me'")
        
    else:
        await bot.change_presence (game = discord.Game (name = "with mankind"))
        getCat()
        await bot.send_file(discord.Object(id = "298873991723089920"), "images/cat.jpg")
    
@bot.event
async def on_message(message):
    
    bot_mention = "<@" + bot.user.id + ">"
    
    global postCount, postCountEnd, insults
    #print(message.channel)
    #print(message.author)
    #print(message.server)
    #print(str(message.attachments))
    
    if str(message.author.id) != bot.user.id:
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
            getRedditImage('dankmemes')
            await bot.send_file(message.channel, "images/dankmemes.jpg")
            
        elif message.content.startswith("get image from subreddit "):
            subreddit = message.content.split()[4]
            if subreddit[ : 3] == '/r/':
                subreddit = subreddit[3 : ]
                
            elif subreddit[ : 2] == 'r/':
                subreddit = subreddit[2 : ]
                
            getRedditImage(subreddit)
            await bot.send_file(message.channel, "images/" + subreddit + ".jpg")
            
        elif message.content.startswith("timecube"):
            line = random.choice(open("timecube.txt").readlines())
            await bot.send_message(message.channel, line)
            await bot.send_message(message.channel, "http://timecube.2enp.com/")

        elif message.content.startswith("bible"):
            line = request.urlopen("http://labs.bible.org/api/?passage=random").read().decode()
            headers = line.split("</b>");
            headers[0] = headers[0].replace("<b>", "***") + "***"
            await bot.send_message(message.channel, headers[0])
            await bot.send_message(message.channel, headers[1])
            
        elif message.content.startswith(bot_mention):
            m = message.content.split()
            if len(m) == 1:
                await bot.send_message(message.channel, "Hey gurl : )")
                
            elif m[1] == "help" and len(m) == 3 and m[2] == "me":
                if randint(1, 9) == 7:
                    await bot.send_message(message.channel, "FUCK OFF!")
                    
                else:
                    await bot.send_message(message.channel, "For a cat picture say 'cat'\n"
                                                            "For a dog picture say 'dog'\n"
                                                            "For a diggity dank may may say 'dank meme'\n"
                                                            "For a verse from our lord and savior say 'bible'\n"
                                                            "To bully someone say '@Jesus bully @username'\n"
                                                            "For religious guidance say 'timecube'\n"
                                                            "To force me to look through your favorite subreddit say 'get image from subreddit [subreddit]'\n"
                                                            "To get a list of admin commands say '@Jesus --help'\nhttps://github.com/cfabian/JesusBot")
                
            elif m[1] == '--help':
                await bot.send_message(message.channel, "To get a log dump say '@Jesus logdump number_of_messages'\nTo add to the list of insults say '@Jesus add insult your_insult\nhttps://github.com/cfabian/JesusBot")
                
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
                        if num > 20:
                            await bot.send_message(message.channel, "Fuck you!\nI'm not gonna post more than 20 logged messages.")
                            
                        else:
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
                    
            elif m[1] == 'add' and m[2] == 'insult':
                lists['insults'].append(', %s' % (' '.join(m[3 : ])))
                writeLists(lists)
                insults = tuple(lists['insults'])
                await bot.send_message(message.channel, "Added \"%s\" to list of insults." % (' '.join(m[3 : ])))
                        
            else:
                await bot.send_message(message.channel, "I'm sorry " + message.author.mention + " but I am currently not smart enough to fulfill your request of:\n~" + str(message.content[len(bot_mention) + 1 : ]) + "\nHowever, I can provide you with a picture of a cat.")
                getCat()
                await bot.send_file(message.channel, "images/cat.jpg")
                

bot.run(conf['botId'])
