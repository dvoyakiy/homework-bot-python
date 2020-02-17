const {createHmac, createHash} = require('crypto');

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

module.exports = {
    checkSignature,
    createSecret
};