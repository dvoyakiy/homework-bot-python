const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
    user_id: Number,
    username: String,
    first_name: String,
    last_name: String,
    user_pic: String,
    tokens: [{
        accessToken: String,
        refreshToken: String
    }]
});

module.exports = mongoose.model('User', UserSchema);