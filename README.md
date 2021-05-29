# discord-link-opener
Automatically open browser tabs when links matching given constraints are sent in discord channels.
Adapted to link sent by https://partalert.net/join-discord. If a link contains `partalert.net`, the script directly builds the Amazon link and opens it directly (of course including the PartAlert affiliate information).

# Disclaimer
Use at own risk!

Automating normal user accounts (generally called "self-bots") is against the [Discord Guidelines](https://discord.com/guidelines) and may result in an account termination (ban) without prior notice.

# Installation and Usage
1. Download Python 3.6.x or 3.7.x or 3.8.x . Before installing, make sure to check “Add Python to PATH”.
2. Once installed, open CMD and type:
```
pip install discord.py[voice] 
pip install asyncio
pip install pyyaml
```
3. Download Link Opener: https://github.com/Smidelis/discord-link-opener/
4. Extract the contents of the *.zip file to your Desktop/Documents
5. Copy config_example.yaml and rename it to config.yml
6. Replace the placeholders with the values for the token*, the keywords you're looking for, the blacklisted words and the channels
* Add your Discord token. (Tutorial on how to find your token: https://www.youtube.com/watch?v=tI1lzqzLQCs)

**Do not edit the keyword and blacklist lines!**

6. 3 browsers have been implemented: chrome, edgechromium, firefox and you can choose the one you want to use by editing the user_choice parameter
7. Save the file.
8. Run open.py
9. Wait for the bot to automatically open new browser tabs when links matching given constraints are sent in the specified discord channels. 
10. Cook.
11. To change keywords at any point, press Ctrl + c to terminate the script. Then simply run the script again and enter new words when prompted.

# Requirements
asyncio, discord.py, pyyaml

# Operating Systems
This was designed for and only tested on windows.

# Credits
This script is a combination of the versions by clearyy and Vincentt1705 and some own ideas. Thanks for the inspiration!
Config files added by elevul
