from pyrogram import idle

import bots.shutUp as SU
#import bots.userBot as UB
import common
import moduleHelps

SU.app.start()
#UB.usr.start()

SU.app.send_message(common.owner_id, "Starting")
print("Starting")

idle()

SU.app.send_message(common.owner_id, "Stopping")
print("Stopping")
#print(UB.usr.export_session_string())

SU.app.stop()
#UB.usr.stop()
