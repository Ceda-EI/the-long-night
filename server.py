#!/usr/bin/env python3
"Server for the-long-night"

import subprocess
import json
import os
import bcrypt
from flask import Flask, request

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def en_login():
    "/login"
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

    if "matrix" in config and config["matrix"]["enabled"]:
        from backends import matrix
        try:
            matrix.send(config["matrix"], message)
        except:
            pass

    if "telegram" in config and config["telegram"]["enabled"]:
        from backends import telegram
        try:
            telegram.send(config["telegram"], message)
        except:
            pass

    if "email" in config and config["email"]["enabled"]:
        from backends import mail
        try:
            mail.send(config["email"], message)
        except:
            pass

    return ("Logged In. The ssh key will be added " + str(config["days"]) +
            " day(s) later.")


@app.route('/')
def en_root():
    "/"
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>The Long Night</title>
    </head>
    <body>
        <h1>The Long Night</h1>
        <form action="login" method="POST" style="width: 100%;">
            <input type="password" name="password" placeholder="Password"/>
            <br>
            <button type="submit">Submit</button>
        </form>
        <a href="http://gitlab.com/ceda_ei/the-long-night">Source</a>
    </body>
</html>
"""
