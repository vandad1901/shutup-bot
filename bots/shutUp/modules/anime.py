"""
Anime info module

**/anime**
Searches Anilist for an anime
**/character**
Searches Anilist for a character
"""
from anilistpy import Anime, Character, animeSearch, charSearch
from common import makeButtons
from pyrogram import filters, types

from ..shutup import app, bot_username


@app.on_message(filters.command(["anime", f"anime@{bot_username}"]))
async def getAnimeSearch(client, message):
    query = " ".join(message.command[1:])
    result = animeSearch(query)
    await message.reply_photo("https://anilist.co/img/icons/android-chrome-512x512.png", "Select anime", reply_markup=types.InlineKeyboardMarkup(makeButtons([types.InlineKeyboardButton(anime["title"]["romaji"], f"ANI:{anime['id']}") for anime in result.media], 1)))


@app.on_message(filters.command(["character", f"character@{bot_username}"]))
async def getCharacterSearch(client, message):
    query = " ".join(message.command[1:])
    result = charSearch(query)
    await message.reply_photo("https://anilist.co/img/icons/android-chrome-512x512.png", "Select character", reply_markup=types.InlineKeyboardMarkup(makeButtons([types.InlineKeyboardButton(character["name"]["full"], f"CHR:{character['id']}") for character in result.media], 1)))


@app.on_callback_query(filters.regex("ANI"))
async def getAnime(client, callback_query):
    args = callback_query.data.split(":")
    anime = Anime(args[1])
    msg1 = f"""
**Title:** {anime.title("romaji")}({anime.title("english")})
**Genres:** {", ".join(anime.genres())}
**Episodes:** {anime.episodes()}
**Duration:** {anime.duration()} minute
**Status:** {anime.status()}
**Ratings:** {anime.averageScore()}/100

**Characters:** {", ".join([ch["node"]["name"]["full"] for ch in anime.media[0]["characters"]["edges"]])}
**Description:**"""
    msg2 = f"""
**Studios:** {", ".join(anime.studios())}
**Tags:** {" ".join(["#"+tag.replace(" ","_").replace("-","_") for tag in anime.tags()])}
"""
    await callback_query.message.edit_media(types.InputMediaPhoto(anime.coverImage("extraLarge"), msg1 + anime.description()[:(1019-len(msg1)-len(msg2))]+"...\n"+msg2))


@app.on_callback_query(filters.regex("CHR"))
async def getCharacter(client, callback_query):
    args = callback_query.data.split(":")
    character = Character(args[1])
    caption = f"""
**Name:** {character.name("full")}({character.name("native")})
**Description:**
{character.description()}
"""
    await callback_query.message.edit_media(types.InputMediaPhoto(character.image("large"), caption[:1021]+"..."))
