"""
Sends a customizable message when users join or leave the group

Usage:
**/setwelcome**
Set the welcome message to the command argument
Or reply it to a message containing media to use that message from welcome
**/setbye**
Same as /setwelcome but for the farewell message
"""
from pyrogram import Client, filters

import DBManagement as DB
from common import bot_username, isModuleToggledFilter, owner_id


@Client.on_message(filters.new_chat_members & isModuleToggledFilter("greetings"))
async def welcome(client, message):
    if (any([u.is_self for u in message.new_chat_members])):
        await message.reply("Hewwo thwank you fow awdding me")
    elif (any(u.id == owner_id for u in message.new_chat_members)):
        await message.reply("Daddy")
    elif (not all([u.is_self for u in message.new_chat_members])):
        welcomeMessage = DB.groups.get(message.chat.id)["welcome"]
        if (not welcomeMessage):
            return
        welcomeMessage._client = client
        await welcomeMessage.copy(message.chat.id, reply_to_message_id=message.message_id)


@Client.on_message(filters.left_chat_member & isModuleToggledFilter("greetings"))
async def goodbye(client, message):
    if (message.left_chat_member.id == owner_id):
        await message.reply("Daddy")
    else:
        byeMessage = DB.groups.get(message.chat.id)["bye"]
        if (not byeMessage):
            return
        byeMessage._client = client
        await byeMessage.copy(message.chat.id, reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["setwelcome", f"setwelcome@{bot_username}"]) & filters.group & isModuleToggledFilter("greetings"))
async def setWelcome(client, message):
    if (message.reply_to_message):
        DB.groups.setWelcome(message.chat.id, message.reply_to_message)
        await message.reply_text("Successfully set the welcome message")
    else:
        message.text = " ".join(message.command[1:])
        DB.groups.setWelcome(message.chat.id, message)
        await message.reply_text(f"Successfully set the welcome message to: {' '.join(message.command[1:])}")


@Client.on_message(filters.command(["setbye", f"setbye@{bot_username}"]) & filters.group & isModuleToggledFilter("greetings"))
async def setBye(client, message):
    if (message.reply_to_message):
        DB.groups.setBye(message.chat.id, message.reply_to_message)
        await message.reply_text("Successfully set the goodbye message")
    else:
        message.text = " ".join(message.command[1:])
        DB.groups.setBye(message.chat.id, message)
        await message.reply_text(f"Successfully set the goodbye message to: {' '.join(message.command[1:])}")
