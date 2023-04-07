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


# from lexicon.lexicon import LEXICON_RU
config : Config = load_config()
# Инициализируем роутер уровня модуля
router: Router = Router()
adm_ids = config.tg_bot.admin_ids


print('test2')
router.message.filter(F.from_user.id.in_(adm_ids))


button_1: KeyboardButton = KeyboardButton(text='Добавить пользователя')
button_2: KeyboardButton = KeyboardButton(text='Удалить пользователя')
button_3: KeyboardButton = KeyboardButton(text='Просмотр всех пользователей')
button_4: KeyboardButton = KeyboardButton(text='просмотр всех заявок на регистрацию')

# button_2: KeyboardButton = KeyboardButton(text='Просмотр всех пользователей')



keyboard_admin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1, button_2, button_3, button_4]])



# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='/start_povelitel', reply_markup=keyboard_admin, resize_keyboard=True)



@router.message(Text(startswith='одобрить', ignore_case=True))
async def approve_reg(message: Message):
    id_reg = int(message.text.split()[1])
    
    obj = db.add_user(id_reg)
    if obj == None:
        await message.answer(text='Что-то пошло не так, но мы уже взяли деньги и пропали', reply_markup=keyboard_admin, resize_keyboard=True)
    else:
        await bot.send_message(obj.user_id, f"Ваша заявка на регистрацию одобрена. Теперь вы можете пользоваться умным домом")

        await message.answer(text=f'Пользователь {obj.user_name} успешно добавлен', reply_markup=keyboard_admin, resize_keyboard=True)

    
    print(id_reg)
    print(message.text)

@router.message(Text(text='просмотр всех заявок на регистрацию'))
async def show_all_registr_appl(message: Message):
    
    appl_regs = db.show_all_app_registration()
    print(appl_regs)
    ans: list[str] = [f'Заявка {reg["id"]}, user_id : {reg["user_id"]}, user_name : {reg["user_name"]}' for reg in appl_regs]
    print(message.text)
    
    
    await message.answer(text='\n'.join(ans))
    

    
@router.message(Text(text='Удалить пользователя'))
async def del_user(message: Message):
    users = db.show_all_users()
    button_1: KeyboardButton = KeyboardButton(text='Добавить пользователя')

    buttons: list[KeyboardButton] = [KeyboardButton(str(user["id"]) + " : " + str(user["user_id"])) for user in users]
    print(users)
    await message.answer(text=json.dumps(users), reply_markup=buttons, resize_keyboard=True)


@router.message(Text(text='Просмотр всех пользователей'))
async def show_all_users(message: Message):
   

    users = db.show_all_users()
    ans: list[str] = [f'Пользователь {user["id"]}, user_id : {user["user_id"]}, user_name : {user["user_name"]}' for user in users]


    keyboard_admin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1, button_2, button_3]])
    await message.answer(text="\n".join(ans), ReplyKeyboardMarkup=keyboard_admin)

    
# Этот хэндлер срабатывает на команду /help
# @router.message(Command(commands='reg'))
# async def process_help_command(message: Message):
#     await bot.send_message(message.from_user.id, "test message") #like this
#     await message.answer(text='/help')
    
# @router.message(Command(commands='reg'))
