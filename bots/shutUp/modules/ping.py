"""
Measures the bot server ping by looking at the difference between message send and receive time

Usage:
**/ping**
"""

import time

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Chat, Message

from common import bot_username, isModuleToggledFilter


@Client.on_message(filters.command(["ping", f"ping@{bot_username}"]) & isModuleToggledFilter("ping"))
async def ping(client: Client, message: Message):
    start_time = time.time()
    myMsg = await message.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    await myMsg.edit_text(f"***Pong!!!***\n`{ping_time}ms`")
