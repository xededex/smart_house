import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config,  load_config
from handlers import auth_handlers, command_handlers,  reg_handlers
import multiprocessing
import comport_driver.serialworker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from util_threadings.warnings_check import init_, check_warnings
# from .warnings_check import init, check_warnings
# from util_threadings.warnings_check import init, check_warnings
input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()


async def test(i):
    print(1)

# Функция конфигурирования и запуска бота
async def main() -> None:
    cp = comport_driver.serialworker.ComPort(input_queue, output_queue)

    # Загружаем конфиг в переменную config
    config: Config = load_config()
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    init_(bot, input_queue, output_queue)
    
    dp: Dispatcher = Dispatcher()
    command_handlers.init(bot, input_queue, output_queue, cp)
    reg_handlers.init(bot)
    auth_handlers.init(bot)
    dp.include_router(auth_handlers.router)
    dp.include_router(command_handlers.router)
    dp.include_router(reg_handlers.router)

    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    

    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(check_warnings, "interval", seconds=5, args=())
    scheduler.start()

    # loop = asyncio.get_event_loop()
    # loop.create_task(check_warnings())
    # print("ewqeqw")
    await dp.start_polling(bot)




if __name__ == '__main__':
    print("aposteriori main2")
    asyncio.run(main())
    print("aposteriori main")