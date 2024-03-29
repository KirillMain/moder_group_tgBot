import aiosqlite as sq


async def db_start():
    db = await sq.connect("data/tg.db")

    await db.execute('CREATE TABLE IF NOT EXISTS bans('
                     'id INTEGER,'
                     'username TEXT,'
                     'warning INTEGER,'
                     'ban BOOLEAN NOT NULL)')
    await db.execute('CREATE TABLE IF NOT EXISTS nwords('
                     'word TEXT)')

    # await db.execute('INSERT INTO bans (id, warning, ban) VALUES (?, ?, ?)',
    #            (1124, 5, 10))

    await db.commit()
    await db.close()