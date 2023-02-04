"""
Basic module for pinning and unpinning messages.

Usage:
**/pin**
will pin the message that it was replied to
**/unpin**
will unpin the message that it was replied to or if it wasn't a reply to a message will unpin the latest message
"""
from pyrogram import Client, filters

from common import bot_username, isModuleToggledFilter


@Client.on_message(filters.command(["pin", f"pin@{bot_username}"]) & filters.group & isModuleToggledFilter("pin"))
def pin(client, message):
    if (message.chat.get_member("self").can_pin_messages):
        if (message.reply_to_message):
            message.reply_to_message.pin()
            message.reply_text(
                "You do know that you can just TOUCH THE GODDAMN MESSAGE AND SELECT \"PIN MESSAGE\" to pin a message right? Lazy ass millennials")
        else:
            message.reply_text("Pin what? Fucking retard")
            m = message.reply_text(
                f"{message.from_user.first_name} is retarded", quote=False)
            m.pin()
    else:
        message.reply_text("I don't have permission to pin messages here")


@Client.on_message(filters.command(["unpin", f"unpin@{bot_username}"]) & filters.group & isModuleToggledFilter("pin"))
def unpin(client, message):
    if (message.chat.get_member("self").can_pin_messages):
        if (message.reply_to_message):
            message.reply_to_message.unpin()
            message.reply_text(
                "You do know that you can just TOUCH THE GODDAMN MESSAGE AND SELECT \"UNPIN MESSAGE\" to pin a message right? Lazy ass millennials")
        else:
            client.unpin_chat_message(message.chat.id, client.get_chat(
                message.chat.id).pinned_message.id)
    else:
        message.reply_text("I don't have permission to unpin messages here")
