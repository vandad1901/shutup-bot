"""
Measures the bot server ping by looking at the difference between message send and receive time

Usage:
**/ping**
"""

import time

from pyrogram import filters
from shutup import app

from common import bot_username, isModuleToggledFilter


@app.on_message(filters.command(["ping", f"ping@{bot_username}"]) & isModuleToggledFilter("ping"))
async def ping(client, message):
    start_time = time.time()
    mymsg = await message.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    await mymsg.edit_text(f"***Pong!!!***\n`{ping_time}ms`")
