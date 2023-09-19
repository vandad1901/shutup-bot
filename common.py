from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from collections.abc import Callable
from collections.abc import Iterator
from functools import partial
from functools import wraps
from itertools import repeat
from math import ceil
from os import environ
from typing import Any
from typing import TypeVar

import dotenv
from pyrogram import filters
from pyrogram.filters import Filter
from pyrogram.types import Chat
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


T = TypeVar("T")


def partitionGenerator(
    items: list[T],
    partitionTable: int | list[int],
) -> Iterator[list[T]]:
    if isinstance(partitionTable, int):
        partitionTable = list(repeat(partitionTable, ceil(len(items) / partitionTable)))
    for i in range(len(partitionTable)):
        beginning = sum(partitionTable[:i])
        yield items[beginning : beginning + partitionTable[i]]


def partition(items: list[T], partitionTable: int | list[int]) -> list[list[T]]:
    return list(partitionGenerator(items, partitionTable))


def getFullName(user: User | Chat) -> str:
    return f"{user.first_name} {user.last_name if user.last_name is not None else ''}".strip()


def ordinal(n: int) -> str:
    return f"{n}{'tsnrhtdd'[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4]}"
