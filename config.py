from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True
TOKEN = os.environ.get('TOKEN')


# Message attachments types
class FileTypes:
    PHOTO = 0
    DOCUMENT = 1
    NO_FILES = -1


if DEBUG:
    CONNECTION_STRING = 'mongodb://localhost:27017'
    DB_NAME = 'hw_bot_dev'
else:
    CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')
    DB_NAME = 'homework_bot'
