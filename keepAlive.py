import random
import time
from threading import Thread
from typing import Optional

import requests


def ping(target: str, debug: bool):
    print(f"Starting keep-alive service for {target}")
    while True:
        time.sleep(random.randint(10 * 60, 15 * 60))
        r = requests.get(target)
        if debug == True:
            print(f"Status Code: {r.status_code}")


def awake(target: Optional[str] = None, debug: bool = False):
    if (target is not None):
        Thread(target=ping, args=(target, debug)).start()
