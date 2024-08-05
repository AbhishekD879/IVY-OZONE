'use strict';

var keystone = require('../bma-betstone'),
    Banners = keystone.list('banners');

exports = module.exports = function(next) {
  Banners.model.find({ vipLevels: { $exists: false } }).exec()
    .then(banners => Promise.all(banners.map(banner => banner.save())))
    .then(() => next(), next);
};