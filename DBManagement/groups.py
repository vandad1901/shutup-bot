from typing import TypedDict

from pymongo.collection import Collection
from pyrogram.types import Message

from .db import database


class GroupsType(TypedDict):
    group_id: int
    shut: bool
    commands: dict
    filters: dict
    welcome: str
    bye: str


groupsCollection: Collection[GroupsType] = database.groups


def add(group_id: int) -> None:
    groupsCollection.update_one(filter={"group_id": group_id},
                                update={"$setOnInsert":
                                        {"shut": False, "commands": {}, "filters": {}, "welcome": "", "bye": ""}},
                                upsert=True)


def remove(group_id: int) -> None:
    groupsCollection.delete_one(filter={"group_id": group_id})


def get(group_id: int) -> GroupsType:
    add(group_id)
    r = groupsCollection.find_one(filter={"user_id": group_id})
    assert (r is not None)
    return r


def get_all() -> list[GroupsType]:
    return list(groupsCollection.find())


def toggleShut(group_id: int) -> None:
    add(group_id)
    groupsCollection.update_one(filter={"group_id": group_id},
                                update=[{"$set": {"shut": {"$not": "$shut"}}}])


def toggleCommand(group_id: int, command: str) -> None:
    groupsCollection.update_one(filter={"group_id": group_id},
                                update=[{"$set": {f"commands.{command}": {"$not": {"$ifNull": [f"commands.{command}", True]}}}}])


def setWelcome(group_id: int, welcome: Message) -> None:
    groupsCollection.update_one(filter={"group_id": group_id},
                                update={"$set": {"welcome": repr(welcome)}})


def setBye(group_id: int, bye: Message) -> None:
    database.groups.update_one(filter={"group_id": group_id},
                               update={"$set": {"bye": repr(bye)}})
