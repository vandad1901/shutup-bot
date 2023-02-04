from flask import Flask
from threading import Thread
import random
import time
import requests
import logging

app = Flask(__name__)

@app.route("/")
def home():
    return "You have found the home of a Python program!"


def run():
    app.run(host="0.0.0.0", port=8080)


def ping(target, debug):
    while True:
        r = requests.get(target)
        if debug == True:
            print("Status Code: " + str(r.status_code))
        time.sleep(random.randint(15*60, 30*60))


def awake(target, debug=False):
    log = logging.getLogger("keep alive")
    log.disabled = True
    app.logger.disabled = True
    t = Thread(target=run)
    r = Thread(
        target=ping,
        args=(
            target,
            debug,
        ),
    )
    t.start()
    r.start()