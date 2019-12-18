from pymongo import MongoClient

import config


client = MongoClient(config.CONNECTION_STRING)
db = client[config.DB_NAME]

users_collection = db['users']
chats_collection = db['chats']
subjects_collection = db['subjects']
