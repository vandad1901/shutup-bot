"""
Replies a custom gif to you or the message you replied to

Usage:
**/fuckyou**
"""
from common import isModuleToggledFilter
from pyrogram import filters

from ..shutup import DB, app, bot_username


@app.on_message(filters.command(["fuckyou", f"fuckyou@{bot_username}"]) & isModuleToggledFilter("fuckyou"))
async def fuckYou(client, message):
    try:
        anId = DB.animations.get()[-1].animationid
    except:
        DB.animations.add("CgADBAADEgcAAqNhEVIQydI7mWvdvBYE")
        anId = "CgADBAADEgcAAqNhEVIQydI7mWvdvBYE"
    if(message.reply_to_message):
        await message.reply_to_message.reply_animation(animation=anId)
    else:
        await message.reply_animation(animation=anId)
