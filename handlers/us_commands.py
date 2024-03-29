from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command(commands=['start']))
async def start_not_in_chat(message: Message):
    await message.answer(f"Hello, {message.from_user.username}!\n"
                         f"Добавь меня в группу в качестве администратора "
                         f"и я буду тебе полезен!")


@router.message()
async def echo(message: Message):
    print(f"echo_us {message.text}")