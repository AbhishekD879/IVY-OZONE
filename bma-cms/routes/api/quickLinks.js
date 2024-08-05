const apiManager = require('../../lib/api'),
  sendError = require('./sendError'),
  sendResponse = require('./sendResponse');

exports = module.exports = function(req, res) {
  const brand = (req.params.brand === undefined) ? 'bma' : req.params.brand.replace(/[^\w\s]/gi, '');
  let raceType = (req.params.raceType === undefined) ? 'horseracing' : req.params.raceType.replace(/[^\w\s]/gi, '');

  if (raceType !== 'horseracing' && raceType !== 'greyhound') {
    raceType = 'horseracing';
  }

  apiManager.run('quickLinks', {
    brand,
    raceType
  }, true)
    .then(result => {
      sendResponse(result, res);
    }, err => {
      sendError({ msg: 'database error', err }, res);
    });
};
