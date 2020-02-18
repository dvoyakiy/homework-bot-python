const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
    username: String,
    user_id: Number,
    first_name: String,
    last_name: String,
    user_pic: String,
    tokens: [String]
});

module.exports = mongoose.model('User', UserSchema);