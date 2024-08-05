const apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const brand = req.params.brand ? req.params.brand.replace(/[^\w\s]/gi, '') : 'bma';

  // Get countries from DB
  apiManager.run('countries', {
    brand
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, []);
    });
};
