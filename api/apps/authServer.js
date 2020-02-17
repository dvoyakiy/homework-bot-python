const { AUTH_PORT } = require('../config');

const authServer = require('express')();
const bodyParser = require('body-parser');
const cors = require('cors');


authServer.use(cors());
authServer.use(bodyParser.urlencoded({
    extended: true
}));
authServer.use(bodyParser.json());


const login = require('../routes/auth/login');

authServer.use('/api/login', login);


authServer.listen(AUTH_PORT, () => {
    console.log(`Auth server started on *: ${AUTH_PORT}`)
});