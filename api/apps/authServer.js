const { AUTH_PORT } = require('../config');
const { createServer } = require('../utils');

const authServer = createServer();


const login = require('../routes/auth/login');

authServer.use('/api/login', login);


authServer.listen(AUTH_PORT, () => {
    console.log(`Auth server started on *: ${AUTH_PORT}`)
});