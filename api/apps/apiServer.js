const { API_PORT } = require('../config');
const { createServer } = require('../utils');

const apiServer = createServer();


const chats = require('../routes/api/chats');

apiServer.use('/api/chats', chats);


apiServer.listen(API_PORT, () => {
    console.log(`API server started on *: ${API_PORT}`)
});

