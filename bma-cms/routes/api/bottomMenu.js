const apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');

  apiManager.run('bottomMenu', {
    brand
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};