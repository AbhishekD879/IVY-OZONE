'use strict';
const Logger = require('../logger');

module.exports = function() {
  return Promise.resolve().then(() => Logger.info('CLEAN_AKAMAI_CACHE', 'garbage cleaner successfully patched!'));
};
