const jwt = require('jsonwebtoken');

const {ACCESS_TOKEN_SECRET} = require('../config');


module.exports.authRequired = function(req, res, next) {
    const authHeader = req.headers.authorization;
    const accessToken = authHeader && authHeader.split(' ')[1];

    if(!accessToken) return res.sendStatus(401);

    jwt.verify(accessToken, ACCESS_TOKEN_SECRET, (err, user_data) => {
        if(err) return res.sendStatus(403);

        req.user = user_data;
        next();
    })
};

