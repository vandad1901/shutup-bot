"""
Banning and kicking module

Usage:
**/kick**
To kick a member (without banning). Reply to user or have their username or id as the argument
**/ban**
To ban a member. Reply to user or have their username or id as the argument
**/unban**
To unban a member. Reply to user or have their username or id as the argument
"""
import pyrogram
from pyrogram import errors, filters

from ..shutup import app, getFullName, owner_id


@app.on_message(filters.command(["kick", "kick@damnshutup_bot"]))
def kick(client, message):
    if(not message.chat.get_member("self").can_restrict_members):
        message.reply_text("I need additional permissions to restrict users")
        return
    if(len(message.command) > 1):
        effectiveId = message.command[1]
    elif(message.reply_to_message):
        effectiveId = message.reply_to_message.from_user.id
    else:
        message.reply_text(
            "No user specified. Reply to the user or have their id as the argument")
        return
    if(message.chat.get_member(message.from_user.id).can_restrict_members or message.from_user.id == owner_id):
        try:
            message.chat.kick_member(effectiveId)
        except errors.exceptions.bad_request_400.UserAdminInvalid:
            message.reply_text("This user is an admin")
            return
        message.chat.unban_member(effectiveId)
        message.reply_text(
            f"Kicked {getFullName(app.get_users(effectiveId))}")
    else:
        message.reply_text(
            "You must have user restricting permissions to use this command")


@app.on_message(filters.command(["ban", "ban@damnshutup_bot"]))
def kick(client, message):
    if(not message.chat.get_member("self").can_restrict_members):
        message.reply_text("I need additional permissions to restrict users")
        return
    if(len(message.command) > 1):
        effectiveId = message.command[1]
    elif(message.reply_to_message):
        effectiveId = message.reply_to_message.from_user.id
    else:
        message.reply_text(
            "No user specified. Reply to the user or have their id as the argument")
        return
    if(message.chat.get_member(message.from_user.id).can_restrict_members or message.from_user.id == owner_id):
        try:
            message.chat.kick_member(effectiveId)
        except errors.exceptions.bad_request_400.UserAdminInvalid:
            message.reply_text("This user is an admin")
            return
        message.reply_text(
            f"Banned {getFullName(app.get_users(effectiveId))}")
    else:
        message.reply_text(
            "You must have user restricting permissions to use this command")


@app.on_message(filters.command(["unban", "unban@damnshutup_bot"]))
def kick(client, message):
    if(not message.chat.get_member("self").can_restrict_members):
        message.reply_text("I need additional permissions to restrict users")
        return
    if(len(message.command) > 1):
        effectiveId = message.command[1]
    elif(message.reply_to_message):
        effectiveId = message.reply_to_message.from_user.id
    else:
        message.reply_text(
            "No user specified. Reply to the user or have their id as the argument")
        return
    if(message.chat.get_member(message.from_user.id).can_restrict_members or message.from_user.id == owner_id):
        message.chat.unban_member(effectiveId)
        message.reply_text(
            f"Unbanned {getFullName(app.get_users(effectiveId))}")
    else:
        message.reply_text(
            "You must have user restricting permissions to use this command")
