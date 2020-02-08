require('dotenv').config();

const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const PORT = process.env.PORT || 3000;

const auth = require('./routes/auth');

//todo use options in production
// const corsOptions = {
//     origin: 'some.domain',
//     optionsSuccessStatus: 200
// };

app.use(cors());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.use('/auth', auth);


app.listen(PORT, () => {
    console.log(`Started on *: ${PORT}`)
});