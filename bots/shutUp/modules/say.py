"""
Deletes the command and says the command argument

Usage:
**/say**
"""
from pyrogram import Client, filters

from common import bot_username, isModuleToggledFilter


@Client.on_message(filters.command(["say", f"say@{bot_username}"]) & isModuleToggledFilter("say"))
async def say(client, message):
    try:
        await message.delete()
    except:
        await message.reply_text("Failed to delete(check permissions)")
    if (message.reply_to_message):
        await message.reply_to_message.reply_text(" ".join(
            message.command[1:]))
    else:
        await message.reply_text(" ".join(message.command[1:]), quote=False)
