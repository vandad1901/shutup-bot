"""
Evaluate a python program with permission from a sudo user

Usage:
**/eval** program
"""
import os
import sys
import traceback
from io import StringIO

from pyrogram import emoji, filters, types
from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message, User

from common import bot_username, isModuleToggledFilter, owner_id


async def asyncExecute(code: str, client: Client, message: Message):
    exec(
        f'async def __asyncExecute(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__asyncExecute'](client, message)


@Client.on_message(filters.command(["eval", f"eval@{bot_username}"]) & isModuleToggledFilter("eval"))
async def evaluate(client: Client, message: Message, authorized: bool = False):
    if (message.from_user.id == owner_id or authorized):
        status_message = await message.reply_text("`Running ...`")
        try:
            cmd = message.text.split(" ", maxsplit=1)[1]
        except IndexError:
            await status_message.delete()
            return
        reply_to_id = message.id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.id
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None
        try:
            await asyncExecute(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"
        final_output = f"<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>"
        if len(final_output) > 4096:
            filename = 'output.txt'
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(final_output))
            await message.reply_document(
                document=filename,
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id
            )
            os.remove(filename)
            await status_message.delete()
        else:
            await status_message.edit(final_output)
    else:
        user = await client.get_users(owner_id)
        assert (isinstance(user, User))
        await message.reply_text(f"Not a SUDO user\n{user.mention}", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(f"Deny {emoji.CROSS_MARK}", "EVAL:DENY"), types.InlineKeyboardButton(f"Allow {emoji.CHECK_MARK_BUTTON}", "EVAL:ALLOW")]]))


@Client.on_callback_query(filters.regex("^EVAL"))
async def authorizeEval(client: Client, callback_query: CallbackQuery):
    assert (isinstance(callback_query.data, str))
    if (callback_query.from_user.id == owner_id):
        if (callback_query.data == "EVAL:DENY"):
            await callback_query.message.edit_text("Denied")
        elif (callback_query.data == "EVAL:ALLOW"):
            await callback_query.message.edit_text("Allowed")
            await evaluate(client, callback_query.message.reply_to_message, True)
    else:
        await callback_query.answer("Only a SUDO user can authorize this")
