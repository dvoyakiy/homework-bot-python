from db import chats_collection


def is_private(chat_id):
    return chat_id > 0  # check docs about chat_id == 0


def chat_exists(chat_id):
    return bool(chats_collection.find_one({'chat_id': chat_id}))
