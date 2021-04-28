'''
Script to monitor links sent to discord channels and opening them in a new browser tab.
Adapted to monitor links sent by https://partalert.net/join-discord

by https://github.com/Smidelis
based on https://github.com/clearyy/discord-link-opener and https://github.com/Vincentt1705/partalert-link-opener

'''

import webbrowser
import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re
import winsound
from datetime import datetime

#pylint: disable=anomalous-backslash-in-string

client = Bot('adawd@@#^^')
client.remove_command('help')

# Prompt users for keywords to search for in the links.
keywords = list(map(str,input("Enter keywords to search for, seperated by space: ").split()))

# Prompt user to enter negative keywords that will prevent a browser window from opening. To have no blacklisted words, press enter right away
blacklist = list(map(str,input("Enter blacklisted keywords, seperated by space: ").split()))

# Enter channel id(s) where links would be picked up (monitor channel id) seperated by commas. these should be ints
channels = []

# Enter token of discord account that has access to watch specified channels
token = ''

global start_count
start_count = 0

# Decide whether you want to hear a bell sound when a link is opened (True/False)
playBellSound = True

# Based on https://github.com/Vincentt1705/partalert-link-opener
# Function to print the current time before the information about the link.
def print_time(*content):
    """
    Can be used as a normal print function but includes the current date and time
    enclosed in brackets in front of the printed content.
    :param content: The content you would normally put in a print() function
    """
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{date_time}] - [INFO] ", *content)

# Function to build the amazon url, where partalert is redirecting to
def get_amazon_url(url):
    """
    This function collects and returns an amazon link
    that would be linked through the green button on the webpage.
    :param url: An partalert.net link for an amazon product
    :return: The extracted amazon link to the product
    """
    # Split url and filter needed parts
    asin, price, smid, tag, timestamp, title, tld = url.split("&")

    # For the product id and country search for the last '=' and collect the part after it
    prod_id, country = (info[info.rfind("=")+1:] for info in (asin, tld))

    # Create full Amazon url
    url = f"https://www.amazon{country}/dp/{prod_id}?{tag}&linkCode=ogi&th=1&psc=1&{smid}"
    return url

# Check for keywords and blacklisted words in message urls and open browser if conditions are met
async def check_urls(urls, channel_name):
    for url in urls:
        if any(x in url.lower() for x in keywords) and all(x not in url.lower() for x in blacklist):
            # Check if url contains partalert.net. If true, direct amazon link will be built.
            if "partalert.net" in url:
                amazon_url = get_amazon_url(url)
                # Enter path to your browser
                webbrowser.get("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s").open(amazon_url)
                print_time(f'Link opened from #{channel_name}: {amazon_url}')
            else: 
                # Enter path to your browser
                webbrowser.get("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s").open(url)
                print_time(f'Link opened from #{channel_name}: {url}')
            if playBellSound:
                winsound.PlaySound('bell.wav', winsound.SND_FILENAME)

@client.event
async def on_message(message):
    global start_count
    # temporary bypass to weird d.py cacheing issue
    # only print this info on the first time the client launches. this is due to d.py calling on_ready() after the bot regains connection
    if start_count == 0:
        print('\n{} is ready to cop some restocks.\n'.format(str(client.user)))
        if len(keywords) >= 1 and keywords[0] != '':
            print('Watching for keywords {}.\n'.format(', '.join(keywords)))
        else:
            print('No keywords have been provided.\n')
        if len(blacklist) > 0:
            print('Ignoring keywords {}.\n'.format(', '.join(blacklist)))
        else:
            print('No keywords currently blacklisted.\n')
        start_count += 1
    else:
        if message.channel.id in channels:
            if message.embeds:
                for embed in message.embeds:
                    toembed = embed.to_dict()
                    if str(toembed['type']).lower() != 'link':
                        urls = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",toembed['title'])
                        if urls:
                            await check_urls(urls, message.channel.name)
                        try:
                            urls2 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",toembed['description'])
                            if urls2:
                                await check_urls(urls2, message.channel.name)
                        except:
                            pass
                        try:
                            for field in toembed['fields']:
                                urls3 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",str(field))
                                if urls3:
                                    await check_urls(urls3, message.channel.name)
                        except:
                            pass
            if message.content != '':
                print(message.content)
                urls4 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",message.content)
                if urls4:
                    await check_urls(urls4, message.channel.name)

client.run(token,bot=False)