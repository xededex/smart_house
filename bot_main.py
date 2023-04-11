import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config,  load_config
from handlers import auth_handlers, command_handlers,  reg_handlers

# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    command_handlers.init(bot)
    reg_handlers.init(bot)
    auth_handlers.init(bot)
    dp.include_router(auth_handlers.router)
    dp.include_router(command_handlers.router)
    dp.include_router(reg_handlers.router)

    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    print("1")
    await dp.start_polling(bot)

    
    print("2")

if __name__ == '__main__':
    asyncio.run(main())
    print("aposteriori main")