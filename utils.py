from db import chats_collection
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import Message
from math import ceil
from typing import Tuple

from db import subjects_collection


def is_private(chat_id):
    return chat_id > 0


def chat_exists(chat_id):
    return bool(chats_collection.find_one({'chat_id': chat_id}))


def create_markup(subjects):
    length = len(subjects)

    def _get_rows(elements_in_row):
        rows = ceil(length / elements_in_row)
        added = 0
        res = []

        for r in range(rows):
            row_el = []

            try:
                for i in range(elements_in_row):
                    row_el.append(
                        InlineKeyboardButton(
                            text=subjects[added + i]['title'],
                            callback_data='subject_' + str(subjects[added + i]['_id'])
                        )
                    )

                added += elements_in_row
            except IndexError:
                continue
            finally:
                res.append(row_el)

        return res

    if length == 0:
        return []

    if 0 < length < 6:
        return [[InlineKeyboardButton(
            text=s['title'],
            callback_data='subject_' + str(s['_id'])
        )] for s in subjects]

    if 6 <= length <= 8:
        return _get_rows(2)

    if 8 < length:
        return _get_rows(3)


def get_subjects_message(m: Message) -> Tuple[str, InlineKeyboardMarkup]:
    chat_id = m.chat.id
    subjects = list(subjects_collection.find({'chat_id': chat_id}))

    if subjects:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=create_markup(subjects))
        text = 'Choose subject:'
    else:
        # TODO: Add callback button with login url if no subjects
        reply_markup = None
        text = 'No subjects were added.'

    return text, reply_markup
