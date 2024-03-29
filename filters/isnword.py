from aiogram.filters import Filter
from aiogram.types import Message

from data.get_data import get_nwords

from typing import List


class IsNWord(Filter):
    async def __call__(self, message: Message) -> bool:
        db = await get_nwords()
        for el in db:
            if el[0] in message.text.lower():
                return True
        return False
