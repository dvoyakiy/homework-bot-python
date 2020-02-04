from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False
TOKEN = os.environ.get('TOKEN')


# Message attachments types
class FileTypes:
    PHOTO = 0
    DOCUMENT = 1


if DEBUG:
    CONNECTION_STRING = 'mongodb://localhost:27017'
    DB_NAME = '<dev_db_name>'
else:
    CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')
    DB_NAME = '<prod_db_name>'
