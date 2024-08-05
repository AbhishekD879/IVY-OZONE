const initialDataApi = require('../../lib/api/initialDataManager'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, ''),
    paramsDeviceType = req.params.deviceType,
    isUnsupportedDevice = ['mobile', 'tablet', 'desktop'].indexOf(paramsDeviceType) === -1,
    deviceType = isUnsupportedDevice ? 'mobile' : paramsDeviceType;

  initialDataApi.getInitialData(brand, deviceType)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
