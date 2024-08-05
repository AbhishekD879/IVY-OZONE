const apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');

  apiManager.run('systemConfiguration', {
    brand
  }, true)
    .then(result => {
      // Define user IP. And send it to frontend.
      // That is need for IMG STREAM.
      // Maybe some additional features also requires IP of user.
      result.UserIp = req.headers['x-forwarded-for'] || req.connection.remoteAddress ||
        req.socket.remoteAddress || req.connection.socket.remoteAddress;

      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
