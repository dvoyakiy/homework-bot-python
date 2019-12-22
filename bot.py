from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ForceReply
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from bson.objectid import ObjectId

from config import TOKEN
from db import users_collection, chats_collection, subjects_collection, tasks_collection
import utils

bot = Bot(TOKEN)
dp = Dispatcher(bot)

waiting = {}


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
    subjects = list(subjects_collection.find({'chat_id': chat_id}))

    inline_keyboard = utils.create_markup(subjects)

    if inline_keyboard:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        text = 'Choose:'
    else:
        # TODO: Add callback button with login url if no subjects
        reply_markup = None
        text = 'No subjects added.'

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


@dp.callback_query_handler(lambda q: q.data.startswith('subject'))
async def subjects_query(q: CallbackQuery):
    subject_id = ObjectId(q.data.split('_')[1])
    tasks_list = list(tasks_collection.find({'subject_id': subject_id}))

    try:
        message = str(tasks_list[-1]['task_text'])
    except IndexError:
        message = 'No tasks'

    await q.message.edit_text(message)
    await q.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Back', callback_data='back'),
            InlineKeyboardButton(text='Add homework', callback_data='add_' + str(subject_id)),
            InlineKeyboardButton(text='Update', callback_data='update_' + str(subject_id))
        ]
    ]))


@dp.callback_query_handler(lambda q: q.data == 'back')
async def back_button(q: CallbackQuery):
    chat_id = q.message.chat.id
    subjects = list(subjects_collection.find({'chat_id': chat_id}))

    reply_markup = InlineKeyboardMarkup(inline_keyboard=utils.create_markup(subjects))

    await q.message.edit_text('Choose:')
    await q.message.edit_reply_markup(reply_markup)


@dp.callback_query_handler(lambda q: q.data.startswith('add'))
async def add_button(q: CallbackQuery):
    waiting['chat_id'] = q.message.chat.id
    waiting['user_id'] = q.from_user['id']
    waiting['subject_id'] = q.data.split('_')[1]

    await q.message.reply('Send homework', reply_markup=ForceReply())


@dp.callback_query_handler(lambda q: q.data.startswith('update'))
async def update_button(q: CallbackQuery):
    subject_id = ObjectId(q.data.split('_')[1])
    tasks_list = list(tasks_collection.find({'subject_id': subject_id}))

    try:
        message = str(tasks_list[-1]['task_text'])
    except IndexError:
        message = 'No tasks'

    await q.message.edit_text(message)
    await q.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Back', callback_data='back'),
            InlineKeyboardButton(text='Add', callback_data='add_' + str(subject_id)),
            InlineKeyboardButton(text='Update', callback_data='update_' + str(subject_id))
        ]
    ]))


@dp.message_handler()
async def any_message(m: Message):

    if waiting and m.chat.id == waiting['chat_id'] and m.from_user['id'] == waiting['user_id']:

        task = {
            'user_id': waiting['user_id'],
            'chat_id': waiting['chat_id'],
            'subject_id': ObjectId(waiting['subject_id']),
            'task_text': m.text
        }

        tasks_collection.insert_one(task)
        waiting.clear()

        await m.reply('Homework added!')
