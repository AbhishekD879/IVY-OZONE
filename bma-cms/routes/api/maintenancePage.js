'use strict';

const
  apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = (req, res) => {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');
  const deviceType = req.params.deviceType;

  apiManager.run('maintenancePage', { brand, deviceType }, true)
    .then(
      result => sendResponse(result, res),
      err => sendError({ msg: 'database error', err }, res)
    );
};
