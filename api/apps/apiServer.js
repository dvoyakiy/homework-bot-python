const { API_PORT } = require('../config');

const apiServer = require('express')();
const bodyParser = require('body-parser');
const cors = require('cors');


apiServer.use(cors());
apiServer.use(bodyParser.urlencoded({
    extended: true
}));
apiServer.use(bodyParser.json());


const chats = require('../routes/api/chats');

apiServer.use('/api/chats', chats);


apiServer.listen(API_PORT, () => {
    console.log(`API server started on *: ${API_PORT}`)
});

