
from pyrogram.client import Client

from common import api_hash, api_id, aux_user

# Comment this for USER_SESSION_STRING
usr = Client(aux_user, api_id=api_id, api_hash=api_hash)
# usr = Client(":memory:", api_id, api_hash) # Uncomment this for USER_SESSION_STRING
