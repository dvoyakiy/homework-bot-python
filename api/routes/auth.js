const express = require('express');
const router = express.Router();

const {checkSignature, createSecret} = require('../utils');


router.post('/', (req, res) => {
    const secretKey = createSecret(process.env.TOKEN);
    const valid = checkSignature(secretKey, req.body);

    const status = valid ? 200 : 401;

    res.status(status).send(valid);
});

module.exports = router;
