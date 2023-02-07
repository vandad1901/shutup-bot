"""
Various administrative commands

Usage:
**/setgifid**
reply to a gif or use the gif id as argument to set the /fuckyou gif if
**/dump**
dumps some basic info
"""
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

import DBManagement as DB
from common import bot_username, owner_id


@Client.on_message(filters.command(["setgifid", f"setgifid@{bot_username}"]))
async def setGifId(client: Client, message: Message):
    if (message.from_user.id == owner_id):
        try:
            animationId = message.reply_to_message.animation.file_id
        except:
            animationId = message.command[1]
        await message.reply_animation(animation=animationId, caption=f"The new animation id is: {animationId}")
        DB.animations.add(animationId)
    else:
        await message.reply_text("No")


@Client.on_message(filters.command(["dump"]))
async def dumpStuff(client: Client, message: Message):
    await message.reply_text(str(message.reply_to_message if message.reply_to_message else message))


@Client.on_message(filters.private, group=-1)
async def newId(client: Client, message: Message):
    userId = message.from_user.id
    if (DB.users.add(userId)):
        print(DB.users.get())
