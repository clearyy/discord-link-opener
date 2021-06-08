'''
Script to monitor links sent to discord channels and opening them in a new browser tab.
Adapted to monitor links sent by https://partalert.net/join-discord

by https://github.com/Smidelis
based on https://github.com/clearyy/discord-link-opener and https://github.com/Vincentt1705/partalert-link-opener

'''

import webbrowser
import asyncio
from discord.ext.commands import Bot
import re
import winsound
from datetime import datetime
import urllib.parse as urlparse
from urllib.parse import parse_qs
import yaml

#pylint: disable=anomalous-backslash-in-string

client = Bot('KarlaKolumna')
client.remove_command('help')

#Pulling configuration from yaml file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

#Registering the browsers and preparing the choice
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(cfg['browsers']['chrome']['path']))
webbrowser.register('edgechromium', None, webbrowser.BackgroundBrowser(cfg['browsers']['edgechromium']['path']))
webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(cfg['browsers']['firefox']['path']))
browserchoice = cfg['browsers']['user_choice']

# Pulling keywords from yml config file
keywords = cfg['filters']['keywords']

# Pulling blacklist from yml file and accounting for it being null
black = cfg['filters']['blacklist']
if black == [None]:
    blacklist = ''
else:
    blacklist = black
print(blacklist)

# Pulling channels from yml file
channels = cfg['channels']

# Pulling token from the yml file
token = cfg['token']

global start_count
start_count = 0

# Decide whether you want to hear a bell sound when a link is opened (True/False)
playBellSound = cfg['various']['playBellSound']

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

    # Parse url to obtain query parameters
    parsed = urlparse.urlparse(url)

    country = parse_qs(parsed.query)['tld'][0]
    prod_id = parse_qs(parsed.query)['asin'][0]
    tag = parse_qs(parsed.query)['tag'][0]
    smid = parse_qs(parsed.query)['smid'][0]

    # Create full Amazon url
    url = f"https://www.amazon{country}/dp/{prod_id}?tag={tag}&linkCode=ogi&th=1&psc=1&smid={smid}"
    return url

# Check for keywords and blacklisted words in message urls and open browser if conditions are met
async def check_urls(urls, channel_name):
    for url in urls:
        if any(x in url.lower() for x in keywords) and all(x not in url.lower() for x in blacklist):
            # Check if url contains partalert.net. If true, direct amazon link will be built.
            if "partalert.net" in url:
                amazon_url = get_amazon_url(url)
                # Enter path to your browser
                webbrowser.get(browserchoice).open_new_tab(amazon_url)
                print_time(f'Link opened from #{channel_name}: {amazon_url}')
            else: 
                # Enter path to your browser
                webbrowser.get(browserchoice).open_new_tab(url)
                print_time(f'Link opened from #{channel_name}: {url}')
            if playBellSound:
                winsound.PlaySound('bell.wav', winsound.SND_FILENAME)

async def get_last_msg(channelid):
    msg = await client.get_channel(channelid).history(limit=1).flatten()
    return msg[0]

@client.event
async def on_ready():
    print_time('{} is ready to watch for links.'.format(str(client.user)))
    if len(keywords) >= 1 and keywords[0] != '':
        print_time('Watching for keywords {}.'.format(', '.join(keywords)))
    else:
        print_time('No keywords have been provided.')
    if len(blacklist) > 0:
        print_time('Ignoring keywords {}.'.format(', '.join(blacklist)))
    else:
        print_time('No keywords currently blacklisted.')

# Fixed discordpy not able to read embeds anymore. Thanks to dubble#0001 on Discord.
@client.event
async def on_message(message):
    if message.channel.id in channels:
        await asyncio.sleep(0.3)
        try:
            last_msg = await get_last_msg(message.channel.id)
            fields = last_msg.embeds[0].fields
            linkembed = next(x for x in fields if x.name == "Link")
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', linkembed.value if linkembed else "")
            for url in urls:
                await check_urls(urls, message.channel.name)
        except:
            if message.content != '':
                urls = re.findall("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.#&+]+\.[\w/\-?=%.#&+]+",message.content)
                
                if urls:
                    asyncio.ensure_future(check_urls(urls, message.channel.name))
client.run(token,bot=False)
