const apiManager = require('../../lib/api'),
  sendError = require('../api/sendError'),
  sendResponse = require('../api/sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');
  let deviceType = (req.params.deviceType === undefined) ? 'tablet' : req.params.deviceType.replace(/[^\w\s]/gi, '');

  if (deviceType !== 'tablet' && deviceType !== 'desktop') {
    deviceType = 'tablet';
  }

  apiManager.run('offersV2', {
    brand,
    deviceType
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
