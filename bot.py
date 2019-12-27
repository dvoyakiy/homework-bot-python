from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from bson.objectid import ObjectId

from config import TOKEN, DEBUG
from db import users_collection, chats_collection, subjects_collection, tasks_collection
import utils
from states import BotState

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if DEBUG:
    @dp.message_handler(commands=['id'])
    async def get_chat_id(m: Message):
        await m.reply(m.chat.id)


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
    text, reply_markup = utils.get_subjects_message(m)

    await m.reply(text=text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda q: q.data == 'subjects_list')
async def subjects_list_button(q: CallbackQuery):
    text, reply_markup = utils.get_subjects_message(q.message)

    await q.message.edit_text(text)
    await q.message.edit_reply_markup(reply_markup)


@dp.callback_query_handler(lambda q: q.data.startswith('subject'))
async def subject_query(q: CallbackQuery):
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


@dp.callback_query_handler(lambda q: q.data == 'back')
async def back_button(q: CallbackQuery):
    chat_id = q.message.chat.id
    subjects = list(subjects_collection.find({'chat_id': chat_id}))

    reply_markup = InlineKeyboardMarkup(inline_keyboard=utils.create_markup(subjects))

    await q.message.edit_text('Choose:')
    await q.message.edit_reply_markup(reply_markup)


@dp.callback_query_handler(lambda q: q.data.startswith('add'))
async def add_button(q: CallbackQuery, state: FSMContext):
    await BotState.waiting.set()

    data = {
        'chat_id': q.message.chat.id,
        'user_id': q.from_user['id'],
        'subject_id': q.data.split('_')[1]
    }

    await state.update_data(data)

    await q.message.edit_text('Send homework')
    await q.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Cancel', callback_data='cancel_' + q.data.split('_')[1])
        ]
    ]))


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


@dp.callback_query_handler(lambda q: q.data.startswith('cancel'))
async def cancel_button(q: CallbackQuery, state: FSMContext):
    await state.finish()
    await subject_query(q)


@dp.message_handler(state=BotState.waiting)
async def any_message(m: Message, state: FSMContext):
    data = await state.get_data()

    if data and m.chat.id == data['chat_id'] and m.from_user['id'] == data['user_id']:

        task = {
            'user_id': data['user_id'],
            'chat_id': data['chat_id'],
            'subject_id': ObjectId(data['subject_id']),
            'task_text': m.text
        }

        tasks_collection.insert_one(task)
        data.clear()

        await state.finish()
        await m.reply('Homework added!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Subjects list', callback_data='subjects_list')
            ]
        ]))
