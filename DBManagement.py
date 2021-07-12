import os
from enum import unique
from typing import Type

from pyrogram.session.internals import data_center
from sqlalchemy import JSON as js
from sqlalchemy import (BigInteger, Boolean, Column, Integer, MetaData, String,
                        Table, create_engine)
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import PickleType

from common import database_url

engine = create_engine(database_url, echo=False)

meta = MetaData()
groupsTable = Table(
    "groups", meta,
    Column("id", Integer, primary_key=True),
    Column("groupid", BigInteger, unique=True),
    Column("shut", Boolean, unique=False, default=False),
    Column("commands", js, unique=False, default={}),
    Column("filters", js, unique=False, default={}),
    Column("welcome", PickleType, unique=False),
    Column("bye", PickleType, unique=False),
    Column("addbacks", js, unique=False, default={}))
usersTable = Table(
    "users", meta,
    Column("id", Integer, primary_key=True),
    Column("userid", BigInteger, unique=True),
    Column("lastfm", String, unique=False))
animationsTable = Table(
    "animations", meta,
    Column("id", Integer, primary_key=True),
    Column("animationid", String, unique=True))

meta.create_all(engine)


class groups():
    @staticmethod
    def add(group_id):
        try:
            with engine.connect() as conn:
                if(not conn.execute(groupsTable.select(None).where(groupsTable.c.groupid == group_id)).fetchone()):
                    return conn.execute(groupsTable.insert(None).values(groupid=group_id))
                else:
                    return False
        except Exception as E:
            print(E)
            return False

    @staticmethod
    def remove(group_id):
        try:
            with engine.connect() as conn:
                conn.execute(groupsTable.delete(None).where(
                    groupsTable.c.groupid == group_id))
                return True
        except Exception as error:
            return error

    @staticmethod
    def get(group_id=None):
        with engine.connect() as conn:
            if(not group_id):
                return(conn.execute(groupsTable.select(None)).fetchall())
            else:
                groups.add(group_id)
                return(conn.execute(groupsTable.select(None).where(
                    groupsTable.c.groupid == group_id)).fetchone())

    @staticmethod
    def toggleShut(group_id):
        try:
            with engine.connect() as conn:
                groups.add(group_id)
                value = conn.execute(groupsTable.select(None).where(
                    groupsTable.c.groupid == group_id), echo=False).fetchone().shut
                return(conn.execute(groupsTable.update(None).where(
                    groupsTable.c.groupid == group_id).values(shut=(not value))))
        except Exception as E:
            print(E)
            return False

    @staticmethod
    def toggleCommand(group_id, command):
        try:
            with engine.connect() as conn:
                groups.add(group_id)
                value = conn.execute(groupsTable.select(None).where(
                    groupsTable.c.groupid == group_id), echo=False).fetchone().commands
                try:
                    value[command] = not value[command]
                except (TypeError, KeyError):
                    value[command] = False
                return(conn.execute(groupsTable.update(None).where(
                    groupsTable.c.groupid == group_id).values(commands=value)))
        except Exception as E:
            print(E)
            return False

    @staticmethod
    def setWelcome(group_id, welcome):
        try:
            with engine.connect() as conn:
                groups.add(group_id)
                return(conn.execute(groupsTable.update(None).where(
                    groupsTable.c.groupid == group_id).values(welcome=welcome)))
        except Exception as E:
            print(E)
            return False

    @staticmethod
    def setBye(group_id, bye):
        try:
            with engine.connect() as conn:
                groups.add(group_id)
                return(conn.execute(groupsTable.update(None).where(
                    groupsTable.c.groupid == group_id).values(bye=bye)))
        except Exception as E:
            print(E)
            return False

    @staticmethod
    def toggleAddback(group_id, user_id):
        user_id = str(user_id)
        try:
            with engine.connect() as conn:
                groups.add(group_id)
                value = conn.execute(groupsTable.select(None).where(
                    groupsTable.c.groupid == group_id)).fetchone().addbacks
                value[user_id] = not value.get(user_id)
                return(conn.execute(groupsTable.update(None).where(
                    groupsTable.c.groupid == group_id).values(addbacks=value)))
        except Exception as E:
            print(E)
            return False


class users():
    def add(user_id):
        try:
            with engine.connect() as conn:
                if(not conn.execute(usersTable.select(None).where(usersTable.c.userid == user_id)).fetchone()):
                    return conn.execute(usersTable.insert(None).values(userid=user_id))
                else:
                    return False
        except Exception as E:
            print(E)
            return False

    def remove(users_id):
        try:
            with engine.connect() as conn:
                return conn.execute(usersTable.delete(None).where(
                    usersTable.c.userid == users_id))
        except Exception as error:
            return error

    def get(user_id=None):
        with engine.connect() as conn:
            if(not user_id):
                return(conn.execute(usersTable.select(None)).fetchall())
            else:
                users.add(user_id)
                return(conn.execute(usersTable.select(None).where(
                    usersTable.c.userid == user_id)).fetchone())

    def setLastfm(user_id, lastfm):
        try:
            with engine.connect() as conn:
                users.add(user_id)
                return(conn.execute(usersTable.update(None).where(
                    usersTable.c.userid == user_id).values(lastfm=lastfm)))
        except Exception as E:
            print(E)
            return False


class animations():
    @staticmethod
    def add(animation_id):
        try:
            with engine.connect() as conn:
                if(not conn.execute(animationsTable.select(None).where(animationsTable.c.animationid == animation_id)).fetchone()):
                    return conn.execute(animationsTable.insert(None).values(animationid=animation_id))
                else:
                    return False
        except:
            return False

    @staticmethod
    def get():
        with engine.connect() as conn:
            return(conn.execute(animationsTable.select(None)).fetchall())


def resetDB():
    with engine.connect() as conn:
        meta.drop_all(engine)
        animations.add("CgADBAADEgcAAqNhEVIQydI7mWvdvBYE")


if __name__ == "__main__":
    if(int(input("reset? 1/0"))):
        resetDB()
