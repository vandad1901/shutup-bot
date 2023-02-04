import asyncio
from functools import partial, wraps
from itertools import repeat
from math import ceil
from os import environ
from typing import Iterator, Union, Callable, Awaitable, Any

import dotenv
from pyrogram import filters
from pyrogram.filters import Filter
from pyrogram.types import User

import DBManagement as DB

dotenv.load_dotenv()
api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ["BOT_TOKEN"]
bot_username = environ["BOT_USERNAME"]
owner_id = int(environ["OWNER_ID"])
# aux_user = environ["USER_SESSION_STRING"]
aux_user = ""

database_url = environ["DATABASE_URL"]

lastfm_key = environ["LASTFM_KEY"]
lastfm_secret = environ["LASTFM_SECRET"]
lastfm_user = environ["LASTFM_USER"]
lastfm_pass = environ["LASTFM_PASS"]


def async_wrap(func) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


def isModuleToggled(chatId: int, moduleName: str) -> bool:
    toggles = DB.groups.get(chatId)["commands"]
    try:
        return toggles.get(moduleName, True)
    except (KeyError, TypeError):
        return True


def isModuleToggledFilter(moduleName: str) -> Filter:
    def func(flt, _, query):
        return isModuleToggled(query.chat.id, flt.moduleName)
    return filters.create(func, moduleName=moduleName)


def partitionGenerator(items: list[Any], partitonTable: Union[int, list[int]]) -> Iterator[list[Any]]:
    if (isinstance(partitonTable, int)):
        partitonTable = list(
            repeat(partitonTable, ceil(len(items)/partitonTable)))
    for i in range(len(partitonTable)):
        beginning = sum(partitonTable[:i])
        yield items[beginning:beginning+partitonTable[i]]


def partition(items: list[Any], partitonTable: Union[int, list[int]]) -> list[Any]:
    return list(partitionGenerator(items, partitonTable))


def getFullName(user: User) -> str:
    return f"{user.first_name} {user.last_name if user.last_name is not None else ''}".strip()


def ordinal(n: int) -> str:
    return f"{n}{'tsnrhtdd'[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4]}"
