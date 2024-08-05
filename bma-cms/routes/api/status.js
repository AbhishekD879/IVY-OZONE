const sendResponse = require('./sendResponse');

// Returns version from package.json
exports = module.exports = (req, res) => {
  const pjson = require('../../package.json');
  sendResponse({ version: pjson.version }, res);
};
