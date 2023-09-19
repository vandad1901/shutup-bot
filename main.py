from __future__ import annotations

import asyncio
import sys

from pyrogram.client import Client
from pyrogram.sync import idle

import DBManagement
from common import api_hash
from common import api_id
from common import bot_token
from common import owner_id

if sys.platform in ("win32", "cygwin", "cli"):
    from winloop import install
else:
    from uvloop import install


async def main():
    apps = [
        Client(
            "shutupbot",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins=dict(root="bots.shutUp.modules"),
        ),
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


install()
asyncio.run(main())
