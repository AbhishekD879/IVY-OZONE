'use strict';

const siteServer = require('./'),
  keystone = require('../../bma-betstone'),
  moment = require('moment'),
  apiManager = require('../api'),
  _ = require('underscore'),
  Logger = require('../logger');

/**
 * get active modules from db
 * @returns {Promise}
 */
function getModules() {
  return new Promise((resolve, reject) => {
    keystone.mongoose.model('HomeModule')
      .find()
      .where({
        'visibility.enabled': true
      })
      .gt(
        'visibility.displayTo', moment().utc()
          .toDate()
          .toISOString()
      )
      .sort('displayOrder')
      .exec()
      .then(result => {
        resolve(result);
      }, reject);
  });
}

/**
 * Update active modules
 * @returns {Promise}
 */
function updateModules() {
  Logger.info('AKAMAI', 'modular-content autoupdate');
  return getModules()
    .then(modules => {
      return Promise.all(modules.map(updateModule));
    })
    .then(modules => {
      const channels = [];

      modules.forEach(mod => {
        const publishToChannels = Array.isArray(mod.publishToChannels) ? mod.publishToChannels : [];
        publishToChannels.forEach(channel => channels.push(channel));
      });

      _.uniq(channels).forEach(brand => {
        apiManager.run('modularContent', { brand });
      });

      return modules;
    });
}

function setName(newEvent, oldEvent) {
  if (oldEvent.name === oldEvent.nameOverride && oldEvent.name !== newEvent.name) {
    newEvent.nameOverride = newEvent.name;
  } else {
    newEvent.nameOverride = oldEvent && oldEvent.nameOverride
      ? oldEvent.nameOverride
      : oldEvent.name;
  }
}

/**
 * Update 1 selected module
 * @param module
 * @returns {Promise}
 */
function updateModule(module) {
  return new Promise((resolve, reject) => {
    let selectionType = module.dataSelection.selectionType;

    if (module.dataSelection.selectionType.indexOf('Enhanced Multiples') > -1) {
      selectionType = 'EnhancedMultiples';
    }

    siteServer.getEvents(
      selectionType,
      module.dataSelection.selectionId,
      moment(module.eventsSelectionSettings.from).utc()
        .toDate()
        .toISOString(),
      moment(module.eventsSelectionSettings.to).utc()
        .toDate()
        .toISOString()
    )
      .then(events => {
        return new Promise((resolve, reject) => { // eslint-disable-line no-shadow
          const moduleUpdateCB = function(err) {
            if (err) {
              reject(err);
            } else {
              resolve({
                _id: module._id,
                publishToChannels: module.publishToChannels
              });
            }
          };
          if (events) {
            const newTotalEvents = events.length,
              newEvents = module.maxRows ? events.slice(0, module.maxRows) : events,
              newEventsWithNameOverride = newEvents.map((event, i) => {
                const eventFromModule = _.findWhere(module.data, { id: event.id });
                if (eventFromModule) {
                  setName(event, eventFromModule);
                }
                return event;
              });
            module.update({ $set: { totalEvents: newTotalEvents, data: newEventsWithNameOverride } }, { w: 1 }, moduleUpdateCB);
          } else {
            module.update({ $set: { totalEvents: 0, data: [] } }, { w: 1 }, moduleUpdateCB);
          }
        });
      })
      .then(resolve, reject); // wrap Q promise into ES6 Promise
  });
}

module.exports = updateModules;
