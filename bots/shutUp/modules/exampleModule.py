"""
This is an example module to show what a module file should look like. Name the files in the camelCase style

Usage:
**/stuff** 
explanations
"""
# Import any pyrogram stuff here
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message

# Import things you need here like owner_id and such
import DBManagement as DB
from common import bot_username, owner_id

# Not every command needs the f"stuff@{bot_username}" variant. Use your own judgement


@Client.on_message(filters.command(["Stuff", f"stuff@{bot_username}"]))
# Name the arguments "client" and "message"
async def exampleCommandFunc(client: Client, message: Message):
    pass


# All callback query data should be all capitalized every "argument" for the callback query should be seperated by ":". e.g STUFF:DELETE:SOMEGROUP
@Client.on_callback_query(filters.regex("^STUFF"))
# Name the arguments "client" and "callback_query"
async def exampleCallbackQueryFunc(client: Client, callback_query: CallbackQuery):
    assert (isinstance(callback_query.data, str))
    args = callback_query.data.split(":")
    pass

# Thank you for contributing :)
