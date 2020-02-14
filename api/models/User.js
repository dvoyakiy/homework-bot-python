const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
    username: String,
    user_id: Number,
    first_name: String,
    second_name: String,
    user_pic: String
});

module.exports = mongoose.model('User', UserSchema);