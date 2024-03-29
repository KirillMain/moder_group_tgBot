import aiosqlite as sq


async def get_nwords():
    db = await sq.connect("data/tg.db")

    cur = await db.execute("SELECT word FROM nwords")
    res = await cur.fetchall()

    await cur.close()
    await db.close()

    return res


async def get_bans(user_id: int):
    db = await  sq.connect("data/tg.db")

    cur = await  db.execute("SELECT username, warning, ban FROM bans WHERE id == {idd}".format(idd=user_id))
    res = await cur.fetchone()

    await cur.close()
    await db.close()

    return res


async def get_bans_by_username(u_name: str):
    db = await  sq.connect("data/tg.db")

    cur = await  db.execute("SELECT id, warning, ban FROM bans WHERE username == '{uname}'".format(uname=u_name))
    res = await cur.fetchone()

    await cur.close()
    await db.close()

    return res