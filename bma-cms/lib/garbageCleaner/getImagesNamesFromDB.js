'use strict';

const keystone = require('../../bma-betstone');
const _ = require('underscore');
const banners = keystone.list('banners').model.find({})
  .select({
    _id: 0,
    uriMedium: 1,
    uriSmall: 1,
    desktop_uriMedium: 1,
    desktop_uriSmall: 1
  })
  .exec();
const promotions = keystone.list('promotions').model.find({})
  .select({
    _id: 0, uriMedium: 1
  })
  .exec();
const features = keystone.list('features').model.find({})
  .select({
    _id: 0, uriMedium: 1
  })
  .exec();
const offers = keystone.list('offer').model.find({})
  .select({
    _id: 0, imageUri: 1
  })
  .exec();

function getBannersImagesNames() {
  return banners.then(results => {
    return ['uriMedium', 'uriSmall', 'desktop_uriMedium', 'desktop_uriSmall'].map(type => _.pluck(results, type));
  });
}

function getOffersImagesNames() {
  return offers.then(results => _.pluck(results, 'imageUri'));
}

function getPromotionsImagesNames() {
  return promotions.then(results => _.pluck(results, 'uriMedium'));
}

function getFeaturesImagesNames() {
  return features.then(results => _.pluck(results, 'uriMedium'));
}

module.exports = function() {
  return Promise.all([
    getBannersImagesNames(),
    getOffersImagesNames(),
    getPromotionsImagesNames(),
    getFeaturesImagesNames()
  ])
    .then(images => {
      return [].concat(..._.flatten(images, true));
    });
};
