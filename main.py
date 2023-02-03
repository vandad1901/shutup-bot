import asyncio
import time
import uvloop
from pyrogram.sync import idle
from pyrogram import filters

import DBManagement as DB
import common
import bots.shutUp.shutup as SU
import moduleHelps


apps = [SU.app]

for app in apps:
    app.start()
SU.app.send_message(common.owner_id, "Starting")
print("Starting")

idle()

SU.app.send_message(common.owner_id, "Stopping")
print("Stopping")
# print(UB.usr.export_session_string())
for app in apps:
    app.stop()
