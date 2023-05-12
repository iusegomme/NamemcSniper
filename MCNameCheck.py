import configparser
import os
import requests
import time
import datetime
import logging



#Creating log file and config if necessary
logging.basicConfig(filename = "namechange.log", encoding = "utf-8", level = logging.INFO)

config = configparser.ConfigParser()
def write_file():
    config.write(open("config.ini", "w"))

if not os.path.exists("config.ini"):
    config.add_section("Accounts")
    config.set("Accounts", "accounts", "UUIDs Go Here")
    config.add_section("Settings")
    config.set("Settings", "cooldown", "0.75")
    config.set("Settings", "failcooldown", "5")

    with open("config.ini", "w") as configfile:
        config.write(configfile)

#Reading settings
config.read("config.ini")
cooldown = float(config["Settings"]["cooldown"])
failcooldown = float(config["Settings"]["failcooldown"])

#If user has not filled any UUIDs into config.ini this error will appear
while True:
    if config["Accounts"]["accounts"] == "UUIDs Go Here":
        input("Please fill your selected UUIDs separated by a space into the created config.ini file before pressing any key to continue.")
        config.read("config.ini")

    elif config["Accounts"]["accounts"] != "UUIDs Go Here":
        break

uuidlist = config["Accounts"]["accounts"].split()

#Adding all current names of provided UUIDs to a list
namelist = []
var = 0
while var == 0:
    for i in uuidlist:
        try:
            request = requests.get(f"https://api.mojang.com/user/profile/{i}").json()
            name = request["name"]
            namelist.append(name)
            print("Added", name, "to namelist.")
            var = var + 1
        except:
            print("Unable to read username from API... Waiting", failcooldown, "second/s before continuing.")
            time.sleep(failcooldown)

#Reading out settings to confirm with user
print("\nSettings:")
print("Provided UUIDs -", uuidlist)
print("Provided usernames -", namelist)

input("\nPress any key to continue...")

#Use this to check for uptime
starttime = time.time()

#Checking all provided UUIDs for changes to their name in the API
while True:
    for i in uuidlist:
        #Finding name relative to the position of this UUID in the namelist to print it
        index = uuidlist.index(i)
        username = namelist[index]
        #Grabbing current time and calculating uptime to two decimal points to print in check message
        timestamp = datetime.datetime.now().isoformat()
        uptime = "%.2f" % round(time.time() - starttime, 2)
        print(index, "| Uptime:", uptime, "| Time:", timestamp, "| Checking account:", username, i)
        #Try to grab the current username of the UUID being checked and store it to a variable
        try:
            request = requests.get(f"https://api.mojang.com/user/profile/{i}").json()
            namecheck = request["name"]
        #If that is not possible tell the user and wait for the specified time in config
        except:
            print("Unable to read username from API... Waiting", failcooldown, "second/s before continuing.")
            time.sleep(failcooldown)

        #If a change is detected to the username run this
        if namecheck not in namelist:
            print("Account", username, i, "changed at", timestamp, "to", namecheck)
            logging.info("Account %s %s changed at %s to %s.", username, i, timestamp, namecheck)
            #Removing the current name from namelist and uuidlist
            del namelist[index]
            del uuidlist[index]
            time.sleep(cooldown)
        #If namecheck is the same as the username have a little nap
        else:
            time.sleep(cooldown)
