from aiogram.filters import BaseFilter
from aiogram.types import Message

from urlextract import URLExtract


class IsUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        extractor = URLExtract()
        if not extractor.find_urls(message.text): # []
            return False
        else: return True