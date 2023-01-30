"""
Deletes the message it was replied to

Usage:
**/del**
"""
from pyrogram import filters

from common import bot_username, isModuleToggledFilter, owner_id

from ..shutup import app


@app.on_message(filters.command(["del", f"del@{bot_username}"]) & filters.group & isModuleToggledFilter("delete"))
def deleteCommand(client, message):
    if (message.chat.get_member("self").can_delete_messages):
        if (message.from_user.id == owner_id or message.chat.get_member(message.from_user.id).can_delete_messages):
            message.delete()
            message.reply_to_message.delete()
        else:
            message.reply_text("Imagine")
    else:
        message.reply_text("I don't have permission to delete messages here")
