# Overview

This script constantly checks a set of provided Minecraft UUIDs for changes to their associated username. This is useful for small scale name sniping if you want to know (close to) the exact time the name was changed as Mojang no longer provides an API route for this information.

# Usage
Simply [install Python](https://www.python.org/downloads/), go to the directory with MCNameCheck.py in it in your terminal and run `python3 MCNameCheck.py`, it will create a config file in the same directory where you can enter as many UUIDs as you want separated by spaces. The more UUIDs you add the longer it takes to cycle through all names so you should try to keep the amount low.

# Features
- Logs any detected change to usernames you are checking to a file named namechange.log in the same directory
- Automatically stops checking a username when it is changed
- Uptime counter in all check messages to know how long the script has been running
- Settings confirmation screen to ensure you are checking the correct names
- Configurable cooldowns between each name check
- Configurable cooldowns at API errors
- Easy to use config file in .ini format
- Intuitive and useful messages at runtime
- Well documented code comments
- ISO 8601 time format

