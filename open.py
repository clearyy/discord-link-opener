import webbrowser
import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re

#pylint: disable=anomalous-backslash-in-string

client = Bot('adawd@@#^^')
client.remove_command('help')

#enter keywords to check for in links seperated by commas
keywords = ['']

#enter negative keywords that will prevent a browser window from opening seperated by commas. to have no blacklisted words, leave this empty
blacklist = []

#enter channel id(s) where links would be picked up (monitor channel id) seperated by commas. these should be ints
channels = []

#enter token of discord account that has access to watch specified channels
token = ''

global start_count
start_count = 0

#check for keywords and blacklisted words in message urls and open browser if conditions are met
async def check_urls(urls):
    for url in urls:
        if any(x in url for x in keywords) and all(x not in url for x in blacklist):
            #enter path to chrome here, for windows 10, this should work
            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
            print(f'Opened {url}')

@client.event
async def on_ready():
    global start_count
    # only print this info on the first time the client launches. this is due to d.py calling on_ready() after the bot regains connection
    if start_count == 0 and len(keywords) != 1 and keywords[0] != '':
        print('{} is ready to cop some restocks.\n'.format(str(client.user)))
        print('Watching for keywords {}.\n'.format(', '.join(keywords)))
        if len(blacklist) > 0:
            print('Ignoring keywords {}\n'.format(', '.join(blacklist)))
        else:
            print('No keywords currently blacklisted.\n')
        start_count += 1
    else:
        print('You have not provided any keywords to monitor. Restart with keywords added to the list.')

@client.event
async def on_message(message):
    if message.channel.id in channels:
        if message.embeds:
            for embed in message.embeds:
                toembed = embed.to_dict()
                #lazy fix
                try:
                    for field in toembed['fields']:
                        urls = re.findall("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+",str(field))
                        await check_urls(urls)
                except:
                    pass
        else:
            urls = re.findall("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+",message.content)
            await check_urls(urls)

client.run(token,bot=False)
