import smtplib
from email.mime.text import MIMEText


def send(config, message):
    if config["ssl"]:
        smtp = smtplib.SMTP_SSL(config["url"], config["port"])
        smtp.starttls()
    else:
        smtp = smtplib.SMTP(config["url"], config["port"])
        if config["tls"]:
            smtp.starttls()

    msg = MIMEText(message)
    msg["Subject"] = "Access to The Long Night"
    msg["From"] = config["from"]
    msg["To"] = config["tos"]
    smtp.login(config["login"], config["password"])
    smtp.send_message(msg, from_addr=config["from"], to_addrs=config["tos"])
