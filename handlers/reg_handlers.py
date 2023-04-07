from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram import F
from aiogram.types import Message
from database.sqlite_api import DB_API
from config_data.config import Config, load_config
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from database.sqlite_api import DB_API
import json

bot = None
def init(in_bot):
    global bot
    bot = in_bot

db = DB_API()
ADMIN_IDS='1021596615'



# from lexicon.lexicon import LEXICON_RU
config : Config = load_config()
# Инициализируем роутер уровня модуля
router: Router = Router()
adm_ids = config.tg_bot.admin_ids

button_1: KeyboardButton = KeyboardButton(text='регистрация')

keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1]])

# def is_registered_and_not_adm(message: Message) -> bool:
#     return db.is_registered(message.from_user.id)


adm_ids = config.tg_bot.admin_ids

router.message.filter(lambda x : not (x.from_user.id in adm_ids) and not (db.is_registered(x.from_user.id)))




# Этот хэндлер срабатывает на команду /start
@router.message(Text(text='регистрация'))
async def process_start_command(message: Message):
    await message.answer(text='Вы не зарегистрированны в системе. Запрос на регистрацию отправлен администратору',)
    id_apply = db.create_app_registration(message.from_user.full_name, message.from_user.id)
    await bot.send_message(ADMIN_IDS, f"запрос на регистрацию от {message.from_user.full_name} : {message.from_user.id}. id заявки : {id_apply}")
    # await message.answer(text='/start_unathorized', reply_markup=keyboard_admin, resize_keyboard=True)



@router.message()
async def command_not_recognized(message: Message):
    await message.answer(text='Команда не распознана. Оставьте заявку на регистрацию для использования умного дома',reply_markup=keyboard, resize_keyboard=True)

