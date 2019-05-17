#!/usr/bin/env python3

import bcrypt
import json


def get_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Not a number!\n")


def get_boolean(prompt, default):
    string = input(prompt).lower()
    if string in ["y", "yes", "true", "t", "1"]:
        return True
    elif string in ["n", "no", "false", "f", "0"]:
        return False
    return default


config = {}

# Master password
print("""
Enter master password. Master password is the password you provide to your bus
factor. When the master password is entered, The Long Night will send messages
to you via all the configured mediums. If you do not respond within 2 days
(configurable), The Long Night will add the supplied key as an authorized key
for the user it is running as.
""")
password = input("> ").encode()
config["password"] = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

print("\nEnter number of days to wait before adding the ssh key\n")
config["days"] = get_number("> ")


# SSH key
print("\nEnter ssh key to add\n")
config["ssh_key"] = input("> ")

print("\nConfiguring mediums for contact when the master password is entered.")

# Telegram
print("\nDo you want to enable Telegram messages?\n")
config["telegram"] = {}
tg_enable = get_boolean("Y/n ", True)
config["telegram"]["enabled"] = tg_enable

if tg_enable:
    print("\nEnter bot token\n")
    config["telegram"]["bot_token"] = input("> ")
    print("\nEnter userid\n")
    config["telegram"]["user_id"] = get_number("> ")
    print("\nAttempting to send a test message")
    from backends import telegram
    telegram.send(config["telegram"], "Test Message from The Long Night")
    print("""
Message sent, if you did not recieve a message, check the bot_token and
user_id. Also, ensure that you have started the bot.
""")

print("\nStoring config.")
with open('config.json', 'w') as f:
    json.dump(config, f)
print("Stored config.")
