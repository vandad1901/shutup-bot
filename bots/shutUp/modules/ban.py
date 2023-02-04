"""
Banning and kicking module

Usage:
**/kick**
To kick a member (without banning). Reply to user or have their username or id as the argument
**/ban**
To ban a member. Reply to user or have their username or id as the argument.
Enter a multiple of **s, m, h, d or w**(e.g. 20m for 20 minutes) as the last argument to specify the amount of time the user will be banned for. The minimum is 30 seconds and the maximum is 366 days. If the time specified is not in this range they will be banned forever
**/unban**
To unban a member. Reply to user or have their username or id as the argument
"""
from datetime import datetime, timedelta

from pyrogram import errors, filters
from pyrogram.client import Client
from pyrogram.types import Message

from common import bot_username, getFullName, owner_id

timePeriods = {"s": "seconds", "m": "minutes",
               "h": "hours", "d": "days", "w": "weeks"}


@Client.on_message(filters.command(["kick", f"kick@{bot_username}"]))
async def kick(client: Client, message: Message):
    if (not (await message.chat.get_member("self")).privileges.can_restrict_members):
        await message.reply_text("I need additional permissions to kick users")
        return
    match message.reply_to_message is not None, len(message.command) > 1:
        case True, False:
            effectiveId = message.reply_to_message.from_user.id
        case False, True:
            effectiveId = message.command[1]
        case _:
            await message.reply_text("Ambiguous user specified. Reply to the user or have their id as the argument")
            return
    if (not ((await message.chat.get_member(message.from_user.id)).privileges.can_restrict_members or message.from_user.id == owner_id)):
        await message.reply_text("You must have user restricting permissions to use this command")
        return
    try:
        await message.chat.ban_member(effectiveId)
    except errors.exceptions.bad_request_400.UserAdminInvalid:
        await message.reply_text("This user is an admin")
        return
    await message.chat.unban_member(effectiveId)
    await message.reply_text(f"Kicked {getFullName(await client.get_users(effectiveId))}")


@Client.on_message(filters.command(["ban", f"ban@{bot_username}"]))
async def ban(client: Client, message: Message):
    if (not (await message.chat.get_member("self")).privileges .can_restrict_members):
        await message.reply_text("I need additional permissions to ban users")
        return
    match message.reply_to_message is not None, len(message.command) == 1:
        case True, False:
            effectiveId = message.reply_to_message.from_user.id
        case False, True:
            effectiveId = message.command[1]
        case _:
            await message.reply_text("No user specified. Reply to the user or have their id as the argument")
            return
    if (not ((await message.chat.get_member(message.from_user.id)).privileges.can_restrict_members or message.from_user.id == owner_id)):
        await message.reply_text("You must have user restricting permissions to use this command")
        return
    untilTime = datetime.now()
    try:
        durationStr = message.command[-1]
        untilTime += timedelta(**
                               {timePeriods[durationStr[-1]]: int(durationStr[:-1])})
        msg = f"Banned {getFullName(await client.get_users(effectiveId))} for {durationStr}"
    except (KeyError, ValueError):
        await message.reply_text("Invalid time duration")
        return
    except IndexError:
        msg = f"Banned {getFullName(await client.get_users(effectiveId))} forever"
    try:
        await message.chat.ban_member(effectiveId, untilTime)
    except errors.exceptions.bad_request_400.UserAdminInvalid:
        await message.reply_text("This user is an admin")
        return
    await message.reply_text(msg)


@Client.on_message(filters.command(["unban", f"unban@{bot_username}"]))
async def unban(client: Client, message: Message):
    if (not (await message.chat.get_member("self")).privileges.can_restrict_members):
        await message.reply_text("I need additional permissions to unban users")
        return
    match message.reply_to_message is not None, len(message.command) == 1:
        case True, False:
            effectiveId = message.reply_to_message.from_user.id
        case False, True:
            effectiveId = message.command[1]
        case _:
            await message.reply_text("No user specified. Reply to the user or have their id as the argument")
            return
    if (not ((await message.chat.get_member(message.from_user.id)).privileges.can_restrict_members or message.from_user.id == owner_id)):
        await message.reply_text("You must have user restricting permissions to use this command")
        return
    await message.chat.unban_member(effectiveId)
    await message.reply_text(f"Unbanned {getFullName(await client.get_users(effectiveId))}")
