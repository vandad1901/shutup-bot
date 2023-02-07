from typing import TypedDict

from pymongo.collection import Collection

from .db import database


class UsersType(TypedDict):
    user_id: int
    lastfm: str


usersCollection: Collection[UsersType] = database.users


def add(user_id: int) -> None:
    usersCollection.update_one(filter={"user_id": user_id},
                               update={"$setOnInsert": {"lastfm": ""}},
                               upsert=True)


def remove(users_id: int) -> None:
    usersCollection.delete_one({"user_id": users_id})


def get(user_id: int) -> UsersType:
    add(user_id)
    r = usersCollection.find_one(filter={"user_id": user_id})
    assert (r is not None)
    return r


def get_all() -> list[UsersType]:
    return list(usersCollection.find())


def setLastfm(user_id: int, lastfm: str) -> None:
    usersCollection.update_one(filter={"user_id": user_id},
                               update={"$set": {"lastfm": lastfm}})
