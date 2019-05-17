import requests


def send(tg_config, message):
    url = "https://api.telegram.org/bot{}/sendMessage".format(
        tg_config["bot_token"])
    data = {
        "chat_id": tg_config["user_id"],
        "text": message
    }
    requests.post(url, data=data)
