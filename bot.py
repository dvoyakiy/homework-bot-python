from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import TOKEN
from db import chats_collection, users_collection
import utils

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['new_chat'])
async def new_chat_command(m: Message):
    chat_id = m.chat.id
    user_doc = users_collection.find_one({'username': m.from_user['username']})
    user_id = user_doc['_id']

    if not utils.chat_exists(chat_id):
        chat_doc = {
            'chat_id': chat_id,
            'user_id': user_id
        }

        chats_collection.insert_one(chat_doc)
        await m.reply('Chat created!')
    else:
        await m.reply('Chat has been already created!')


# add auth functionality later
# @dp.message_handler(commands=['auth'])
# async def get_id_command(m: Message):
#     await m.reply('authenticated!' if utils.is_private(m.chat.id) else 'use private chat!')


@dp.message_handler(commands=['add_hw'])
async def add_hw_command(m: Message):

    await m.reply('Homework added!')

