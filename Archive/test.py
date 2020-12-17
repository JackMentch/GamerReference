import callofduty
from callofduty import Mode, Platform, Title
import asyncio

def get_data(username):
    try:
        client = asyncio.run(callofduty.Login("sample224433@gmail.com", "sample224433#"))
    except:
        print("Error Found")
        return 0, 0, 0, 0

    try:
        results = asyncio.run(client.SearchPlayers(Platform.Activision, username, limit=1))
    except:
        print("Error Found")
        return 0, 0, 0, 0


    if len(results) == 0:
        return 0, 0, 0, 0

    me = results[0]

    try:
        mw_profile = asyncio.run(me.profile(Title.ModernWarfare, Mode.Multiplayer))
    except:
        print("Error Found")
        return 0, 0, 0, 0

    try:
        cw_profile = asyncio.run(me.profile(Title.BlackOpsColdWar, Mode.Multiplayer))
    except:
        print("Error Found")
        return 0, 0, 0, 0


    if mw_profile["title"] != None:
        mw_kd = mw_profile["lifetime"]["all"]["properties"]["kdRatio"]
        wz_kd = mw_profile["lifetime"]["mode"]["br"]["properties"]["kdRatio"]
        wz_wins = mw_profile["lifetime"]["mode"]["br"]["properties"]["wins"]
    else:
        mw_kd = 0
        wz_kd = 0
        wz_wins = 0

    if cw_profile["title"] != None:
        cw_kd = cw_profile["lifetime"]["all"]["properties"]["kdratio"]
    else:
        cw_kd = 0

    return cw_kd, mw_kd, wz_kd, wz_wins


if __name__ == '__main__':
    print(get_data("daddy420#7046366"))