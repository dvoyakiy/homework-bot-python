from aiogram import executor
import logging

from bot import dp
import config


def main():
    if config.DEBUG:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)
    executor.start_polling(dispatcher=dp, skip_updates=True)


if __name__ == '__main__':
    main()
