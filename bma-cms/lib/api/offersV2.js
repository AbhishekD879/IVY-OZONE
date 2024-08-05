const keystone = require('../../bma-betstone'),
  Q = require('q'),
  _ = require('underscore');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  const offerSubQuery = {
    brand: options.brand,
    showOfferOn: {
      $in: [options.deviceType, 'both']
    }
  };

  /**
   * Get unique id for appropriate sportCategory
   *
   * @returns {*|promise}
   */
  function getOfferModules(brand) {
    const deferred = Q.defer(),
      modules = {};

    keystone.list('offerModule')
      .model.find({ brand })
      .where({ disabled: false })
      .where('showModuleOn')
      .in([options.deviceType, 'both'])
      .sort('sortOrder')
      .exec((err, items) => {
        if (err) {
          deferred.reject(err);
        } else {
          items.forEach(item => {
            const module = {
              name: item.name,
              offers: []
            };

            modules[item._id] = module;
          });

          deferred.resolve(modules);
        }
      });

    return deferred.promise;
  }

  /**
   * Get Banners
   * Get list of available banners by category id
   * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
   */
  function getOffers(modules) {
    const deferred = Q.defer(),
      currentDate = new Date();

    if (!modules) {
      deferred.resolve([]);
      return deferred.promise;
    }

    keystone.list('offer')
      .model.find()
      .where({ disabled: false })
      .where(offerSubQuery)
      .where('module')
      .in(Object.keys(modules))
      .where('displayTo')
      .gt(currentDate)
      .sort('sortOrder')
      .exec()
      .then(items => {
        items.forEach(item => {
          const offer = {
            targetUri: item.targetUri,
            displayFrom: item.displayFrom,
            displayTo: item.displayTo,
            image: item.imageUri,
            useDirectImageUrl: item.useDirectImageUrl,
            directImageUrl: item.directImageUrl,
            vipLevels: Array.isArray(item.vipLevels) ? item.vipLevels : [],
            showToCustomer: item.showOfferTo !== 'both' ? [item.showOfferTo] : ['new', 'existing']
          };

          modules[item.module].offers.push(offer);
        });

        const modulesWithOffers = _.filter(modules, module => {
          return module.offers.length;
        });

        deferred.resolve(_.values(modulesWithOffers));
      }, err => {
        deferred.reject(err);
      });

    return deferred.promise;
  }

  return getOfferModules(options.brand).then(getOffers);
};
