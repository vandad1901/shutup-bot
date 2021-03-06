"""
Various administrative commands

Usage:
**/setgifid**
reply to a gif or use the gif id as argument to set the /fuckyou gif if
**/dump**
dumps some basic info
"""
from pyrogram import filters

from ..shutup import DB, app, bot_username, owner_id


@app.on_message(filters.command(["setgifid", f"setgifid@{bot_username}"]))
async def setGifId(client, message):
    if(message.from_user.id == owner_id):
        try:
            animationId = message.reply_to_message.animation.file_id
        except:
            animationId = message.command[1]
        await message.reply_animation(animation=animationId, caption=f"The new animation id is: {animationId}")
        DB.animations.add(animationId)
    else:
        await message.reply_text("No")


@app.on_message(filters.command(["dump"]))
async def dumpStuff(client, message):
    if(message.from_user.id == owner_id):
        await message.reply_text(str(message.reply_to_message if message.reply_to_message else message))
    else:
        await message.reply_text(
            "This command can only be used by the bot administrator (You're welcome)")


@app.on_message(filters.private, group=-1)
async def newId(client, message):
    userId = str(message.from_user.id)
    if(DB.users.add(userId)):
        print(DB.users.get())
