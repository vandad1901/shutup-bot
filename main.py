import asyncio

import uvloop
from pyrogram.sync import idle

import bots.shutUp as SU
import common
import moduleHelps


async def main():
    apps = [SU.app]

    for app in apps:
        await app.start()
    await SU.app.send_message(common.owner_id, "Starting")
    print("Starting")

    await idle()

    await SU.app.send_message(common.owner_id, "Stopping")
    print("Stopping")
    # print(UB.usr.export_session_string())
    for app in apps:
        await app.stop()

uvloop.install()
asyncio.run(main())
