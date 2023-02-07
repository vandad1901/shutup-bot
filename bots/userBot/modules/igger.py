"""
I hope someday I can get rid of this. I hate the internet
"""
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

from common import isModuleToggledFilter

iggerEnable = False


@Client.on_message(filters.regex("^[NnんンنΝνНнנן]$") & filters.incoming & isModuleToggledFilter("igger"))
async def igger(client: Client, message: Message):
    global iggerEnable
    if (iggerEnable):
        await message.reply_sticker("CAADBAADQgADQ2rUGvEaOX-Bu7ucFgQ")
