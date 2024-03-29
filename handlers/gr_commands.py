from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter


router = Router()
router.message.filter(
    ChatTypeFilter(chat_type=['group', 'supergroup']),
)


@router.message(Command(commands=['start']))
async def start(message: Message):
    await message.answer(f"Hello, {message.from_user.username}!")


@router.message(Command(commands=['id']))
async def start(message: Message):
    await message.answer(f"id группы - {message.chat.id}")


@router.message()
async def echo(message: Message):
    print(f"echo_gr {message.text}")
