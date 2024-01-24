require('dotenv').config();

var authApiRouter = require('./api/auth.router');

var errorHandler = require('../helpers/http-error-handler');

const route = (app) => {
  app.use('/api', authApiRouter);
  // global error handler
  app.use(errorHandler);
}

module.exports = route;