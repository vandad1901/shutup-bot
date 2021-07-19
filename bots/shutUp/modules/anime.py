"""
Anime info module

**/anime**
Searches Anilist for an anime
**/character**
Searches Anilist for a character
"""
from anilistpy import (Anime, Character, Manga, animeSearch, charSearch,
                       mangaSearch)
from common import makeButtons
from pyrogram import filters, types

from ..shutup import app, bot_username


@app.on_message(filters.command(["anime", f"anime@{bot_username}"]))
async def getAnimeSearch(client, message):
    if(len(message.command) < 2):
        await message.reply_text('Usage:\n/anime anime name')
        return
    query = " ".join(message.command[1:])
    result = animeSearch(query)
    await message.reply_photo("https://anilist.co/img/icons/android-chrome-512x512.png", "Select anime", reply_markup=types.InlineKeyboardMarkup(makeButtons([types.InlineKeyboardButton(anime["title"]["romaji"], f"ANI:{anime['id']}") for anime in result.media], 1)))


@app.on_message(filters.command(["manga", f"manga@{bot_username}"]))
async def getMangaSearch(client, message):
    if(len(message.command) < 2):
        await message.reply_text('Usage:\n/manga manga name')
        return
    query = " ".join(message.command[1:])
    result = mangaSearch(query)
    await message.reply_photo("https://anilist.co/img/icons/android-chrome-512x512.png", "Select manga", reply_markup=types.InlineKeyboardMarkup(makeButtons([types.InlineKeyboardButton(manga["title"]["romaji"], f"MANGA:{manga['id']}") for manga in result.media], 1)))


@app.on_message(filters.command(["character", f"character@{bot_username}"]))
async def getCharacterSearch(client, message):
    if(len(message.command) < 2):
        await message.reply_text('Usage:\n/character character name')
        return
    query = " ".join(message.command[1:])
    result = charSearch(query)
    await message.reply_photo("https://anilist.co/img/icons/android-chrome-512x512.png", "Select character", reply_markup=types.InlineKeyboardMarkup(makeButtons([types.InlineKeyboardButton(character["name"]["full"], f"CHR:{character['id']}") for character in result.media], 1)))


@app.on_callback_query(filters.regex("ANI"))
async def getAnime(client, callback_query):
    args = callback_query.data.split(":")
    anime = Anime(args[1])
    msg1 = f"""
**Title:** {anime.title("romaji")}{f"({anime.title('english')})" if anime.title("english") else ""}
**Genres:** {", ".join(anime.genres())}
**Episodes:** {anime.episodes()} ({anime.status().replace("_"," ").lower().capitalize()}){f'''
**Duration:** {anime.duration()} minute{"s" if anime.duration()>1 else ""}''' if anime.duration() else ""}
**Ratings:** {anime.averageScore()}/100

**Characters:** {", ".join([ch["node"]["name"]["full"] for ch in anime.media[0]["characters"]["edges"]])}
**Description:**"""
    msg2 = f"""
**Studios:** {", ".join(anime.studios())}
**Tags:** {" ".join(["#"+tag.replace(" ","_").replace("-","_") for tag in anime.tags()])}
"""
    await callback_query.message.edit_media(types.InputMediaPhoto(anime.coverImage("extraLarge"), (msg1 + anime.description()[:(1019-len(msg1)-len(msg2))]+"...\n"+msg2 if len(msg1+anime.description()+msg2) > 1024 else msg1+anime.description()+msg2)))


@app.on_callback_query(filters.regex("MANGA"))
async def getManga(client, callback_query):
    args = callback_query.data.split(":")
    manga = Manga(args[1])
    msg1 = f"""
**Title:** {manga.title("romaji")}{f"({manga.title('english')})" if manga.title("english") else ""}
**Genres:** {", ".join(manga.genres())}
**Status:** {manga.status().replace("_"," ").lower().capitalize()}{f'''
**Volumes:** {manga.volumes()}
**Chapters:** {manga.chapters()}''' if manga.status()=="FINISHED" else ''}
**Ratings:** {manga.averageScore()}/100

**Characters:** {", ".join([ch["node"]["name"]["full"] for ch in manga.media[0]["characters"]["edges"]])}
**Description:**"""
    msg2 = f"""
**Tags:** {" ".join(["#"+tag.replace(" ","_").replace("-","_") for tag in manga.tags()])}
"""
    await callback_query.message.edit_media(types.InputMediaPhoto(manga.coverImage("extraLarge"), (msg1 + manga.description()[:(1019-len(msg1)-len(msg2))]+"...\n"+msg2 if len(msg1+manga.description()+msg2) > 1024 else msg1+manga.description()+msg2)))


@app.on_callback_query(filters.regex("CHR"))
async def getCharacter(client, callback_query):
    args = callback_query.data.split(":")
    character = Character(args[1])
    caption = f"""
**Name:** {character.name("full")}({character.name("native")})
**Description:**
{character.description()}
"""
    await callback_query.message.edit_media(types.InputMediaPhoto(character.image("large"), (caption[:1021]+"..." if len(caption) > 1024 else caption)))
