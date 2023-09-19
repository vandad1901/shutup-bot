"""
Resizes the replied to images to meet the sticker requirements (less than 512x512)

Usage:
**/stickerize**
"""
from __future__ import annotations

import os

from PIL import Image
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

from common import bot_username
from common import isModuleToggledFilter


@Client.on_message(
    filters.command(["stickerize", f"stickerize@{bot_username}"])
    & isModuleToggledFilter("stickerize"),
)
async def stickerize(client: Client, message: Message):
    if message.reply_to_message:
        imgPath = await message.reply_to_message.download()
        img = Image.open(imgPath)
        img.thumbnail((512, 512))
        w, h = img.size

        if w > h:
            img = img.resize((512, (512 * h) // w))
        else:
            img = img.resize(((512 * w) // h, 512))
        imgName = (
            f"temp_{message.reply_to_message.chat.id}_{message.reply_to_message.id}"
        )
        img.save(f"{imgName}.webp", "webp")
        img.save(f"{imgName}.png", "webp")
        await message.reply_document(f"{imgName}.webp")
        await message.reply_document(f"{imgName}.png")
        try:
            os.remove(f"{imgName}.webp")
            os.remove(f"{imgName}.png")
            os.remove(imgPath)
        except:
            pass
    else:
        await message.reply_text("You must reply this command to an image")
