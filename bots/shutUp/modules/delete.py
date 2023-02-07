"""
Deletes the message it was replied to

Usage:
**/del**
"""
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

from common import bot_username, isModuleToggledFilter, owner_id


@Client.on_message(filters.command(["del", f"del@{bot_username}"]) & filters.group & isModuleToggledFilter("delete"))
async def deleteCommand(client: Client, message: Message):
    if ((await message.chat.get_member("self")).privileges.can_delete_messages):
        if (message.from_user.id == owner_id or (await message.chat.get_member(message.from_user.id)).privileges.can_delete_messages):
            await message.delete()
            await message.reply_to_message.delete()
        else:
            await message.reply_text("Imagine")
    else:
        await message.reply_text("I don't have permission to delete messages here")
