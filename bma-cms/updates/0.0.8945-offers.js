'use strict';

var keystone = require('../bma-betstone'),
    Offers = keystone.list('offer');

exports = module.exports = function(next) {
  Offers.model.find({ vipLevels: { $exists: false } }).exec()
    .then(offers => Promise.all(offers.map(offer => offer.save())))
    .then(() => next(), next);
};