const sendResponse = require('./sendResponse'),
  Logger = require('../../lib/logger');

exports = module.exports = function(obj, res, status) {
  /**
  * Sends error
  * @param {Object} obj
  */

  obj.msg = obj.msg || 'API Error';
  obj.key = obj.key || 'unknown error';
  obj.msg += ` (${obj.key})`;
  Logger.info('API', obj.msg + (obj.err ? ':' : ''));
  if (obj.err) {
    Logger.error('API', obj.err);
  }
  res.status(status || 500);
  sendResponse({ error: obj.key || 'error', detail: obj.err ? obj.err.message : '' }, res);
};
