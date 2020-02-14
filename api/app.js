const { PORT } = require('./config');

const app = require('express')();
const bodyParser = require('body-parser');
const cors = require('cors');


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


const auth = require('./routes/auth');

app.use('/auth', auth);


app.listen(PORT, () => {
    console.log(`Started on *: ${PORT}`)
});