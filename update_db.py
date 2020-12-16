from threading import Thread
import time
from flask_sqlalchemy import SQLAlchemy
import callofduty
from callofduty import Mode, Platform, Title
import asyncio
from app import app


def update_loop():

    loop = asyncio.new_event_loop()
    answer = loop.run_until_complete(main("snowmanonfire99"))
    print(answer)

async def main(username):
    client = await callofduty.Login("jackmentch99@gmail.com", "Boeing1998")

    results = await client.SearchPlayers(Platform.Activision, username, limit=1)
    me = results[0]
    mw_profile = await me.profile(Title.ModernWarfare, Mode.Multiplayer)
    cw_profile = await me.profile(Title.BlackOpsColdWar, Mode.Multiplayer)

    if mw_profile["title"] != None:
        mw_kd = mw_profile["lifetime"]["all"]["properties"]["kdRatio"]
        wz_kd = mw_profile["lifetime"]["mode"]["br"]["properties"]["kdRatio"]
        wz_wins = mw_profile["lifetime"]["mode"]["br"]["properties"]["wins"]
    else:
        mw_kd = ""
        wz_kd = ""
        wz_wins = ""

    if cw_profile["title"] != None:
        cw_kd = cw_profile["lifetime"]["all"]["properties"]["kdratio"]
    else:
        cw_kd = ""

    return cw_kd, mw_kd, wz_kd, wz_wins


update_loop()