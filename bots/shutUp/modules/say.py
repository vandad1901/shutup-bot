"""
Deletes the command and says the command argument

Usage:
**/say**
"""
from pyrogram import filters

from ..shutup import app, isModuleToggledFilter


@app.on_message(filters.command(["say", "say@damnshutup_bot"]) & isModuleToggledFilter("say"))
async def say(client, message):
    try:
        await message.delete()
    except:
        await message.reply_text("Failed to delete(check permissions)")
    if(message.reply_to_message):
        await message.reply_to_message.reply_text(" ".join(
            message.command[1:]))
    else:
        await message.reply_text(" ".join(message.command[1:]), quote=False)
