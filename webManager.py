import random
import time
from threading import Thread

import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "You have found the home of a Python program!"


def run():
    app.run(host="0.0.0.0", port=8080)


def ping(target, debug):
    while True:
        time.sleep(random.randint(15*60, 30*60))
        r = requests.get(target)
        if debug == True:
            print("Status Code: " + str(r.status_code))


def awake(target=None, debug=False):
    app.logger.disabled = True
    t = Thread(target=run)
    t.start()
    if (target is not None):
        r = Thread(target=ping, args=(target, debug))
        r.start()
