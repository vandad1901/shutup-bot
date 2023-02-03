"""
Prevents all users except admins(not yet implemented sorry) from sending messages. also ignores every other command except itself.
To turn it off simply send the command again

Usage:
**/shut**
"""
from pyrogram import filters

import DBManagement as DB
from common import bot_username, isModuleToggledFilter, owner_id

from ..shutup import app

isShut = filters.create(lambda _, __, query: bool(DB.groups.get(query.chat.id)["shut"]))


@app.on_message(filters.command(["shut", f"shut@{bot_username}"]) & filters.group & isModuleToggledFilter("shut"), group=0)
async def shut(client, message):
    if ((await message.chat.get_member(message.from_user.id)).can_delete_messages or message.from_user.id == owner_id):
        DB.groups.toggleShut(message.chat.id)
    else:
        await message.reply_text("You need delete permission in this group to be able to toggle \"shut\"")


@app.on_message(~filters.me & filters.group & isShut & isModuleToggledFilter("shut"), group=0)
async def deleteIfShut(client, message):
    print(f"{message.from_user.first_name} broke the shut")
    if (message.from_user.id != owner_id):
        try:
            await message.delete()
        except:
            await message.reply_text("Need delete permission")
