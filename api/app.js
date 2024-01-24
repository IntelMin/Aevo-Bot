require('dotenv').config();
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser'
import cookieParser from 'cookie-parser';

const app = express();
const http = require('http').createServer(app);

// express init
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cors());
app.use(cookieParser())

// api routes
require('./routers/index.router')(app);

const port = process.env.PORT || 8080;
http.listen(port, () => {
  console.log('listening on *:' + port);
});
