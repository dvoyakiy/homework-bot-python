from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types.message import ContentType
from aiogram.types import input_media, ParseMode
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import italic
from aiogram.utils.exceptions import MessageNotModified
from bson.objectid import ObjectId

from config import TOKEN, DEBUG, FileTypes
from db import users_collection, chats_collection, subjects_collection, tasks_collection
import utils
from states import States

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if DEBUG:
    @dp.message_handler(commands=['chat_id'])
    async def get_chat_id(m: Message):
        await m.reply(m.chat.id)


    @dp.message_handler(lambda m: m.caption == '/file_id', content_types=ContentType.PHOTO)
    async def get_chat_id(m: Message):
        await m.reply(m.photo[1].file_id)


    @dp.message_handler(commands=['file'])
    async def get_file_by_id(m: Message):
        await m.reply_photo(photo=m.get_args())


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


@dp.message_handler(commands=['subjects'], state='*')
async def subjects_command(m: Message):
    await States.subject_list.set()

    text, reply_markup = utils.get_subjects_message(m)

    await m.reply(text=text, reply_markup=reply_markup)


@dp.message_handler(state=States.waiting, commands=['done'])
async def done_command(m: Message, state: FSMContext):
    data = await state.get_data()

    try:
        task = {
            'user_id': data['user_id'],
            'chat_id': data['chat_id'],
            'subject_id': ObjectId(data['subject_id']),
            'task_text': data['task_text'],
            'files': data['files']
        }

        tasks_collection.insert_one(task)

        await m.reply('Homework added!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Subjects list', callback_data='subjects_list')
            ]
        ]))

        data.clear()
    except KeyError:
        return
    finally:
        await state.finish()


@dp.callback_query_handler(lambda q: q.data == 'subjects_list')
async def subjects_list_button(q: CallbackQuery):
    text, reply_markup = utils.get_subjects_message(q.message)

    await q.message.edit_text(text, reply_markup=reply_markup)


@dp.callback_query_handler(lambda q: q.data.startswith('subject'))
async def subject_query(q: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    subject_id = ObjectId(q.data.split('_')[1])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Back', callback_data='back'),
            InlineKeyboardButton(text='Add', callback_data='add_' + str(subject_id)),
            InlineKeyboardButton(text='Update', callback_data='update_' + str(subject_id))
        ]
    ])

    tasks_list = list(tasks_collection.find({'subject_id': subject_id}))
    last_task = tasks_list[-1] if tasks_list else None

    if current_state != States.subject_task.state:
        await States.subject_task.set()

    if not tasks_list:
        message = 'No tasks'
        await q.message.edit_text(message, reply_markup=reply_markup)
        return
    elif not last_task['task_text']:
        message = ''
    else:
        message = 'Last task is:\n' + last_task['task_text']

    files = last_task['files']
    if files:
        photos = [file for file in files if file['type'] == FileTypes.PHOTO]
        docs = [file for file in files if file['type'] == FileTypes.DOCUMENT]

        message = italic('Task with file(s)\n\n') + message
    else:
        data = {
            'subject_id': subject_id
        }

        await state.set_data(data)
        await q.message.edit_text(message, reply_markup=reply_markup)
        return

    await q.message.edit_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    data = {
        'subject_id': subject_id,
        'photos': [],
        'docs': []
    }

    if photos:
        media_group = [
            input_media.InputMediaPhoto(media=photo['id'], caption=photo['caption']) for photo in photos
        ]

        data['photos'] = await q.message.reply_media_group(media=media_group)

    if docs:
        for doc in docs:
            sent_doc = await q.message.reply_document(doc['id'], caption=doc['caption'])
            data['docs'].append(sent_doc)

    await state.update_data(data)


@dp.callback_query_handler(lambda q: q.data == 'back')
async def back_button(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    chat_id = q.message.chat.id
    subjects = list(subjects_collection.find({'chat_id': chat_id}))

    reply_markup = InlineKeyboardMarkup(inline_keyboard=utils.create_markup(subjects))

    await q.message.edit_text('Choose:', reply_markup=reply_markup)

    for key in data.keys():
        if key == 'subject_id':
            continue
        for item in data[key]:
            await item.delete()

    await state.finish()


@dp.callback_query_handler(lambda q: q.data.startswith('add'))
async def add_button(q: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    for key in data.keys():
        if key == 'subject_id':
            continue
        for item in data[key]:
            await item.delete()

    reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Cancel', callback_data='cancel_' + q.data.split('_')[1])
        ]
    ])

    await States.waiting.set()

    data = {
        'chat_id': q.message.chat.id,
        'user_id': q.from_user['id'],
        'subject_id': q.data.split('_')[1]
    }

    await state.update_data(data)

    await q.message.edit_text('Send homework', reply_markup=reply_markup)


@dp.callback_query_handler(lambda q: q.data.startswith('update'))
async def update_button(q: CallbackQuery, state: FSMContext):
    try:
        await subject_query(q, state)
    except MessageNotModified:
        return


@dp.callback_query_handler(lambda q: q.data.startswith('cancel'))
async def cancel_button(q: CallbackQuery, state: FSMContext):
    await state.finish()
    await subject_query(q, state)


@dp.message_handler(state=States.waiting, content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def photo_handler(m: Message, state: FSMContext):
    if m.photo:
        current_file_id = [p.file_id for p in m.photo][1]
        caption = m.caption
        file_type = FileTypes.PHOTO
    elif m.document:
        current_file_id = m.document.file_id
        caption = m.caption
        file_type = FileTypes.DOCUMENT

    data = await state.get_data()

    if 'files' not in data:
        data['files'] = []

    if 'task_text' not in data:
        data['task_text'] = m.caption

    # noinspection PyUnboundLocalVariable
    data['files'].append({
        'id': current_file_id,
        'type': file_type,
        'caption': caption
    })

    await state.update_data(data)


@dp.message_handler(state=States.waiting)
async def any_message(m: Message, state: FSMContext):
    data = await state.get_data()

    if data and m.chat.id == data['chat_id'] and m.from_user['id'] == data['user_id']:
        task = {
            'user_id': data['user_id'],
            'chat_id': data['chat_id'],
            'subject_id': ObjectId(data['subject_id']),
            'task_text': m.text,
            'files': []
        }

        tasks_collection.insert_one(task)
        data.clear()

        await state.finish()
        await m.reply('Homework added!', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Subjects list', callback_data='subjects_list')
            ]
        ]))
