#!/usr/bin/env python3

import subprocess
import json
import os
import bcrypt
from flask import Flask, request

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def en_login():
    try:
        password = request.values['password']
    except KeyError:
        return "Missing password", 400
    with open('config.json') as f:
        config = json.load(f)

    if not bcrypt.checkpw(password.encode(), config["password"].encode()):
        return "Unauthorized", 401

    if os.path.isfile(os.path.expanduser('~/.the-long-night-pid')):
        return "Already logged in"

    with open(os.path.expanduser('~/.the-long-night-pid'), 'w') as f:
        x = subprocess.Popen(["python3", "background.py"],
                             start_new_session=True)
        f.write(str(x.pid))

    message = ("The correct password has been entered in The-Long-Night. "
               "The ssh key will be added " + str(config["days"]) + " days "
               "later. To prevent that from happenning, login to your server "
               "and run `cancel-adding-key.sh` in The Long Night installation"
               "directory.")

    if config["matrix"]["enabled"]:
        from backends import matrix
        try:
            matrix.send(config["matrix"], message)
        except:
            pass

    if config["telegram"]["enabled"]:
        from backends import telegram
        try:
            telegram.send(config["telegram"], message)
        except:
            pass

    return ("Logged In. The ssh key will be added " + str(config["days"]) +
            " day(s) later.")
