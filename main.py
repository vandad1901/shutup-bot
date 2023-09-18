import asyncio
import sys

import DBManagement
from common import api_hash, api_id, bot_token, owner_id
from pyrogram.client import Client
from pyrogram.sync import idle

if sys.platform in ('win32', 'cygwin', 'cli'):
    from winloop import install
else:
    from uvloop import install


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

install()
asyncio.run(main())
