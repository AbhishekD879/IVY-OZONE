const apiManager = require('../../lib/api'),
  sendError = require('../api/sendError'),
  sendResponse = require('../api/sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');
  let categoryUri = req.query.categoryUri ? req.query.categoryUri : req.params.categoryUri;

  // BACKWARD COMPATIBILITY: for handling error in BMA initialDataFactory with empty category
  // TODO: remove
  if (categoryUri === undefined) {
    categoryUri = 'home';
  }

  // Remove all special characters
  categoryUri = categoryUri.replace(/[^-^_^\w\s]/gi, '');

  apiManager.run('bannersV2', {
    brand,
    categoryUri
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
