'use strict';

var keystone = require('../bma-betstone'),
    Promotions = keystone.list('promotions');

exports = module.exports = function(next) {
  Promotions.model.find({ vipLevels: { $exists: false } }).exec()
    .then(promos => Promise.all(promos.map(promo => promo.save())))
    .then(() => next(), next);
};