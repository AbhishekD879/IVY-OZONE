'use strict';

const siteServerAPI = require('./siteServerAPI'),
  _ = require('underscore'),
  Logger = require('../../lib/logger');

// TODO: add more informative comments

/**
 *
 * @param response
 * @returns {Promise}
 */
function getEventsFromResponse(response) {
  return new Promise((resolve, reject) => {
    const result = [];

    if (response.SSResponse && response.SSResponse.children) {
      response.SSResponse.children.forEach(item => {
        if (item.event && item.event.children && item.event.children.length && item.event.eventStatusCode !== 'S') {
          const event = item.event;
          result.push({
            nameOverride: event.name,
            id: event.id,
            name: event.name,
            displayOrder: event.displayOrder,
            startTime: event.startTime
          });
        }
      });

      resolve(result);
    } else {
      reject(new Error('No SSResponse children'));
    }
  });
}

/**
 * add 'outright' flag to items
 * @param flag
 * @param items
 * @returns {Array}
 */
function setOutrightFlag(flag, items) {
  _.each(items, item => {
    item.outright = flag;
  });

  return items;
}

/**
 * get events by Race Type Id
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {*|promise}
 */
function getEventsByRaceType(typeId, from, to) {
  return siteServerAPI.getEventsByRaceType(typeId, from, to)
    .then(getEventsFromResponse);
}

/**
 * get category code for selection
 * @param typeId
 * @returns {Promise}
 */
function getClassToSubTypeForType(typeId) {
  return siteServerAPI.getClassToSubTypeForType(typeId)
    .then(result => result.SSResponse.children[0].class.categoryCode);
}

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {*|promise}
 */
function getOutrightsDataByType(typeId, from, to) {
  return siteServerAPI.getOutrights(typeId, from, to)
    .then(getEventsFromResponse)
    .then(setOutrightFlag.bind(null, true));
}

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @param {string} [marketCode]
 * @param {string} [marketNames]
 * @returns {*|promise}
 */
function getEventsByTypeAndMarket(typeId, from, to,
                                  marketCode = 'MR,HH,2W,3W',
                                  marketNames = ['Match Betting', 'Match Winner',
                                    'Money Line', 'Fight Betting', 'Match Result']
) {
  return siteServerAPI.getEventsByTypeAndMarket(typeId, from, to, marketCode, marketNames)
    .then(getEventsFromResponse)
    .then(setOutrightFlag.bind(null, false));
}

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @param {string} [marketCode]
 * @param {string} [marketNames]
 * @returns {*|promise}
 */
function getEventsByTypeAndMarketAndMainMarkets(typeId, from, to, marketCode, marketNames) {
  /**
   * middleware promise to add 'Main Markets' events
   * @param events
   * @returns {*|promise}
     */
  function addMainMarketsEvents(events) { // eslint-disable-line no-unused-vars
    // collection of event ids
    const eventIds = events.map(event => { return event.id; });

    // get events with 'Main Markets' and not empty market code
    // add collected event ids as IdNotIn to prevent fetch of previously fetched events
    return siteServerAPI.getEventsByTypeAndMarket(typeId, from, to, 'isNotEmpty', 'Main Markets',
      { eventIdNotIn: eventIds.join(',') }
    )
      .then(getEventsFromResponse)
      .then(additionalEvents => {
        // add fetched events
        additionalEvents.forEach(item => {
          events.push(item);
        });

        return events;
      });
  }

  return siteServerAPI.getEventsByTypeAndMarket(typeId, from, to, marketCode, marketNames)
    .then(getEventsFromResponse)
    // .then(addMainMarketsEvents) // temporary disabled
    .then(setOutrightFlag.bind(null, false));
}

function concatOutrights(results) {
  Logger.info('concatOutrights', JSON.stringify(results));
  return _.uniq(results[1].concat(results[0]), x => {
    return x.id;
  });
}

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {*|promise}
 */

function getOutrightsAndEventsByType(typeId, from, to) {
  return Promise.all([getEventsByTypeAndMarketAndMainMarkets(typeId, from, to, 'MR,HH,3W,2W'),
    getOutrightsDataByType(typeId, from, to)]
  ).then(concatOutrights);
}

/**
 *
 * @param outcomeId
 * @returns {*|promise}
 */
function getOutcomeByOutcome(outcomeId) {
  return siteServerAPI.getOutcomeByOutcome(outcomeId)
    .then(response => {
      if (response.SSResponse.children[0].event) {
        const event = response.SSResponse.children[0].event;

        return [{
          nameOverride: event.children[0].market.children[0].outcome.name.replace(/\|/g, ''),
          id: event.id,
          name: event.name
        }];
      }
      return [];
    });
}

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {*|promise}
 */
function getEventsByType(typeId, from, to) {
  return siteServerAPI.getEventsByType(typeId, from, to).then(getEventsFromResponse);
}

/**
 *
 * @param eventIds
 * @returns {*|promise}
 */
