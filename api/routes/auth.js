const express = require('express');
const router = express.Router();
const crypto = require('crypto');

const utils = require('../utils');


router.post('/', (req, res) => {
    const secretKey = crypto.createHash('sha256').update(process.env.TOKEN).digest();
    res.send(utils.checkSignature(secretKey, req.body));
});

module.exports = router;
