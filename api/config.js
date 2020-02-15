require('dotenv').config();

const DEBUG = true;

const BOT_TOKEN = process.env.BOT_TOKEN;
const PORT = process.env.PORT;
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET;
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET;

const CONNECTION_STRING = DEBUG ? 'mongodb://localhost:27017/hw_bot_dev' : process.env.MONGO_CONNECTION_STRING;

const chatTypes = {
    group: -1,
    private: 0
};

module.exports = {
    BOT_TOKEN,
    PORT,
    ACCESS_TOKEN_SECRET,
    REFRESH_TOKEN_SECRET,
    CONNECTION_STRING,
    chatTypes
};

