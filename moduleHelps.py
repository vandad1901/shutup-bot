from pyrogram import emoji, filters, types

import bots.shutUp as SU
import bots.userBot as UB
import common
import DBManagement as DB

userBotDocs = {}
shutUpDocs = {}
for i in UB.modules.allFiles:
    userBotDocs[i] = eval(f"UB.{i}.__doc__")
for i in SU.modules.allFiles:
    shutUpDocs[i] = eval(f"SU.{i}.__doc__")


userBotDocsButtons = [types.InlineKeyboardButton(
    doc, f"HELP:UB:{doc}") for doc in userBotDocs]
userBotDocsButtons = common.makeButtons(
    userBotDocsButtons, 3) + [[types.InlineKeyboardButton("See shutup docs", f"CHDOC:SU")]]

shutupDocsButtons = [types.InlineKeyboardButton(
    doc, f"HELP:SU:{doc}") for doc in shutUpDocs]
shutupDocsButtons = common.makeButtons(
    shutupDocsButtons, 3) + [[types.InlineKeyboardButton("See userbot docs", f"CHDOC:UB")]]


@SU.app.on_message(filters.command(["toggle"]))
async def toggleCommand(client, message):
    if(len(message.command) == 3):
        if(message.command[2] in userBotDocs | shutUpDocs):
            DB.groups.toggleCommand(
                message.command[1], message.command[2])
            chat = await client.get_chat(message.command[2])
            chat = common.getFullName(chat) if chat.type =="private" else chat.title()
            await message.reply_text(f"Module `{message.command[2]}` in chat `{chat}` is now {f'ON{emoji.CHECK_MARK_BUTTON}' if common.isModuleToggled(message.command[1], message.command[2]) else f'OFF{emoji.CROSS_MARK}'}")
        else:
            await message.reply_text("Invalid command")
    else:

        await message.reply_text("Usage:\n/toggle group_id command")


@SU.app.on_message(filters.command(["help", f"help@{common.bot_username}"]))
async def help(client, message):
    await message.reply_text(
        "**Shutup** modules\n\nChoose the module you want help with and or want to enable/disable", reply_markup=types.InlineKeyboardMarkup(shutupDocsButtons))


@SU.app.on_callback_query(filters.regex("^HELP"))
async def helpCallbackAnswer(client, callback_query):
    args = callback_query.data.split(":")
    if(args[1] == "SU"):
        buttons = [[types.InlineKeyboardButton(
            f"The module is {emoji.CHECK_MARK_BUTTON if common.isModuleToggled(callback_query.message.chat.id, args[2]) else emoji.CROSS_MARK}", f"TOGGLE:SU:{args[2]}")], [types.InlineKeyboardButton("Back", "CHDOC:SU")]]
        await callback_query.message.edit(shutUpDocs[args[2]], reply_markup=types.InlineKeyboardMarkup(buttons))
    elif(args[1] == "UB"):
        buttons = [[types.InlineKeyboardButton(
            f"The module is {emoji.CHECK_MARK_BUTTON if common.isModuleToggled(callback_query.message.chat.id, args[2]) else emoji.CROSS_MARK}", f"TOGGLE:UB:{args[2]}")], [types.InlineKeyboardButton("Back", "CHDOC:UB")]]
        await callback_query.message.edit(userBotDocs[args[2]], reply_markup=types.InlineKeyboardMarkup(buttons))


@SU.app.on_callback_query(filters.regex("^CHDOC"))
async def chdocCallbackAnswer(client, callback_query):
    args = callback_query.data.split(":")
    if(args[1] == "SU"):
        await callback_query.message.edit(
            "**Shutup** modules\n\nChoose the module you want help with and or want to enable/disable", reply_markup=types.InlineKeyboardMarkup(shutupDocsButtons))
    elif(args[1] == "UB"):
        await callback_query.message.edit(
            "**userbot** modules\n\nChoose the module you want help with and or want to enable/disable", reply_markup=types.InlineKeyboardMarkup(userBotDocsButtons))


@SU.app.on_callback_query(filters.regex("^TOGGLE"))
async def toggleCallbackAnswer(client, callback_query):
    args = callback_query.data.split(":")
    markup = callback_query.message.reply_markup.inline_keyboard
    if(args[1] == "SU"):
        if(callback_query.from_user.id == common.owner_id or (await callback_query.message.chat.get_member(callback_query.message.from_user.id)).status == "creator"):
            value = not common.isModuleToggled(
                callback_query.message.chat.id, args[2])
            DB.groups.toggleCommand(
                callback_query.message.chat.id, args[2])
            markup[0] = [types.InlineKeyboardButton(
                f"The module is {emoji.CHECK_MARK_BUTTON if value else emoji.CROSS_MARK}", f"TOGGLE:UB:{args[2]}")]
            await callback_query.message.edit(callback_query.message.text, reply_markup=types.InlineKeyboardMarkup(markup))
        else:
            await callback_query.answer("Only the chat creator or the bot owner can change this")
    elif(args[1] == "UB"):
        if(callback_query.from_user.id == common.owner_id):
            value = not common.isModuleToggled(
                callback_query.message.chat.id, args[2])
            DB.groups.toggleCommand(
                callback_query.message.chat.id, args[2])
            markup[0] = [types.InlineKeyboardButton(
                f"The module is {emoji.CHECK_MARK_BUTTON if value else emoji.CROSS_MARK}", f"TOGGLE:SU:{args[2]}")]
            await callback_query.message.edit(callback_query.message.text, reply_markup=types.InlineKeyboardMarkup(markup))
        else:
            await callback_query.answer("The userbot can only be configured by the bot owner")
