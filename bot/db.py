from pymongo import MongoClient

from bot import config

client = MongoClient(config.CONNECTION_STRING)
db = client[config.DB_NAME]

users_collection = db['users']
chats_collection = db['chats']
subjects_collection = db['subjects']
tasks_collection = db['tasks']
