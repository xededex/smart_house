from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from config_data.config import Config, load_config
from database.sqlite_api import DB_API
import comport_driver.serialworker
from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram import F
from aiogram.types import Message
from database.sqlite_api import DB_API
from config_data.config import Config, load_config
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from database.sqlite_api import DB_API
import multiprocessing
import json
import os

router: Router = Router()
config : Config = load_config()
db = DB_API()
input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()
cp = comport_driver.serialworker.ComPort(input_queue, output_queue)
adm_ids = config.tg_bot.admin_ids

button_1: KeyboardButton = KeyboardButton(text='все устройства')
# button_2: KeyboardButton = KeyboardButton(text='устройство')
button_3: KeyboardButton = KeyboardButton(text='дым')
# button_4: KeyboardButton = KeyboardButton(text='уровень воды')
# button_5: KeyboardButton = KeyboardButton(text='стат')
button_6: KeyboardButton = KeyboardButton(text='все показатели')


# button_2: KeyboardButton = KeyboardButton(text='Просмотр всех пользователей')



keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1],  [button_3], [button_6]])

router.message.filter(lambda x : not (x.from_user.id in adm_ids) and db.is_registered(x.from_user.id))

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Приветствуем вас в проекте "умный дом"', reply_markup=keyboard, resize_keyboard=True)




@router.message(Text(text='все устройства'))
async def search_all_controllers(message: Message):
    files = os.listdir("/dev/")
    contr = list(filter(lambda x : x.find("ttyUSB") != -1, files))
    print(contr)

    if len(contr) == 0:
        await message.answer('На сервере не найдено устройств')
        return
    await message.answer('Устройства :\n' + "\n".join(contr), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)
    




@router.message(Text(text='все показатели'))
async def all_info(message: Message):
    print("water_lvl test")
    data = json.loads(await cp.request("all, "))
    dt = f"Газ : {'Есть' if data['gas'] == 0 else 'Нет'}\nCO2 - {data['smoke']}\nТемпература : {data['temp']}°C \nВлажность : {data['hum']}% \nУровень воды - {data['water']}\n"


    print(data)
    await message.answer(dt, ReplyKeyboardMarkup = keyboard, resize_keyboard=True)
    # files = os.listdir("/dev/")
    # contr = list(filter(lambda x : x.find("ttyUSB") != -1, files))
    # print(contr)

    # if len(contr) == 0:
    #     await message.answer('На сервере не найдено устройств')
    #     return
    # await message.answer('Устройства :\n' + "\n".join(contr), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)
    







@router.message(Text(text='устройство'))
async def process_start_command(message: Message):
    data = await cp.get_stat_arduino()
    await message.answer(str(data), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)


@router.message(Text(text='дым'))
async def process_start_command(message: Message):
    data = await cp.request("getlvlsmoke, ")
    await message.answer(str(data), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)


# @router.message(Text(text='эхо тест'))
# async def process_start_command(message: Message):
#     data = await cp.request("echo_test, ")
#     await message.answer(str(data), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)

@router.message(Text(text='уровень воды'))
async def water_lvl(message: Message):
    print("water_lvl test")
    data = await cp.request("getlvlwater, ")
    words = data.split(',')
    await message.answer(f"Уровень воды: {words[1]} \n", ReplyKeyboardMarkup = keyboard, resize_keyboard=True)

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Text(text='стат'))
async def process_start_command(message: Message):
    data = cp.get_stat_arduino()
    await message.answer(str(data), ReplyKeyboardMarkup = keyboard, resize_keyboard=True)

# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['help']))
# async def process_help_command(message: Message):
#     await message.answer('Напиши мне что-нибудь и в ответ '
#                         'я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"



    

    
    #
    
    

    
    