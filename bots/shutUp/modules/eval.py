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

from common import bot_username, isModuleToggledFilter, owner_id

from ..shutup import app


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)


@app.on_message(filters.command(["eval", f"eval@{bot_username}"]) & isModuleToggledFilter("eval"))
async def evaluate(client, message, authorized=False):
    if (message.from_user.id == owner_id or authorized):
        status_message = await message.reply_text("`Running ...`")
        try:
            cmd = message.text.split(" ", maxsplit=1)[1]
        except IndexError:
            await status_message.delete()
            return
        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None
        try:
            await aexec(cmd, client, message)
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
        await message.reply_text(f"Not a SUDO user\n{(await app.get_users(owner_id)).mention}", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(f"Deny {emoji.CROSS_MARK}", "EVAL:DENY"), types.InlineKeyboardButton(f"Allow {emoji.CHECK_MARK_BUTTON}", "EVAL:ALLOW")]]))


@app.on_callback_query(filters.regex("^EVAL"))
async def authorizeEval(client, callback_query):
    if (callback_query.from_user.id == owner_id):
        if (callback_query.data == "EVAL:DENY"):
            await callback_query.message.edit_text("Denied")
        elif (callback_query.data == "EVAL:ALLOW"):
            await callback_query.message.edit_text("Allowed")
            await evaluate(client, callback_query.message.reply_to_message, True)
    else:
        await callback_query.answer("Only a SUDO user can authorize this")
