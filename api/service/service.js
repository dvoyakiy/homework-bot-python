const { CONNECTION_STRING } = require('../config');

const mongoose = require('mongoose');

const User = require('./models/User');

mongoose.set('useNewUrlParser', true);
mongoose.set('useUnifiedTopology', true);
mongoose
    .connect(CONNECTION_STRING, {useNewUrlParser: true})
    .catch(err => {
        console.error(err)
    });

async function registerUser({id, first_name, last_name, username, photo_url}) {
    if (!(await _exists(id))) {
        const user = new User({
            username: username,
            user_id: id,
            first_name: first_name,
            last_name: last_name,
            user_pic: photo_url
        });

        try{
            await user.save();
        } catch (e) {
            console.error(e);
        }
    }
}

async function _exists(user_id) {
    const user = await User.findOne({user_id: user_id});
    console.log(user);
    return Boolean(user);
}

module.exports = {
    registerUser
};