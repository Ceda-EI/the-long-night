# The Long Night

Increase Bus Factor by providing ssh access to server.

# How it works

+ The server admin runs the installation and sets a password, ssh-key, number
  of days to add the key after.
+ The server admin gives the "bus factor" the password.
+ In case of an incident, the "bus factor" visits the webpage and enters the
  provided password.
+ If the correct password is entered, the server admin is notified via all the
  configured backends that the correct password has been added.
+ If the server admin doesn't wish the ssh-key to be added, they can login and
  run `cancel-adding-key.sh` in the installation directory.
	+ If the command is run within the configured number of days, then the key
	  is not added and everything returns back to normal and the server starts
	  listening for password again. No new setup is necessary.
	+ If the command is not run within the configured number of days, then the
	  ssh key is added.


# Installation

+ Clone the repository.
	+ `git clone https://gitlab.com/ceda_ei/the-long-night.git`
+ Install the dependencies
	+ `pip3 install -r requirements.txt`
+ Create a config file by running `./installation.py`.
+ Install `gunicorn`.
	+ `pip3 install gunicorn`
+ Run `gunicorn3 -b 127.0.0.1:5000 server:app`. Change port if you want to run
  gunicorn on a different port.
+ Set up a reverse proxy from your webserver to `localhost:5000`.
