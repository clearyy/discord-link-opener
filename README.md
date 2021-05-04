# discord-link-opener
Automatically open browser tabs when links matching given constraints are sent in discord channels.
Adapted to link sent by https://partalert.net/join-discord. If a link contains `partalert.net`, the script directly builds the Amazon link and opens it directly (of course including the PartAlert affiliate information).

# Disclaimer
Use at own risk!

Automating normal user accounts (generally called "self-bots") is against the [Discord Guidelines](https://discord.com/guidelines) and may result in an account termination (ban) without prior notice.

# Installation and Usage
1. Download Python 3.6.x or 3.7.x . Before installing, make sure to check “Add Python to PATH”.
2. Once installed, open CMD and type:
```
pip install discord.py[voice] 
pip install asyncio
```
3. Download Link Opener: https://github.com/Smidelis/discord-link-opener/
4. Extract the contents of the *.zip file to your Desktop/Documents
5. Right click open.py and select “Edit with IDLE”. Once in the code, only do the following two things:
* Add the discord channel IDs (separated by commas) that you would like to monitor.
* Add your Discord token. (Tutorial on how to find your token: https://www.youtube.com/watch?v=tI1lzqzLQCs)

**Do not edit the keyword and blacklist lines!**

6. The script has been tested with Edge Chromium, but Google Chrome most probably works as well. In case you want to change to Google Chrome replace the browser path with either the 32bit or the 64bit path:
* Chrome 32bit: `C:/Program Files (x86)/Google/Chrome/Application/chrome.exe`
* Chrome 64bit: `C:/Program Files/Google/Chrome/Application/chrome.exe`
7. Save the file.
8. Run open.py and you will be prompted for keywords and blacklisted words. Keywords are the words searched for in the sent links. If a link is containing a blacklisted word, it will be ignored. Enter words in lowercase, separated by spaces and press enter when completed.
9. Wait for the bot to automatically open new browser tabs when links matching given constraints are sent in the specified discord channels. 
10. Cook.
11. To change keywords at any point, press Ctrl + c to terminate the script. Then simply run the script again and enter new words when prompted.

# Requirements
asyncio, discord.py

# Operating Systems
This was designed for and only tested on windows.

# Credits
This script is a combination of the versions by clearyy and Vincentt1705 and some own ideas. Thanks for the inspiration!
