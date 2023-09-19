"""
Shows this message
"""
from __future__ import annotations

import ast
from pathlib import Path

from pyrogram import emoji
from pyrogram import filters
from pyrogram import types
from pyrogram.client import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import Chat
from pyrogram.types import Message

import common
import DBManagement as DB

userBotDocs = {
    i.stem: ast.get_docstring(ast.parse(i.read_text(encoding="utf-8")))
    for i in Path("bots/userBot/modules").iterdir()
    if i.is_file()
}
shutUpDocs = {
    i.stem: ast.get_docstring(ast.parse(i.read_text()))
    for i in Path("bots/shutUp/modules").iterdir()
    if i.is_file()
}

userBotDocsButtonsFlat = [
    types.InlineKeyboardButton(doc, f"HELP:UB:{doc}") for doc in userBotDocs
]
userBotDocsButtons = common.partition(userBotDocsButtonsFlat, 3) + [
    [types.InlineKeyboardButton("See shutup docs", f"CHDOC:SU")],
]

shutupDocsButtonsFlat = [
    types.InlineKeyboardButton(doc, f"HELP:SU:{doc}") for doc in shutUpDocs
]
shutupDocsButtons = common.partition(shutupDocsButtonsFlat, 3) + [
    [types.InlineKeyboardButton("See userbot docs", f"CHDOC:UB")],
]


@Client.on_message(filters.command(["toggle"]))
async def toggleCommand(client: Client, message: Message):
    if len(message.command) == 3:
        if message.command[2] in userBotDocs | shutUpDocs:
            DB.groups.toggleCommand(
                int(message.command[1]),
                message.command[2],
            )
            chat = await client.get_chat(message.command[2])
            assert isinstance(chat, Chat)
            chatName = (
                common.getFullName(
                    chat,
                )
                if chat.type == "private"
                else chat.title
            )
            await message.reply_text(
                f"Module `{message.command[2]}` in chat `{chatName}` is now {f'ON{emoji.CHECK_MARK_BUTTON}' if common.isModuleToggled(int(message.command[1]), message.command[2]) else f'OFF{emoji.CROSS_MARK}'}",
            )
        else:
            await message.reply_text("Invalid command")
    else:
        await message.reply_text("Usage:\n/toggle group_id command")


@Client.on_message(filters.command(["help", f"help@{common.bot_username}"]))
async def help(client, message):
    await message.reply_text(
        "**Shutup** modules\n\nChoose the module you want help with and or want to enable/disable",
        reply_markup=types.InlineKeyboardMarkup(shutupDocsButtons),
    )


@Client.on_callback_query(filters.regex("^HELP"))
async def helpCallbackAnswer(client: Client, callback_query: CallbackQuery):
    assert isinstance(callback_query.data, str)
    args = callback_query.data.split(":")
    if args[1] == "SU":
        buttons = [
            [
                types.InlineKeyboardButton(
                    f"The module is {emoji.CHECK_MARK_BUTTON if common.isModuleToggled(callback_query.message.chat.id, args[2]) else emoji.CROSS_MARK}",
                    f"TOGGLE:SU:{args[2]}",
                ),
            ],
            [types.InlineKeyboardButton("Back", "CHDOC:SU")],
        ]
        await callback_query.message.edit(
            shutUpDocs.get(args[2]) or "",
            reply_markup=types.InlineKeyboardMarkup(buttons),
        )
    elif args[1] == "UB":
        buttons = [
            [
                types.InlineKeyboardButton(
                    f"The module is {emoji.CHECK_MARK_BUTTON if common.isModuleToggled(callback_query.message.chat.id, args[2]) else emoji.CROSS_MARK}",
                    f"TOGGLE:UB:{args[2]}",
                ),
            ],
            [types.InlineKeyboardButton("Back", "CHDOC:UB")],
        ]

        await callback_query.message.edit(
            userBotDocs[args[2]] or "",
            reply_markup=types.InlineKeyboardMarkup(buttons),
        )


@Client.on_callback_query(filters.regex("^CHDOC"))
async def chdocCallbackAnswer(client: Client, callback_query: CallbackQuery):
    assert isinstance(callback_query.data, str)
    args = callback_query.data.split(":")
    if args[1] == "SU":
        await callback_query.message.edit(
            "**Shutup** modules\n\nChoose the module you want help with and or want to enable/disable",
            reply_markup=types.InlineKeyboardMarkup(shutupDocsButtons),
        )
    elif args[1] == "UB":
        await callback_query.message.edit(
            "**userbot** modules\n\nChoose the module you want help with and or want to enable/disable",
            reply_markup=types.InlineKeyboardMarkup(userBotDocsButtons),
        )


@Client.on_callback_query(filters.regex("^TOGGLE"))
async def toggleCallbackAnswer(client: Client, callback_query: CallbackQuery):
    assert isinstance(callback_query.data, str)
    args = callback_query.data.split(":")
    assert isinstance(
        callback_query.message.reply_markup,
        types.InlineKeyboardMarkup,
    )
    markup = callback_query.message.reply_markup.inline_keyboard
    if args[1] == "SU":
        if (
            callback_query.from_user.id == common.owner_id
            or (
                await callback_query.message.chat.get_member(
                    callback_query.message.from_user.id,
                )
            ).status
            == "creator"
        ):
            value = not common.isModuleToggled(
                callback_query.message.chat.id,
                args[2],
            )
            DB.groups.toggleCommand(callback_query.message.chat.id, args[2])
            markup[0] = [
                types.InlineKeyboardButton(
                    f"The module is {emoji.CHECK_MARK_BUTTON if value else emoji.CROSS_MARK}",
                    f"TOGGLE:UB:{args[2]}",
                ),
            ]
            await callback_query.message.edit(
                callback_query.message.text,
                reply_markup=types.InlineKeyboardMarkup(markup),
            )
        else:
            await callback_query.answer(
                "Only the chat creator or the bot owner can change this",
            )
    elif args[1] == "UB":
        if callback_query.from_user.id == common.owner_id:
            value = not common.isModuleToggled(
                callback_query.message.chat.id,
                args[2],
            )
            DB.groups.toggleCommand(callback_query.message.chat.id, args[2])
            markup[0] = [
                types.InlineKeyboardButton(
                    f"The module is {emoji.CHECK_MARK_BUTTON if value else emoji.CROSS_MARK}",
                    f"TOGGLE:SU:{args[2]}",
                ),
            ]
            await callback_query.message.edit(
                callback_query.message.text,
                reply_markup=types.InlineKeyboardMarkup(markup),
            )
        else:
            await callback_query.answer(
                "The userbot can only be configured by the bot owner",
            )
