import asyncio

from aiogram import Dispatcher, Bot

from handlers import us_commands, gr_commands, gr_nword, admin_commands

from middlewares.mw_anti_flood import AntiFloodMw

from data.db_main import db_start

from config_reader import config


async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMw(time_limit=2))

    dp.include_routers(
        admin_commands.router,
        gr_nword.router,
        gr_commands.router,
        us_commands.router,
    )

    await  db_start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())