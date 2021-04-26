# discord-link-opener
Automatically open browser tabs when links matching given constraints are sent in discord channels.

# Installation and Usage
1.    Download Python 3.6.x or 3.7.x . Before installing, make sure to check “Add Python to PATH”.
2.   Once installed, open CMD and type: 
                     pip install discord.py[voice] and 
                     pip install asyncio
3.    Download Link Opener: https://github.com/clearyy/discord-link-opener
4.    Copy open.py to your desktop.
5.    Right click open.py and select “Edit with IDLE”. Once in the code, only do the following two things: 
        1. Add the discord channel IDs (separated by commas) that you would like to monitor.
        2. Add your Discord token. (Tutorial on how to find your token: https://www.youtube.com/watch?v=tI1lzqzLQCs)
        3. Do not edit the keyword and blacklist lines.
        4. **OPTIONAL** Change path argument on line 37 for different os/browsers (assuming default install path):
        ```
        (DEFAULT) Windows/Chrome: "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        MacOS/Chrome: "open -a /Applications/Google\ Chrome.app %s"
        ```
6.    Save the file.
7.    Run open.py and you will be prompted for keywords and blacklisted words. Enter words in lowercase, separated by spaces and press enter when completed.
8.    Wait for the bot to automatically open Chrome browser tabs when links matching given constraints are sent in the specified discord channels. 
9.    Cook.
10.   To change keywords at any point, press Ctrl + c to terminate the script. Then simply run the script again and enter new words when prompted.

# Requirements
asyncio, discord.py

# Operating Systems
This was designed for and only tested on windows.

