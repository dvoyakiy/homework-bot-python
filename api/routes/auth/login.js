const express = require('express');
const router = express.Router();

const { BOT_TOKEN } = require('../../config');

const {checkSignature, createSecret, issueTokenPair} = require('../../utils');
const {userExists, registerUser} = require('../../service/service');


router.post('/', async (req, res) => {
    let status = 401;
    const data = {};

    const secretKey = await createSecret(BOT_TOKEN);
    const valid = await checkSignature(secretKey, req.body);

    if (valid) {
        status = 200;
        const { accessToken, refreshToken } = await issueTokenPair({
            id: req.body.id
        });

        data.accessToken = accessToken;
        data.refreshToken = refreshToken;

        if (!(await userExists(req.body.id))) await registerUser(req.body);
    }

    res.status(status).send(data);
});

module.exports = router;
