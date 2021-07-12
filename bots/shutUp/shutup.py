import DBManagement as DB
from common import (api_hash, api_id, bot_token, getFullName,
                    isModuleToggledFilter, lastfm_key, lastfm_pass,
                    lastfm_secret, lastfm_user, owner_id)
from pyrogram import Client, filters

app = Client(":memory:", api_id, api_hash, bot_token=bot_token)
