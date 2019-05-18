from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi


def send(config, message):
    if 'token' in config:
        token = config["token"]
    else:
        token = MatrixClient(config["server"]).login(config["username"],
                                                     config["password"])
    bot = MatrixHttpApi(config["server"], token=token)
    bot.send_message(config["room_id"], message)
