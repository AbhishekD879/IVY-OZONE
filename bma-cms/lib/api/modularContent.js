const keystone = require('../../bma-betstone'),
  Q = require('q'),
  _ = require('underscore');

/**
 *
 * @returns {adapter.deferred.promise|*|promise|promiseAndHandler.promise|returnArgs.promise|defer.promise}
 */
exports = module.exports = function(options) {
  const currentDate = new Date();

  function assembleModularContent(brand) {
    const totalDeferred = Q.defer(),
      modelToObject = function(model) {
        return JSON.parse(JSON.stringify(model));
      },
      getDevices = function(devices) {
        const devicesArr = [];
        for (const i in devices) {
          if (devices[i]) {
            devicesArr.push(i);
          }
        }
        return devicesArr;
      };

    function getModuleRibbonTabs() {
      const deferred = Q.defer(),
        ribbonResult = [];

      keystone.list('ModuleRibbonTabs')
        .model.find()
        .where({ visible: true, brand })
        .sort('sortOrder')
        .exec()
        .then(result => {
          result.forEach((item, key) => {
            ribbonResult[key] = {};
            ribbonResult[key].title = item.title;
            ribbonResult[key].directiveName = item.directiveName;
            ribbonResult[key].visible = item.visible;
            ribbonResult[key].id = item.ID;
            ribbonResult[key].url = item.url;
            ribbonResult[key].modules = [];
            ribbonResult[key].sortBy = item.sortBy;
            ribbonResult[key].showTabOn = item.showTabOn;
            ribbonResult[key].devices = getDevices(modelToObject(item.devices));
          });
          deferred.resolve(ribbonResult);
        },
        err => {
          deferred.reject(err);
        }
      );

      return deferred.promise;
    }

    function getHomeModules() {
      const deferred = Q.defer();

      keystone.mongoose.model('HomeModule')
        .find()
        .where({
          'visibility.enabled': true,
          publishToChannels: brand
        })
        .where('visibility.displayTo')
        .gt(currentDate)
        .sort('displayOrder')
        .exec()
        .then(result => {
          const cleanModules = [];

          result.forEach((module, moduleKey) => {
          // If module has no event data throw it away.
            if ((module.data === undefined || module.data.length === 0) &&
              module.dataSelection.selectionType !== 'RacingGrid'
            ) {
              return;
            }
            if (!module.publishedDevices || !module.publishedDevices[brand]) {
              module.publishedDevices = ['desktop', 'mobile', 'tablet'];
            } else {
              module.publishedDevices = _.each(module.publishedDevices[brand], (device, key) => {
                if (!device) {
                  delete module.publishedDevices[brand][key];
                }
              });
              module.publishedDevices = _.isObject(module.publishedDevices) ? Object.keys(module.publishedDevices) : [];
            }
            cleanModules.push(module);
          });
          deferred.resolve(cleanModules);
        }, err => {
          deferred.reject(err);
        });

      return deferred.promise;
    }

    Q.all([ getModuleRibbonTabs(), getHomeModules() ]).spread((tabs, modules) => {
      const finalResult = [],
        eventsData = {
          eventsIds: [],
          outcomesIds: [],
          enhMultiplesIds: [],
          typeIds: [],
          racingEventsIds: []
        };

      tabs.forEach((tab, tabKey) => {
        finalResult[tabKey] = tab;
        modules.forEach((module, moduleKey) => {
          if (tab.directiveName === module.navItem) {
            finalResult[tabKey].modules[moduleKey] = module;
            _.each(module.data, item => {
              item.outcomeStatus = false;
              item.outcomeId = null;
              item.marketsCount = Number(item.marketCount);

              if (module.dataSelection.selectionType === 'Selection') {
                eventsData.outcomesIds.push(Number(module.dataSelection.selectionId));
                item.marketsCount = null;
                item.outcomeStatus = true;
                item.outcomeId = Number(module.dataSelection.selectionId);
              }

              if (module.dataSelection.selectionType === 'Type') {
                if (item.outright) {
                  eventsData.typeIds.push(Number(module.dataSelection.selectionId));
                } else {
                  eventsData.eventsIds.push(Number(item.id));
                }
              }

              if (module.dataSelection.selectionType === 'RaceTypeId') {
                eventsData.racingEventsIds.push(Number(item.id));
              }

              if (module.dataSelection.selectionType.indexOf('Enhanced Multiples') > -1) {
                eventsData.enhMultiplesIds.push(Number(item.id));
              }

              delete item.marketCount;
            });
          }
        });
      });

      finalResult.push(eventsData);
      totalDeferred.resolve(finalResult);
    });

    return totalDeferred.promise;
  }

  return assembleModularContent(options.brand);
};
