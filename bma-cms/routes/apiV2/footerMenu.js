const apiManager = require('../../lib/api'),
  sendError = require('../api/sendError'),
  sendResponse = require('../api/sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, ''),
    paramsDeviceType = req.params.deviceType,
    isUnsupportedDevice = ['mobile', 'tablet', 'desktop'].indexOf(paramsDeviceType) === -1,
    deviceType = isUnsupportedDevice ? 'mobile' : paramsDeviceType;

  apiManager.run('footerMenuV2', {
    brand,
    deviceType
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
