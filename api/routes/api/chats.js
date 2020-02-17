const express = require('express');
const router = express.Router();

const {authRequired} = require('../../middleware/authRequired');


router.route('/')
    .post(authRequired, (req, res) => {
        res.json(req.user);
    });

module.exports = router;

