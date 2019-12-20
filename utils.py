from db import chats_collection
from aiogram.types.inline_keyboard import InlineKeyboardButton
from math import ceil


def is_private(chat_id):
    return chat_id > 0  # check docs about chat_id == 0


def chat_exists(chat_id):
    return bool(chats_collection.find_one({'chat_id': chat_id}))


def create_markup(subjects):
    l = len(subjects)

    def _get_rows(elements_in_row):
        rows = ceil(l / elements_in_row)
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

    if l == 0:
        return []

    if 0 < l < 6:
        return [[InlineKeyboardButton(
            text=s['title'],
            callback_data='subject_' + str(s['_id'])
        )] for s in subjects]

    if 6 <= l <= 8:
        return _get_rows(2)

    if 8 < l:
        return _get_rows(3)
