from datetime import datetime
from typing import Any, Optional, TypedDict

from pymongo import ASCENDING, DESCENDING, MongoClient
from pyrogram.types import Message

from common import database_url

database = MongoClient(database_url).shutup


class GroupsType(TypedDict):
    group_id: int
    shut: bool
    commands: dict
    filters: dict
    welcome: str
    bye: str


class UsersType(TypedDict):
    user_id: int
    lastfm: str


class AnimationsType(TypedDict):
    animation_id: str
    insert_date: datetime


class groups():
    @staticmethod
    def add(group_id: int) -> None:
        database.groups.update_one(filter={"group_id": group_id},
                                   update={"$setOnInsert":
                                           {"shut": False, "commands": {}, "filters": {}, "welcome": "", "bye": ""}},
                                   upsert=True)

    @staticmethod
    def remove(group_id: int) -> None:
        database.groups.delete_one(filter={"group_id": group_id})

    @staticmethod
    def get(group_id: Optional[int] = None) -> list[Any] | Any:
        if (not group_id):
            return list(database.groups.find())
        else:
            groups.add(group_id)
            return database.groups.find_one(filter={"group_id": group_id})

    @staticmethod
    def toggleShut(group_id: int) -> None:
        groups.add(group_id)
        database.groups.update_one(filter={"group_id": group_id},
                                   update=[{"$set": {"shut": {"$not": "$shut"}}}])

    @staticmethod
    def toggleCommand(group_id: int, command: str) -> None:
        database.groups.update_one(filter={"group_id": group_id},
                                   update=[{"$set": {f"commands.{command}": {"$not": {"$ifNull": [f"commands.{command}", True]}}}}])

    @staticmethod
    def setWelcome(group_id: int, welcome: Message) -> None:
        database.groups.update_one(filter={"group_id": group_id},
                                   update={"$set": {"welcome": repr(welcome)}})

    @staticmethod
    def setBye(group_id: int, bye: Message) -> None:
        database.groups.update_one(filter={"group_id": group_id},
                                   update={"$set": {"bye": repr(bye)}})


class users():
    @staticmethod
    def add(user_id: int) -> None:
        database.users.update_one(filter={"user_id": user_id},
                                  update={"$setOnInsert": {"lastfm": ""}},
                                  upsert=True)

    @staticmethod
    def remove(users_id: int) -> None:
        database.users.delete_one({"user_id": users_id})

    @staticmethod
    def get(user_id: Optional[int] = None) -> list[Any] | Any:
        if (not user_id):
            return list(database.animations.find())
        else:
            users.add(user_id)
            return database.users.find_one(filter={"user_id": user_id})

    @staticmethod
    def setLastfm(user_id: int, lastfm: str) -> None:
        database.users.update_one(filter={"user_id": user_id},
                                  update={"$set": {"lastfm": lastfm}})


class animations():
    @staticmethod
    def add(animation_id: str) -> None:
        database.animations.update_one(filter={"animation_id": animation_id},
                                       update={"$setOnInsert": {
                                           "insert_date": datetime.utcnow()}},
                                       upsert=True)

    @staticmethod
    def get() -> list[dict]:
        return list(database.animations.find(sort=[('insert_date', ASCENDING)]))

    @staticmethod
    def getLatest() -> dict:
        return database.animations.find(sort=[('insert_date', DESCENDING)])[0]
