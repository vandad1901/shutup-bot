"""
Module for Youtube downloading

Usage:
**/youtube link** 
Lists format ids for a link
**/youtube link quality**
Downloads the video with the selected quality
"""
from pathlib import Path

import yt_dlp as youtube_dl
from common import async_wrap
from pyrogram import filters

from ..shutup import app, bot_username


class MyLogger():
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print("error")


@app.on_message((filters.command(["youtube", f"youtube@{bot_username}"]) | filters.regex("^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?")) & ~filters.edited)
async def youtubeGetInfo(client, message):
    if(not message.command):
        message.command = ["/youtube"] + message.text.split()
    ydl_opts = {
        "outtmpl": f"%(title)s {message.from_user.id}.%(ext)s",
        "logger": MyLogger(),
        "format_sort": ["height", "tbr"],
        "merge_output_format": "mp4"}
    if(len(message.command) == 2):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = message.command[1]
            result = ydl.extract_info(url, download=False)
            formats = result["formats"]
            highest_qualities = {}
            filtered_formats = [
                f for f in formats if "dash" in f.get("container", "")]
            if not formats:
                filtered_formats = formats
            for format in filtered_formats:
                highest_qualities.update({format['format_note']: format})
            await message.reply_text("\n".join([f"{f['format_note']}: {f['format_id']}" for f in highest_qualities.values()]+["\nTo mix video and audio, use \"video quality+audio quality\""]))
    elif len(message.command) == 3:
        ydl_opts.update({
            "format": message.command[2]})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = message.command[1]
            result = await async_wrap(ydl.extract_info)(url, download=True)
            fname = ydl.prepare_filename(result)
            if("audio only" in result["format"] and "+" not in result["format"]):
                await message.reply_audio(
                    fname, duration=result["duration"], title=result["title"])
            else:
                await message.reply_video(
                    fname, duration=result["duration"], width=result["width"], height=result["height"])
            Path(fname).unlink(missing_ok=True)
    else:
        await message.reply_text('Usage:\n/youtube link\n/youtube link quality')


@app.on_callback_query(filters.regex("^YTDL"))
async def exampleCallbackQueryFunc(client, callback_query):
    args = callback_query.data.split(":")
    pass
