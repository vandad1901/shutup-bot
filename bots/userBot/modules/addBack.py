"""
Adds certain users back when they get banned from groups you specify. Group admins probably won't like this

Usage:
**/toggleaddback**
Toggles wether a certain user should be added back everytime they're removed from the chat. either reply to the user or have their id or username as the command argument
"""
from pyrogram import filters

from ..userbot import DB, app, isModuleToggledFilter, usr


@usr.on_message(filters.left_chat_member & isModuleToggledFilter("addBack"))
async def addBack(client, message):
    if(DB.groups.get(message.chat.id).addbacks.get(str(message.left_chat_member.id))):
        await message.chat.add_members(message.left_chat_member.id)
        print(f"Added {message.left_chat_member.first_name}")


@app.on_message(filters.group & filters.command((["toggleaddback", "toggleaddback@damnshutup_bot"])) & isModuleToggledFilter("addBack"))
async def addAddback(client, message):
    addbackGroup = message.chat.id
    if(message.reply_to_message):
        addbackId = message.reply_to_message.from_user.id
    elif(len(message.command) > 1):
        if(message.command[1].isnumeric()):
            addbackId = int(message.command[1])
        else:
            try:
                addbackId = (await client.get_users(message.command[1])).id
            except Exception as E:
                await message.reply_text(f"Invalid user identifier: {message.command[1]}")
                return
        if(len(message.command) == 3):
            if(message.command[1].isnumeric()):
                addbackGroup = int(message.command[2])
            else:
                await message.reply_text(f"Invalid group identifier: {message.command[2]}")
                return
    else:
        message.reply_text("No user identifier")
    if(not DB.groups.get(addbackGroup).addbacks.get(str(addbackId))):
        DB.groups.toggleAddback(addbackGroup, addbackId)
        await message.reply_text(f"Successfully turned on addback for {addbackId} in group {addbackGroup}")
    else:
        DB.groups.toggleAddback(addbackGroup, addbackId)
        await message.reply_text(f"Successfully turned off addback for {addbackId} in group {addbackGroup}")
