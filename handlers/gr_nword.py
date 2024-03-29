from aiogram import Router, Bot
from aiogram.types import Message

from filters.chat_type import ChatTypeFilter
from filters.isnword import IsNWord
from filters.isurl import IsUrl

from data import get_data
from data import db_update

from funcs import mute_unmute


router = Router()
router.message.filter(
    ChatTypeFilter(chat_type=['group', 'supergroup']),
)


@router.message(IsNWord()) # or
@router.message(IsUrl()) # or
async def check_for_n_word(message: Message, bot: Bot):
    db = await get_data.get_bans(message.from_user.id)
    print(db)
    if db is None:
        await db_update.insert_bans(id=message.from_user.id, username=message.from_user.username, warn=1)
        await message.delete()
        return await message.answer("warning = 1")

    if db[2] >= 4: # 4 - кол-во предупреждений для мута
        await db_update.update_bans_by_id(id=message.from_user.id, username=message.from_user.username, warn=3,
                                          ban=True)
        await message.delete()
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
        await message.answer(f"ban user: {message.from_user.username}\n"
                             f"reason: banwords xyuarit")

    elif db[2] >= 2: # 2 - кол-во предупреждений для мута (изменить и в мут анмут тоже)
        await mute_unmute.func_group_mute(message, bot, db=db)

    else:
        await db_update.update_bans_by_id(id=message.from_user.id, username=message.from_user.username, warn=db[2]+1)
        await message.delete()
        await message.answer(f"warning = {db[2]+1}")



