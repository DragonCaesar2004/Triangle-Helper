import asyncio
import logging
import tracemalloc

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.staring import register_starting
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.sending_poll import send_my_poll

tracemalloc.start()
logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_starting(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # async def send_my_poll():
    #     # создание объекта часового пояса для Москвы
    #     tz = pytz.timezone('Europe/Moscow')
    #     # получение текущей даты и времени в Москве
    #     now = datetime.now(tz)
    #     # вывод даты и времени в формате 'YYYY-MM-DD HH:MM:SS'
    #     string_time_and_date = now.strftime('%Y-%m-%d %H:%M:%S')
    #
    #     await bot.send_message(chat_id=469527568, text='опрос')

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    proxy_url = 'http://proxy.server:3128'
    bot = Bot(token=config.tg_bot.token, proxy=proxy_url,parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # TODO СДЕЛАТЬ ТАК ЧТОБЫ ЧТЕНИЕ И ЗАПИСЬ БАЗЫ ДАННЫХ НЕ ПЕРЕСЕКАЛИСЬ
    scheduler = AsyncIOScheduler()  # создаем инстанс шедулера
    scheduler.add_job(send_my_poll, 'cron', hour=config.misc.hours, minute=config.misc.minutes, args=(bot,))
    await send_my_poll(bot) #????

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        bot.get_session().close()
        await dp.storage.close()
        await dp.storage.wait_closed()
        #session = await bot.get_session()
       #if session is not None:
         #await session.close()

        scheduler.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
