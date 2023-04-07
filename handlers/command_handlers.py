from aiogram.types import Message
from aiogram.filters import Command, CommandStart
# from lexicon.lexicon import LEXICON_RU


# Этот хэндлер срабатывает на команду /start
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
# from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(Command(commands='help'))
async def process_start_command(message: Message):
    await message.answer(text='/start')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='/help')