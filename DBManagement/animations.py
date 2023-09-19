from __future__ import annotations

from datetime import datetime
from typing import TypedDict

from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo.collection import Collection

from .db import database


class AnimationsType(TypedDict):
    animation_id: str
    insert_date: datetime


animationsCollection: Collection[AnimationsType] = database.animations


def add(animation_id: str) -> None:
    animationsCollection.update_one(
        filter={"animation_id": animation_id},
        update={"$setOnInsert": {"insert_date": datetime.utcnow()}},
        upsert=True,
    )


def get() -> list[AnimationsType]:
    return list(animationsCollection.find(sort=[("insert_date", ASCENDING)]))


def getLatest() -> AnimationsType:
    return animationsCollection.find(sort=[("insert_date", DESCENDING)])[0]
