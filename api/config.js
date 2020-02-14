require('dotenv').config();

const DEBUG = true;

const BOT_TOKEN = process.env.TOKEN;
const PORT = process.env.PORT;
const SECRET = process.env.SECRET;

const CONNECTION_STRING = DEBUG ? 'mongodb://localhost:27017' : process.env.MONGO_CONNECTION_STRING;
const DB_NAME = DEBUG ? 'hw_bot_dev' : process.env.DB_NAME;

const chatTypes = {
    group: -1,
    private: 0
};

module.exports = {
    BOT_TOKEN,
    PORT,
    SECRET,
    CONNECTION_STRING,
    DB_NAME,
    chatTypes
};

