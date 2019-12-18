from db import chats_collection
from aiogram.types.inline_keyboard import InlineKeyboardButton


def is_private(chat_id):
    return chat_id > 0  # check docs about chat_id == 0


def chat_exists(chat_id):
    return bool(chats_collection.find_one({'chat_id': chat_id}))


def create_markup(collection):
    subjects = [s for s in collection]
    l = len(subjects)

    if l < 6:
        return [[InlineKeyboardButton(text=s['title'], callback_data=str(s['_id']))] for s in subjects]

    if l >= 6 <= 8:
        rows = round(l / 2)
        # make this done tomorrow


