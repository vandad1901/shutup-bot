import DBManagement as DB
from common import (api_hash, api_id, aux_user, bot_username,
                    isModuleToggledFilter)
from pyrogram import Client

from ..shutUp import app

usr = Client(aux_user, api_id=api_id, api_hash=api_hash) # Comment this for USER_SESSION_STRING
#usr = Client(":memory:", api_id, api_hash) # Uncomment this for USER_SESSION_STRING
