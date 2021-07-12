"""
Used to get you currently scrobbling song on last.fm

Usage:
**/lastfm**
to get your now playing song
**/setlastfm**
to set your lastfm username
"""
import pylast
from pyrogram import emoji, filters

from ..shutup import (DB, app, lastfm_key, lastfm_pass, lastfm_secret,
                      lastfm_user)

network = pylast.LastFMNetwork(
    api_key=lastfm_key,
    api_secret=lastfm_secret,
    username=lastfm_user,
    password_hash=pylast.md5(lastfm_pass),
)


@app.on_message(filters.command(["lastfm", "lastfm@damnshutup_bot"]))
async def getLastFM(client, message):
    lastFMName = DB.users.get(str(message.from_user.id)).lastfm
    if(not lastFMName):
        await message.reply_text("Set your last.fm username with /setlastfm")
        return
    user = network.get_user(lastFMName)
    try:
        nowPlaying = user.get_now_playing()
    except pylast.WSError:
        await message.reply_text(f"Something went wrong. Is **{lastFMName}** your username?")
        return
    if(nowPlaying):
        await message.reply_text(f"{message.from_user.first_name} is currently listening to:\n• **{nowPlaying.artist} - {nowPlaying.title}** {emoji.RED_HEART if nowPlaying.get_userloved() else emoji.BLACK_HEART}\n\nTheir total scrobble count is: {user.get_playcount()}")
    else:
        recentPlaying = user.get_recent_tracks(limit=3)
        if(recentPlaying):
            await message.reply_text(f"{message.from_user.first_name} is not currently listening to anything. But recently they've been listening to:\n{chr(10).join([f'• **{s.track.artist} - {s.track.title}** {emoji.RED_HEART if s.track.get_userloved() else emoji.BLACK_HEART}' for s in recentPlaying])}\n\nTheir total scrobble count is: {user.get_playcount()}")
        else:
            await message.reply_text(f"{message.from_user.first_name} has never scrobbled any songs")


@app.on_message(filters.command(["setlastfm", "setlastfm@damnshutup_bot"]))
async def setLastFMName(client, message):
    if(len(message.command) == 2):
        DB.users.setLastfm(str(message.from_user.id), message.command[1])
        await message.reply_text(f"Successfully set your lastfm username to {message.command[1]}")
    else:
        await message.reply_text("Usage:\n/setlastfm username")
