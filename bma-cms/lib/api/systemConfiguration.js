'use strict';

const keystone = require('../../bma-betstone'),
  Q = require('q'),
  _ = require('lodash');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  /**
   * Get System Configuration Model
   * Get list of system configurations
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  const getModel = function(brand) {
    const deferred = Q.defer();

    // Load the Module Structure Type model
    keystone.mongoose.model('Structure')
      .findOne()
      .where({
        brand,
        lang: 'en'
      })
      .exec()
      .then(model => {
        _.each(model.structure, group => {
          _.each(group, field => {
            const multiselectValue = _.get(field, 'multiselectValue');
            if (multiselectValue) {
              field.multiselectValue = _.values(field.multiselectValue);
            }
          });
        });
        deferred.resolve(model.structure);
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  };

  return getModel(options.brand);
};
