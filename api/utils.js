const {createHmac} = require('crypto');

function checkSignature (secret, { hash, ...data }) {
    const checkString = Object.keys(data)
        .sort()
        .map(k => (`${k}=${data[k]}`))
        .join('\n');

    const hmac = createHmac('sha256', secret)
        .update(checkString)
        .digest('hex');

    return hmac === hash;
}

module.exports.checkSignature = checkSignature;