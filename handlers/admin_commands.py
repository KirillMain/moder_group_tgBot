from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from filters.chat_type import ChatTypeFilter
from filters.isadmin import IsAdmin

from data import get_data
from data import db_update

from config_reader import config

from funcs import mute_unmute


router = Router()
router.message.filter(
    ~ChatTypeFilter(['group', 'supergroup']),
    IsAdmin(config.admin_ids),
)


@router.message(Command(commands=['help']))
async def adm_unban(message: Message, command: CommandObject):
    await message.answer(f"<b>Доступны следующие комманды:</b>\n\n"
                         f"/unban chat_id username - разбан юзера\n"
                         f"/mute chat_id username n (в часах) - мут юзера на \"n\" часов\n"
                         f"/unmute chat_id username - размут юзера\n"
                         f"/add_nwords nword1 nword2 (можно и одно слово оставить) - "
                         f"добавление слова или слов в список запрещенных\n"
                         f"/remove_nwords nword1 nword2 (можно и одно слово оставить) - "
                         f"удаление слова или слов из списка запрещенных\n\n"
                         f"Например: /add_nwords дверь памперс")


# -------------------- bans --------------------
@router.message(Command(commands=['unban'])) # chat_id + " " + username
async def adm_unban(message: Message, command: CommandObject, bot: Bot):
    if command.args is None:
        return await message.answer("Ошибка: не переданы аргументы")

    args = command.args.split(" ")
    db = await get_data.get_bans_by_username(args[1])
    if db is None:
        await message.answer("Ошибка: такого пользователя нет")
        return
    else:
        await bot.unban_chat_member(chat_id=args[0], user_id=db[0])
        await db_update.update_bans_by_id(id=db[0], username=args[1], warn=0, ban=False)
        await message.answer(f"Юзер <b>{args[1]}</b> был успешно разбанен")


# -------------------- mutes --------------------
@router.message(Command(commands=['mute'])) # chat_id + " " + username + " " + date (в часах)
async def adm_mute(message: Message, command: CommandObject, bot: Bot):
    if command.args is None:
        return await message.answer("Ошибка: не переданы аргументы")

    args = command.args.split(" ")
    try:
        int(args[0])
        int(args[2])
    except ValueError:
        return await message.answer("Данные введены неправильно")

    db = await get_data.get_bans_by_username(args[1])
    if db is None:
        return await message.answer("Ошибка: такого пользователя нет")
    else:
        await mute_unmute.func_adm_mute(message, bot, args, db)


@router.message(Command(commands=['unmute'])) # chat_id + " " + username
async def adm_unmute(message: Message, command: CommandObject, bot: Bot):
    if command.args is None:
        return await message.answer("Ошибка: не переданы аргументы")

    args = command.args.split(" ")
    try:
        int(args[0])
    except ValueError:
        return await message.answer("Данные введены неправильно")

    db = await get_data.get_bans_by_username(args[1])
    if db is None:
        return await message.answer("Ошибка: такого пользователя нет")
    else:
        await mute_unmute.func_adm_unmute(message, bot, args, db)


# -------------------- nword --------------------
@router.message(Command(commands=['add_nwords']))
async def adm_add_nword(message: Message, command: CommandObject): # nword + " " + nword + ...
    if command.args is None:
        return await message.answer("Ошибка: не переданы аргументы")

    if command.args.find(" ") == -1:
        await db_update.insert_nword(command.args.lower())

    else:
        for el in command.args.split(' '):
            await db_update.insert_nword(el.lower())
    await message.answer(f"Банворды были успешно добавлены")


@router.message(Command(commands=['remove_nwords']))
async def adm_add_nword(message: Message, command: CommandObject): # nword + " " + nword + ...
    if command.args is None:
        return await message.answer("Ошибка: не переданы аргументы")

    if command.args.find(" ") == -1:
        await db_update.remove_nword(command.args.lower())

    else:
        for el in command.args.split(' '):
            await db_update.remove_nword(el.lower())
    await message.answer(f"Банворды были успешно добавлены")