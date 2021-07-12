"""
Deletes the message it was replied to

Usage:
**/del**
"""
from pyrogram import filters

from ..shutup import app, isModuleToggledFilter, owner_id


@app.on_message(filters.command(["del", "del@damnshutup_bot"]) & filters.group & isModuleToggledFilter("delete"))
def deleteCommand(client, message):
    if(message.chat.get_member("self").can_delete_messages):
        if(message.from_user.id == owner_id or message.chat.get_member(message.from_user.id).can_delete_messages):
            message.delete()
            message.reply_to_message.delete()
        else:
            message.reply_text("Imagine")
    else:
        message.reply_text("I don't have permission to delete messages here")
