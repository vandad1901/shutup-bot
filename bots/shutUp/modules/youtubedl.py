"""
Module for Youtube downloading

Usage:
**/youtube link**
Lists format ids for a link
**/youtube link quality**
Downloads the video with the selected quality
"""
from __future__ import annotations

from pathlib import Path

import yt_dlp as youtube_dl
from PIL import Image
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import Message

from common import async_wrap
from common import bot_username


class MyLogger:
    def debug(self, _):
        pass

    def warning(self, _):
        pass

    def error(self, _):
        pass


@Client.on_message(
    (
        filters.command(["youtube", f"youtube@{bot_username}"])
        | filters.regex(
            r"^(?:https?:\/\/)?(?:www\.)?(?:music\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?",
        )
    ),
)
async def youtubeGetInfo(client: Client, message: Message):
    if not message.command:
        message.command = ["/youtube"] + message.text.split()
        if len(message.text.split()) == 1:
            return
    ydl_opts = {
        "outtmpl": f"%(title)s {message.from_user.id}.%(ext)s",
        "logger": MyLogger(),
        "format_sort": ["height", "tbr"],
        "merge_output_format": "mp4",
        "writethumbnail": True,
    }
    if len(message.command) == 2:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = message.command[1]
            result = ydl.extract_info(url, download=False)
            if result is None:
                await message.reply_text("Unrecognized link. Please try again")
                return
            formats = result["formats"]
            highest_qualities = {}
            filtered_formats = [f for f in formats if "dash" in f.get("container", "")]
            if not formats:
                filtered_formats = formats
            for format in filtered_formats:
                highest_qualities.update({format["format_note"]: format})
            await message.reply_text(
                "\n".join(
                    [
                        f"{f['format_note']}: {f['format_id']}"
                        for f in highest_qualities.values()
                    ]
                    + [
                        '\nTo mix video and audio, use "video quality+audio quality"\nYou can also download the best audio quality by putting "audio" as the quality',
                    ],
                ),
            )
    elif len(message.command) == 3:
        if message.command[2] == "audio":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                },
            )
        else:
            ydl_opts.update({"format": message.command[2]})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = message.command[1]
            try:
                result = await async_wrap(ydl.extract_info)(url, download=True)
            except youtube_dl.DownloadError as e:
                if "Requested format is not available" in e.msg:
                    await message.reply_text(
                        "Requested format is not available\nSee available formats with\n**/youtube link**",
                    )
                    return
                else:
                    raise e
            filename = Path(ydl.prepare_filename(result))
            thumbName = filename.with_suffix(".webp")
            with Image.open(thumbName).convert("RGBA") as t:
                t.thumbnail((320, 320))
                new_image = Image.new("RGBA", t.size, "WHITE")
                new_image.paste(t, mask=t)
                new_image.convert("RGB").save(thumbName, "webp")
            if "audio only" in result["format"] and "+" not in result["format"]:
                filename = filename.rename(filename.with_suffix(".m4a"))
                try:
                    await message.reply_audio(
                        str(filename),
                        duration=result["duration"],
                        title=result["track"],
                        performer=result["artist"],
                        thumb=str(thumbName),
                    )
                except:
                    await message.reply_audio(
                        str(filename),
                        duration=result["duration"],
                        title=result["title"],
                        performer=result["uploader"],
                        thumb=str(thumbName),
                    )
            else:
                await message.reply_video(
                    str(filename),
                    duration=result["duration"],
                    width=result["width"],
                    height=result["height"],
                )
            filename.unlink(missing_ok=True)
            thumbName.unlink(missing_ok=True)
    else:
        await message.reply_text("Usage:\n/youtube link\n/youtube link quality")


@Client.on_callback_query(filters.regex("^YTDL"))
async def exampleCallbackQueryFunc(client: Client, callback_query: CallbackQuery):
    assert isinstance(callback_query.data, str)
    args = callback_query.data.split(":")
    pass
