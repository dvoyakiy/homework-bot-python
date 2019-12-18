from aiogram.types import Message
from db import chats_collection


def is_private(m: Message):
    return int(m.chat.id) > 0


def chat_exists(chat_id):
    return bool(chats_collection.find_one({'chat_id': chat_id}))
