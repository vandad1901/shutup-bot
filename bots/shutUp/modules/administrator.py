"""
Various administrative commands

Usage:
**/setgifid**
reply to a gif or use the gif id as argument to set the /fuckyou gif if
**/dump**
dumps some basic info
"""
from __future__ import annotations

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.errors import exceptions
from pyrogram.types import Message

import DBManagement as DB
from common import bot_username
from common import owner_id


@Client.on_message(filters.command(["setgifid", f"setgifid@{bot_username}"]))
async def setGifId(_: Client, message: Message):
    if message.from_user.id == owner_id:
        if message.reply_to_message:
            animationId = message.reply_to_message.animation.file_id
        elif len(message.command) == 2:
            animationId = message.command[1]
        try:
            await message.reply_animation(
                animation=animationId,
                caption=f"The new animation id is: {animationId}",
            )
        except (exceptions.BadRequest, UnboundLocalError):
            await message.reply_text("No valid animaion id found")
            return

        DB.animations.add(animationId)
    else:
        await message.reply_text("No")


@Client.on_message(filters.command(["dump"]))
async def dumpStuff(client: Client, message: Message):
    await message.reply_text(
        str(message.reply_to_message if message.reply_to_message else message),
    )


@Client.on_message(filters.private, group=-1)
async def newId(client: Client, message: Message):
    userId = message.from_user.id
    DB.users.add(userId)
