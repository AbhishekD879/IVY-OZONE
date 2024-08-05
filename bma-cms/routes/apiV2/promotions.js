const apiManager = require('../../lib/api'),
  sendError = require('../api/sendError'),
  sendResponse = require('../api/sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');

  apiManager.run('promotionsV2', {
    brand,
    categories: req.params.categories
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
