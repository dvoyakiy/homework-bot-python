const { CONNECTION_STRING } = require('../config');

const mongoose = require('mongoose');

const User = require('./models/User');
const { issueTokenPair } = require('../utils');

mongoose.set('useNewUrlParser', true);
mongoose.set('useUnifiedTopology', true);
mongoose
    .connect(CONNECTION_STRING, {useNewUrlParser: true})
    .catch(err => {
        console.error(err)
    });

async function registerUser({id, first_name, last_name, username, photo_url}) {
    const user = new User({
        username: username,
        user_id: id,
        first_name: first_name,
        last_name: last_name,
        user_pic: photo_url,
        tokens: [await issueTokenPair({id})]
    });

    try{
        await user.save();
    } catch (e) {
        console.error(e);
    }
}

async function userExists(userId) {
    const user = await User.findOne({user_id: userId});
    return Boolean(user);
}

async function addToken(userId, token) {

}

module.exports = {
    registerUser,
    userExists,
    addToken
};