from datetime import datetime
from typing import Optional, TypedDict

from pymongo import MongoClient

from common import database_url

client = MongoClient(database_url).shutup


class Groups(TypedDict):
    groupid: int
    shut: bool
    commands: dict
    filters: dict
    welcome: dict
    bye: dict


class Users(TypedDict):
    userid: int
    lastfm: str


class Animations(TypedDict):
    animationid: str


class groups():
    @staticmethod
    def add(group_id: int):
        client.groups.update_one(filters={"groupid": group_id},
                                 update={"$setOnInsert": {
                                     "shut": False, "commands": {}, "filters": {}, "welcome": {}, "bye": {}}},
                                 upsert=True)

    @staticmethod
    def remove(group_id: int):
        client.groups.delete_one(filters={"groupid": group_id})

    @staticmethod
    def get(group_id: Optional[int] = None):
        if (not group_id):
            return list(client.groups.find())
        else:
            groups.add(group_id)
            return client.groups.find_one(filters={"groupid": group_id})

    @staticmethod
    def toggleShut(group_id):
        groups.add(group_id)
        client.groups.update(filters={"groupid": group_id},
                             update={
                             "$set": {"shut": {"$not": "$shut"}}})

    @staticmethod
    def toggleCommand(group_id, command):
        client.groups.update(filters={"groupid": group_id},
                             update={"$set": {f"commands.{command}": {"$not": f"$commands.{command}"}}})

    @staticmethod
    def setWelcome(group_id, welcome):
        client.groups.update(filters={"groupid": group_id},
                             update={"$set": {"welcome": dict(welcome)}})

    @staticmethod
    def setBye(group_id, bye):
        client.groups.update(filters={"groupid": group_id},
                             update={"$set": {"bye": dict(bye)}})


class users():
    def add(user_id: int):
        try:
            client.users.insert_one(Users(userid=user_id, lastfm=None))
        except Exception as E:
            print(E)
            return False

    def remove(users_id: int):
        try:
            client.users.delete_one({"userid": users_id})
        except Exception as E:
            print(E)
            return False

    def get(user_id: Optional[int] = None):
        if (not user_id):
            return list(client.animations.find())
        else:
            users.add(user_id)
            return client.users.find_one({"userid": user_id})

    def setLastfm(user_id, lastfm):
        try:
            client.users.update_one({"userid": user_id}, {
                                    "$set": {"lastfm": lastfm}})
        except Exception as E:
            print(E)
            return False


class animations():
    @staticmethod
    def add(animation_id: str):
        try:
            print("test")
            client.animations.insert_one(
                {"insert_date": datetime.datetime.utcnow(), "animationid": animation_id})
            print("test222222")
        except:
            return False

    @staticmethod
    def get():
        return list(client.animations.find())
