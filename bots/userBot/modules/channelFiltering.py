"""
This module forward all messages from a channel that is not sent by a banned person and also does not contain the banend words. This is such a niche usage that I didn't even bother implenting a general use.
"""
from pyrogram import filters

from ..userbot import usr

tabbed = 0
bannedWords = ["#انگیزشی", "#توکل"]


@usr.on_message(filters.chat(-1001325902997))
async def filterChannel(client, message):
    if(message.author_signature != "Seyed mohammd Tabatabaie"):
        try:
            if((not message.caption) or (all(message.caption.find(i) == -1 for i in bannedWords))):
                await message.forward(-1001479340622)
        except:
            await message.forward(-1001479340622)
    else:
        global tabbed
        tabbed += 1
