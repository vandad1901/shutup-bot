"""
Used to get you currently scrobbling song on last.fm

Usage:
**/lastfm**
to get your now playing song
**/lastfm_top
get top albums, artists, tracks or tags in a certain time period
**/setlastfm**
to set your lastfm username
"""
import itertools

import pylast
from pyrogram import emoji, filters

from ..shutup import (DB, app, getFullName, lastfm_key, lastfm_pass,
                      lastfm_secret, lastfm_user)

network = pylast.LastFMNetwork(
    api_key=lastfm_key,
    api_secret=lastfm_secret,
    username=lastfm_user,
    password_hash=pylast.md5(lastfm_pass),
)
timePeriods = {"overall": pylast.PERIOD_OVERALL, "week": pylast.PERIOD_7DAYS, "month": pylast.PERIOD_1MONTH,
               "3month": pylast.PERIOD_3MONTHS, "6month": pylast.PERIOD_6MONTHS, "year": pylast.PERIOD_12MONTHS}


@app.on_message(filters.command(["lastfm", "lastfm@damnshutup_bot"]))
async def getLastFMScrobbles(client, message):
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
        await message.reply_text(f"{getFullName(message.from_user)} is currently listening to:\n• **{nowPlaying.artist} - {nowPlaying.title}** {emoji.RED_HEART if nowPlaying.get_userloved() else emoji.BLACK_HEART}\n\nTheir total scrobble count is: {user.get_playcount()}")
    else:
        recentPlaying = user.get_recent_tracks(limit=3)
        if(recentPlaying):
            await message.reply_text(f"{getFullName(message.from_user)} is not currently listening to anything. But recently they've been listening to:\n{chr(10).join([f'• **{s.track.artist} - {s.track.title}** {emoji.RED_HEART if s.track.get_userloved() else emoji.BLACK_HEART}' for s in recentPlaying])}\n\nTheir total scrobble count is: {user.get_playcount()}")
        else:
            await message.reply_text(f"{getFullName(message.from_user)} has never scrobbled any songs")


@app.on_message(filters.command(["lastfm_top", "lastfm_top@damnshutup_bot"]))
async def getLastFMTops(client, message):
    lastFMName = DB.users.get(str(message.from_user.id)).lastfm
    if(not lastFMName):
        await message.reply_text("Set your last.fm username with /setlastfm")
        return
    user = network.get_user(lastFMName)

    try:
        assert(len(message.command) in (3, 4))
        assert(message.command[1] in ("artists", "tracks", "albums", "tags"))
        assert(message.command[2] in timePeriods)
        if(len(message.command) == 4):
            limit = int(message.command[3])
        else:
            limit = 5
    except:
        await message.reply_text("Usage:\n/lastfm_top type period limit\ntype: Either track, album, artist or tags\nperiod: overall, week, month, 3month, 6month, year(The only available option for tags is overall)\nlimit: Number of results(Defaults to 5)")
        return
    try:
        type = message.command[1]
        period = timePeriods[message.command[2]]
        # TODO change to switch in python 3.10
        if(type == "artists"):
            results = user.get_top_artists(period, limit)
            await message.reply_text(
                f"**{getFullName(message.from_user)}**'s top artist{'s are' if len(results)>1 else ' is'}:\n{chr(10).join([f'{s[0]}. {s[1].item.name}' for s in zip(itertools.count(1), results)])}")

        elif(type == "albums"):
            results = user.get_top_albums(period, limit)
            await message.reply_text(
                f"**{getFullName(message.from_user)}**'s top album{'s are' if len(results)>1 else ' is'}:\n{chr(10).join([f'{s[0]}. {s[1].item.artist} - {s[1].item.title}' for s in zip(itertools.count(1), results)])}")

        elif(type == "tracks"):
            results = user.get_top_tracks(period, limit)
            await message.reply_text(
                f"**{getFullName(message.from_user)}**'s top track{'s are' if len(results)>1 else ' is'}:\n{chr(10).join([f'{s[0]}. {s[1].item.artist} - {s[1].item.title}' for s in zip(itertools.count(1), results)])}")

        elif(type == "tags"):
            results = user.get_top_tags(limit)
            await message.reply_text(
                f"**{getFullName(message.from_user)}**'s top tag{'s are' if len(results)>1 else ' is'}:\n{chr(10).join([f'{s[0]}. {s[1].name}' for s in zip(itertools.count(1), results)])}")

    except:
        await message.reply_text(f"Something went wrong. Is **{lastFMName}** your username?")


@app.on_message(filters.command(["setlastfm", "setlastfm@damnshutup_bot"]))
async def setLastFMName(client, message):
    if(len(message.command) == 2):
        DB.users.setLastfm(str(message.from_user.id), message.command[1])
        await message.reply_text(f"Successfully set your lastfm username to {message.command[1]}")
    else:
        await message.reply_text("Usage:\n/setlastfm username")
