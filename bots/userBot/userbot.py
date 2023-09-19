from __future__ import annotations

from pyrogram.client import Client

from common import api_hash
from common import api_id
from common import aux_user

# Comment this for USER_SESSION_STRING
usr = Client(aux_user, api_id=api_id, api_hash=api_hash)
# usr = Client(":memory:", api_id, api_hash) # Uncomment this for USER_SESSION_STRING
