from aiogram import Bot
from aiogram.types import ChatPermissions, Message

from time import time

from data import db_update


# ------------------------ mutes ------------------------
async def func_adm_mute(message: Message, bot: Bot, args, db):
    perm = ChatPermissions(
        can_send_messages=True
    )
    await bot.restrict_chat_member(chat_id=args[0], user_id=db[0], permissions=perm,
                                   until_date=int(time()) + int(args[2]))
    await message.answer(f"Юзер <b>{args[1]}</b> был успешно замучен на <b>{args[2]}</b> часа")


async def func_adm_unmute(message: Message, bot: Bot, args, db):
    perm = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_manage_topics=True
    )
    await bot.restrict_chat_member(chat_id=args[0], user_id=db[0], permissions=perm, until_date=int(time()) + 10)
    await message.answer(f"Юзер <b>{args[1]}</b> был успешно размучен")
    await bot.send_message(chat_id=args[0], text=f"Юзер <b>{args[1]}</b> был размучен")


async def func_group_mute(message, bot, args, db):
    perm = ChatPermissions(
        can_send_messages=False
    )
    await db_update.update_bans_by_id(id=message.from_user.id, username=message.from_user.username, warn=db[2] + 1)
    await message.delete()
    await bot.restrict_chat_member(chat_id=args[0], user_id=db[0], permissions=perm,
                                   until_date=int(time()) + (3600 * (db[2] - 1))) # сначала мут на час, потом на 2
    await message.answer(f"mute user {args[1]} for {db[2] - 1}\n"
                         f"reason: banwords xyarit")
    await bot.send_message(chat_id=args[0], text=f"Юзер <b>{args[1]}</b> был замучен на {db[2]-1}")
