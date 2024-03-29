import aiosqlite as sq

from typing import List


async def insert_bans(id: int, username: str, warn: int, ban: bool=False):
    db = await sq.connect("data/tg.db")

    await db.execute("INSERT INTO bans (id, username, warning, ban) VALUES (?, ?, ?, ?)",
                     (id, username, warn, ban))

    await db.commit()
    await db.close()


async def update_bans_by_id(id: int, username: str, warn: int, ban: bool=False):
    db = await sq.connect("data/tg.db")

    await db.execute('UPDATE bans SET username = ?, warning = ?, ban = ? WHERE id = ?',
                      (username, warn, ban, id))

    await db.commit()
    await db.close()


async def insert_nword(nword: str):
    db = await sq.connect("data/tg.db")

    await db.execute("INSERT INTO nwords (word) VALUES (?)",
                     (nword,))

    await db.commit()
    await db.close()


async  def remove_nword(nword: str):
    db = await sq.connect("data/tg.db")

    await db.execute("DELETE FROM nwords WHERE word={nw}".format(nw=nword))

    await db.commit()
    await db.close()