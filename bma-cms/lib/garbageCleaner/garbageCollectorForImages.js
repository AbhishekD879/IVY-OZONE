'use strict';
const AkamaiImagesCollector = require('./AkamaiImagesCollector');
const getImagesNamesFromDB = require('./getImagesNamesFromDB');
const _ = require('underscore');
const Logger = require('../logger');

module.exports = function() {
  return Promise.all([new AkamaiImagesCollector().getImagesByBrands(), getImagesNamesFromDB()])
    .then(collectGarbage)
    .catch(e => Logger.error('GARBAGE_COLLECTOR', e));
};

/**
 * compares images in DB and on Akamai and finds difference (garbage)
 * @param {Object} files sorted by brands
 * @param {Array} array of images mentioned in DB
 * @returns {Object} garbage files sorted by brands
 */

function collectGarbage([akamaiResults, dbResults]) {
  const garbage = {};
  _.each(akamaiResults, (files, brand) => {
    const collection = files.filter(absentInDB);
    if (collection.length) {
      garbage[brand] = collection;
    }
  });
  return garbage;
  function absentInDB(file) {
    return dbResults.indexOf(file) === -1;
  }
}
