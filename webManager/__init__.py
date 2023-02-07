import logging
import random
import time
from threading import Thread
from typing import Optional

import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "You have found the home of a Python program!"


@app.route("/bingus")
def bingus():
    return render_template("bingus.html")


def run():
    app.run(host="0.0.0.0", port=8080)


def ping(target: str, debug: bool):
    print(f"Starting keep-alive service for {target}")
    while True:
        time.sleep(random.randint(10*60, 15*60))
        r = requests.get(target)
        if debug == True:
            print(f"Status Code: {r.status_code}")


def awake(target: Optional[str] = None, debug: bool = False):
    app.logger.disabled = True
    logging.getLogger("werkzeug").disabled = True
    t = Thread(target=run)
    t.start()
    if (target is not None):
        r = Thread(target=ping, args=(target, debug))
        r.start()


if (__name__ == "__main__"):
    run()
