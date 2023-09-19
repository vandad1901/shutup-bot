"""
Basic module for pinning and unpinning messages.

Usage:
**/pin**
will pin the message that it was replied to
**/unpin**
will unpin the message that it was replied to or if it wasn't a reply to a message will unpin the latest message
"""
from __future__ import annotations

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Chat
from pyrogram.types import Message

from common import bot_username
from common import isModuleToggledFilter


@Client.on_message(
    filters.command(["pin", f"pin@{bot_username}"])
    & filters.group
    & isModuleToggledFilter("pin"),
)
async def pin(client: Client, message: Message):
    if (await message.chat.get_member("self")).privileges.can_pin_messages:
        if message.reply_to_message:
            await message.reply_to_message.pin()
            await message.reply_text(
                'You do know that you can just TOUCH THE GODDAMN MESSAGE AND SELECT "PIN MESSAGE" to pin a message right? Lazy ass millennials',
            )
        else:
            await message.reply_text("Pin what? Fucking retard")
            m = await message.reply_text(
                f"{message.from_user.first_name} is retarded",
                quote=False,
            )
            await m.pin()
    else:
        await message.reply_text("I don't have permission to pin messages here")


@Client.on_message(
    filters.command(["unpin", f"unpin@{bot_username}"])
    & filters.group
    & isModuleToggledFilter("pin"),
)
async def unpin(client: Client, message: Message):
    if (await message.chat.get_member("self")).privileges.can_pin_messages:
        if message.reply_to_message:
            await message.reply_to_message.unpin()
            await message.reply_text(
                'You do know that you can just TOUCH THE GODDAMN MESSAGE AND SELECT "UNPIN MESSAGE" to pin a message right? Lazy ass millennials',
            )
        else:
            chat = await client.get_chat(message.chat.id)
            assert isinstance(chat, Chat)
            if chat.pinned_message:
                await client.unpin_chat_message(message.chat.id, chat.pinned_message.id)
            else:
                await message.reply_text("No messages to unpin")
    else:
        await message.reply_text("I don't have permission to unpin messages here")
