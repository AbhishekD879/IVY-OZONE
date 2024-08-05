const apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const uri = (req.params.uri === undefined) ? '' : req.params.uri.replace(/[^\w\s.-]/gi, ''),
    brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');

  apiManager.run('staticBlock', {
    brand,
    uri
  }, true)
    .then(result => {
      if (result) {
        sendResponse(result, res);
      } else {
        res.status(404);
        sendResponse('Page not fount', res);
      }
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
