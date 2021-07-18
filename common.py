from itertools import repeat
from os import environ
from urllib.parse import urljoin, urlparse

import dotenv
from pyrogram import filters

import DBManagement as DB

dotenv.load_dotenv()
api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["BOT_TOKEN"]
bot_username = environ["BOT_USERNAME"]
owner_id = int(environ["OWNER_ID"])

database_url = environ["DATABASE_URL"]
database_url = urlparse(database_url)._replace(scheme="postgresql").geturl()

lastfm_key = environ["LASTFM_KEY"]
lastfm_secret = environ["LASTFM_SECRET"]
lastfm_user = environ["LASTFM_USER"]
lastfm_pass = environ["LASTFM_PASS"]

aux_user = environ["USER_SESSION_STRING"]


def isModuleToggled(chatId, moduleName):
    toggles = DB.groups.get(chatId).commands
    try:
        return toggles[moduleName]
    except (KeyError, TypeError):
        return True


def isModuleToggledFilter(moduleName):
    def func(flt, _, query):
        return isModuleToggled(query.chat.id, flt.moduleName)
    return filters.create(func, moduleName=moduleName)


def makeButtons(buttons, buttonTable):
    if(isinstance(buttonTable, int)):
        buttonTable = list(repeat(buttonTable, len(buttons)//buttonTable+1))
    buttons = iter(buttons)
    Table = []
    try:
        for i in range(len(buttonTable)):
            Table.append([])
            for _ in range(buttonTable[i]):
                Table[i].append(next(buttons))
        return Table
    except StopIteration:
        if(Table[-1] == []):
            Table.pop()
        return Table


def getFullName(user):
    return " ".join([user.first_name if user.first_name else "", user.last_name if user.last_name else ""])
