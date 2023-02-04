import asyncio

import uvloop
from pyrogram.sync import idle
from pyrogram.client import Client
import DBManagement
from common import api_id, api_hash, bot_token, owner_id, replit_url
import webManager

webManager.awake(replit_url)


async def main():
    apps = [Client("shutupbot",
                   api_id=api_id,
                   api_hash=api_hash,
                   bot_token=bot_token,
                   plugins=dict(root="bots.shutUp.modules"))
            ]

    for app in apps:
        await app.start()
    await apps[0].send_message(owner_id, "Starting")
    print("Starting")

    await idle()

    await apps[0].send_message(owner_id, "Stopping")
    print("Stopping")
    # print(UB.usr.export_session_string())
    for app in apps:
        await app.stop()

uvloop.install()
asyncio.run(main())
