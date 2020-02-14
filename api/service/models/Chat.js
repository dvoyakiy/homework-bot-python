const mongoose = require('mongoose');

const ChatSchema = mongoose.Schema({
    chat_id: Number,
    owner_id: Number,
    chat_name: String,
    type: Number
});

module.exports = mongoose.model('Chat', ChatSchema);