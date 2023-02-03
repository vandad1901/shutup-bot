from pyrogram.client import Client

from common import api_hash, api_id, bot_token

plugins = dict(root="bots.shutUp.modules")
app = Client("shutupbot", api_id=api_id, api_hash=api_hash,
             bot_token=bot_token, in_memory=True, plugins=plugins)
