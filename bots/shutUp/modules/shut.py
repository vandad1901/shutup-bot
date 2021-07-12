"""
Prevents all users except admins(not yet implemented sorry) from sending messages. also ignores every other command except itself.
To turn it off simply send the command again

Usage:
**/shut**
"""
from pyrogram import filters

from ..shutup import DB, app, isModuleToggledFilter, owner_id

isShut = filters.create(lambda _, __, query: bool(
    DB.groups.get(str(query.chat.id)).shut))


@app.on_message(filters.command(["shut", "shut@damnshutup_bot"]) & filters.group & isModuleToggledFilter("shut"), group=0)
async def shut(client, message):
    if((await message.chat.get_member(message.from_user.id)).can_delete_messages or message.from_user.id == owner_id):
        DB.groups.toggleShut(str(message.chat.id))
    else:
        await message.reply_text("You need delete permission in this group to be able to toggle \"shut\"")


@app.on_message(~filters.me & ~filters.edited & filters.group & isShut & isModuleToggledFilter("shut"), group=0)
async def deleteIfShut(client, message):
    print(f"{message.from_user.first_name} broke the shut")
    if(message.from_user.id != owner_id):
        try:
            await message.delete()
        except:
            await message.reply_text("Need delete permission")
