from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.types.inline_keyboard import InlineKeyboardMarkup

from config import TOKEN
from db import users_collection, chats_collection, subjects_collection
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
            'chat_title': m.chat.full_name,
            'user_id': user_id,
            'type': 'private' if utils.is_private(chat_id) else 'group'
        }

        chats_collection.insert_one(chat_doc)
        await m.reply('Chat created!')
    else:
        await m.reply('Chat has been already created!')


@dp.message_handler(commands=['subjects'])
async def subjects_command(m: Message):
    chat_id = m.chat.id
    subjects = subjects_collection.find({'chat_id': chat_id})

    inline_keyboard = utils.create_markup(subjects)

    if inline_keyboard:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        text = 'Choose:'
    else:
        # TODO: Add callback button with login url if no subjects
        reply_markup = None
        text = 'No added subjects.'

    await m.reply(text=text, reply_markup=reply_markup)


@dp.message_handler(commands=['get_homework'])
async def add_hw_command(m: Message):

    await subjects_command(m)


@dp.message_handler(commands=['add_homework'])
async def add_hw_command(m: Message):

    await subjects_command(m)


@dp.message_handler(commands=['id'])
async def get_chat_id(m: Message):
    await m.reply(m.chat.id)