function getMarketsCountByEventIds(eventIds) {
  return siteServerAPI.getMarketsCountByEventIds(eventIds)
    .then(response => {
      const counts = {};

      _.each(response.SSResponse.children, item => {
        if (_.has(item, 'aggregation')) {
          counts[item.aggregation.refRecordId] = item.aggregation.count;
        }
      });

      return counts;
    });
}

function getEvents(selectionType, selectionId, from, to) {
  return new Promise((resolve, reject) => {
    if (
      selectionType === 'RaceTypeId' ||
      selectionType === 'Type' ||
      selectionType === 'Selection' ||
      selectionType === 'EnhancedMultiples'
    ) {
      ({
        RaceTypeId: getEventsByRaceType,
        Type: getOutrightsAndEventsByType,
        Selection: getOutcomeByOutcome,
        EnhancedMultiples: getEventsByType
      }[selectionType](selectionId, from, to))
        .then(openBetEventOrdering)
        .then(filterEventFields)
        .then(addMarketsCount)
        .then(resolve, reject);
    } else {
      resolve(null);
    }
  });
}

function openBetEventOrdering(events) {
  if (events.length) {
    events.sort((a, b) => { // eslint-disable-line consistent-return, array-callback-return
      if (Number(a.displayOrder) < Number(b.displayOrder)) return -1;
      if (Number(a.displayOrder) > Number(b.displayOrder)) return 1;
      if (Number(a.displayOrder) === Number(b.displayOrder)) {
        if (a.startTime < b.startTime) return -1;
        if (a.startTime > b.startTime) return 1;
        if (a.startTime === b.startTime) {
          if (a.name < b.name) return -1;
          if (a.name > b.name) return 1;
          if (a.name === b.name) return 0;
        }
      }
    });
  }

  return events;
}

function filterEventFields(events) {
  events.forEach(event => {
    delete event.displayOrder;
    delete event.startTime;
  });
  return events;
}

/**
 * Promise that adds market counts to events
 * @param events
 * @returns {Promise}
 */
function addMarketsCount(events) {
  return new Promise((resolve, reject) => {
    if (events.length) {
      const eventIds = events.map(event => event.id);

      getMarketsCountByEventIds(eventIds.join(','))
        .then(
          counts => {
            events.forEach(event => {
              event.marketCount = counts[event.id];
            });
            resolve(events);
          },
          reject
        );
    } else {
      resolve(events);
    }
  });
}

/**
 *
 * @param typeIds
 * @returns {Promise}
 */
function getCategoriesByTypeIds(typeIds) {
  return siteServerAPI.getClassToSubTypeForType(typeIds)
    .then(response => response.SSResponse.children)
    .then(data => {
      const classes = data.filter(value => value.class),
        errors = data.filter(value => value.error);

      if (errors.length) {
        return Promise.reject(errors);
      }
      return classes;
    })
    .then(classes => {
      const categories = {};
      classes.forEach(item => {
        categories[item.class.categoryId] = item.class.categoryCode;
      });

      return Object.keys(categories).map(categoryId => ({ categoryId, categoryCode: categories[categoryId] }));
    });
}

/**
 *
 * @param categoryId
 * @returns {Promise}
 */
function getTypeIdsByCategoryId(categoryId) {
  return siteServerAPI.getClassToSubType({ classCategoryIdEquals: categoryId })
    .then(response => response.SSResponse.children)
    .then(data => {
      const classes = data.filter(value => value.class && value.class.children),
        errors = data.filter(value => value.error);

      if (errors.length) {
        return Promise.reject(errors);
      }
      return classes;
    })
    .then(classes => classes.map(item => item.class.children.map(child => child.type.id)))
    .then(data => data.reduce((result, types) => result.concat(types), []));
}

/**
 *
 * @param categoryId
 * @returns {Promise}
 */
function getTypeIdsAndCategoryByCategoryId(categoryId) {
  return siteServerAPI.getClassToSubType({ classCategoryIdEquals: categoryId })
    .then(response => response.SSResponse.children)
    .then(data => {
      const classes = data.filter(value => value.class && value.class.children),
        errors = data.filter(value => value.error);

      if (errors.length) {
        return Promise.reject(errors);
      }
      return classes;
    })
    .then(classes => {
      return {
        categoryCode: classes[0].class.categoryCode,
        typeIds: classes.map(item => item.class.children.map(child => child.type.id))
      };
    })
    .then(data => {
      return {
        categoryCode: data.categoryCode,
        typeIds: data.typeIds.reduce((result, types) => result.concat(types), [])
      };
    });
}

module.exports = {
  getByRaceType: getEventsByRaceType,
  getByType: getOutrightsAndEventsByType,
  getBySelection: getOutcomeByOutcome,
  getByEnhancedMultiples: getEventsByType,
  getMarketsCountByEventIds,
  getEvents,
  getCategoriesByTypeIds,
  getTypeIdsByCategoryId,
  getTypeIdsAndCategoryByCategoryId,
  getEventsByTypeAndMarket,
  getClassToSubTypeForType
};
