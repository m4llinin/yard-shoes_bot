import asyncio

from config import config
from handlers import register_handlers


async def main():
    config.logger.info("Starting bot")
    try:
        register_handlers(config.dp)
        await config.bot.delete_webhook(drop_pending_updates=True)
        await config.dp.start_polling(config.bot)
    finally:
        await config.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        config.logger.error("Bot stopped!")
