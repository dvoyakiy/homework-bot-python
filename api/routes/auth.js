const { BOT_TOKEN } = require('../config');

const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');

const {checkSignature, createSecret} = require('../utils');
const {registerUser} = require('../service/service');


router.post('/', (req, res) => {
    let status = 401, jwtToken;
    const data = {};

    const secretKey = createSecret(BOT_TOKEN);
    const valid = checkSignature(secretKey, req.body);

    if (valid) {
        status = 200;

        jwtToken = jwt.sign({
            id: req.body.id
        }, process.env.SECRET);

        data.token = jwtToken;

        registerUser(req.body);
    }

    res.status(status).send(data);
});

module.exports = router;
