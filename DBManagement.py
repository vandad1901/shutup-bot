from datetime import datetime
from typing import Optional, TypedDict

from pymongo import MongoClient

from common import database_url

client = MongoClient(database_url).shutup


class GroupsType(TypedDict):
    group_id: int
    shut: bool
    commands: dict
    filters: dict
    welcome: dict
    bye: dict


class UsersType(TypedDict):
    user_id: int
    lastfm: str


class AnimationsType(TypedDict):
    animation_id: str
    insert_date: datetime


class groups():
    @staticmethod
    def add(group_id: int):
        client.groups.update_one(filter={"group_id": group_id},
                                 update={"$setOnInsert":
                                 {"shut": False, "commands": {}, "filters": {}, "welcome": {}, "bye": {}}},
                                 upsert=True)

    @staticmethod
    def remove(group_id: int):
        client.groups.delete_one(filter={"group_id": group_id})

    @staticmethod
    def get(group_id: Optional[int] = None):
        if (not group_id):
            return list(client.groups.find())
        else:
            groups.add(group_id)
            return client.groups.find_one(filter={"group_id": group_id})

    @staticmethod
    def toggleShut(group_id):
        groups.add(group_id)
        client.groups.update_one(filter={"group_id": group_id},
                                 update={"$set": {"shut": {"$not": "$shut"}}})

    @staticmethod
    def toggleCommand(group_id, command):
        client.groups.update_one(filter={"group_id": group_id},
                                 update={"$set": {f"commands.{command}": {"$not": f"$commands.{command}"}}})

    @staticmethod
    def setWelcome(group_id, welcome):
        client.groups.update_one(filter={"group_id": group_id},
                                 update={"$set": {"welcome": dict(welcome)}})

    @staticmethod
    def setBye(group_id, bye):
        client.groups.update_one(filter={"group_id": group_id},
                                 update={"$set": {"bye": dict(bye)}})


class users():
    @staticmethod
    def add(user_id: int):
        client.users.update_one(filter={"user_id": user_id},
                                update={"$setOnInsert": {"lastfm": ""}},
                                upsert=True)

    @staticmethod
    def remove(users_id: int):
        client.users.delete_one({"user_id": users_id})

    @staticmethod
    def get(user_id: Optional[int] = None):
        if (not user_id):
            return list(client.animations.find())
        else:
            users.add(user_id)
            return client.users.find_one(filter={"user_id": user_id})

    @staticmethod
    def setLastfm(user_id: int, lastfm: str):
        client.users.update_one(filter={"user_id": user_id},
                                update={"$set": {"lastfm": lastfm}})


class animations():
    @staticmethod
    def add(animation_id: str):
        client.users.update_one(filter={"animation_id": animation_id},
                                update={"$setOnInsert": {
                                    "insert_date": datetime.utcnow()}},
                                upsert=True)

    @staticmethod
    def get():
        return list(client.animations.find())
