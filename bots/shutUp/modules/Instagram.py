"""
Module for Instagram downloading

Usage:
**/instagram link** 
Lists format ids for a link
**/instagram link quality**
Downloads the video with the selected quality
"""
import re
import shutil
from pathlib import Path

import instaloader
from pyrogram import filters, enums
from pyrogram.client import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo, Message

from common import bot_username

L = instaloader.instaloader.Instaloader(quiet=True)


@Client.on_message((filters.command(["instagram", f"instagram@{bot_username}"]) | filters.regex("((?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reels?)\/([^/?#&]+)).*")))  # type: ignore
async def youtubeGetInfo(_: Client, message: Message) -> None:
    if not message.command:
        message.command = ["/instagram"] + message.text.split()
    if len(message.command) == 1:
        await message.reply_text("Usage:\n/instagram link")
        return
    await message.reply_chat_action(enums.ChatAction.TYPING)
    postPath = downloadFromLink(message.command[1].split("/")[4])
    caption = getCaption(postPath)

    if message.command[1].split("/")[3] == "p":
        mediaList = makeMediaList(postPath)
        mediaList[0].caption = caption
        await message.reply_chat_action(
            enums.ChatAction.UPLOAD_VIDEO
            if type(mediaList[0]) == InputMediaVideo
            else enums.ChatAction.UPLOAD_PHOTO
        )
        await message.reply_media_group(mediaList, quote=True)
        await message.reply_chat_action(enums.ChatAction.CANCEL)
    else:
        videoPath = list(postPath.glob("*.mp4"))[0]
        thumbPath = list(postPath.glob("*.jpg"))[0]
        await message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
        await message.reply_video(
            str(videoPath), thumb=str(thumbPath), caption=caption, quote=True
        )
        await message.reply_chat_action(enums.ChatAction.CANCEL)
    shutil.rmtree(postPath, ignore_errors=True)


def downloadFromLink(link: str) -> Path:
    postId = link
    post = instaloader.structures.Post.from_shortcode(L.context, postId)
    L.download_post(post, postId)
    postPath = Path(postId)
    return postPath


def getCaption(postPath: Path) -> str:
    txtFiles = list(postPath.glob("*.txt"))
    caption = txtFiles[0].read_text() if len(txtFiles) > 0 else ""
    return caption


def customFileSortKey(item: Path) -> tuple[int, int] | Path:
    match = re.match(r".*_(\d+)(\..+)", str(item))
    if match:
        return (int(match.group(1)), 0 if match.group(2) == ".mp4" else 1)
    else:
        return item


def makeMediaList(postPath: Path) -> list[InputMediaPhoto | InputMediaVideo]:
    rawMediaList = sorted(
        (f for f in postPath.glob("*") if f.suffix not in {".xz", ".txt"}),
        key=customFileSortKey,
    )
    finalMediaList: list[InputMediaPhoto | InputMediaVideo] = []
    i = 0
    while i < len(rawMediaList):
        if rawMediaList[i].suffix == ".mp4":
            finalMediaList.append(
                InputMediaVideo(str(rawMediaList[i]), thumb=str(rawMediaList[i + 1]))
            )
            i += 1
        else:
            finalMediaList.append(InputMediaPhoto(str(rawMediaList[i])))
        i += 1
    return finalMediaList
