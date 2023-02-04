import asyncio
import time

import uvloop
from pyrogram import filters
from pyrogram.sync import idle

import bots.shutUp.shutup as SU
import common
import DBManagement as DB
import moduleHelps
import webManager

webManager.awake(common.replit_url)
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
