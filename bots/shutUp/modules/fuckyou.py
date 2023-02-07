"""
Replies a custom gif to you or the message you replied to

Usage:
**/fuckyou**
"""
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

import DBManagement as DB
from common import bot_username, isModuleToggledFilter


@Client.on_message(filters.command(["fuckyou", f"fuckyou@{bot_username}"]) & isModuleToggledFilter("fuckyou"))
async def fuckYou(client: Client, message: Message):
    try:
        anId = DB.animations.getLatest()["animation_id"]
    except:
        anId = "CgADBAADEgcAAqNhEVIQydI7mWvdvBYE"
        DB.animations.add(anId)
    if (message.reply_to_message):
        await message.reply_to_message.reply_animation(animation=anId)
    else:
        await message.reply_animation(animation=anId)
