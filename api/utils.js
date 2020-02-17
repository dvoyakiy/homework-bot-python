const {createHmac, createHash} = require('crypto');
const jwt = require('jsonwebtoken');
const uuidv4 = require('uuid/v4');

const { ACCESS_TOKEN_SECRET, EXPIRES_IN } = require('./config');


async function checkSignature (secret, { hash, ...data }) {
    const checkString = Object.keys(data)
        .sort()
        .map(k => (`${k}=${data[k]}`))
        .join('\n');

    const hmac = createHmac('sha256', secret)
        .update(checkString)
        .digest('hex');

    return hmac === hash;
}

async function createSecret(string){
    return createHash('sha256').update(string).digest();
}

async function issueTokenPair(payload) {
    const accessToken = jwt.sign(payload, ACCESS_TOKEN_SECRET, {
        expiresIn: EXPIRES_IN
    });
    const refreshToken = uuidv4();

    return {
        accessToken,
        refreshToken
    }
}

module.exports = {
    checkSignature,
    createSecret,
    issueTokenPair
};