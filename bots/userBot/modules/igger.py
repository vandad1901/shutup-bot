"""
I hope someday I can get rid of this. I hate the internet
"""
from pyrogram import filters

from ..userbot import usr, isModuleToggledFilter

iggerEnable = True


@usr.on_message(filters.regex("^[NnんンنΝνНнנן]$") & filters.incoming & isModuleToggledFilter("igger"))
async def igger(client, message):
    global iggerEnable
    if(iggerEnable):
        await message.reply_sticker("CAADBAADQgADQ2rUGvEaOX-Bu7ucFgQ")
