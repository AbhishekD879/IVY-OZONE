'use strict';

const request = require('request'),
  urljoin = require('url-join'),
  filterBuilder = require('./filterBuilder'),
  Logger = require('../../lib/logger');

// TODO: add more informative comments

/**
 *
 * @constructor
 * @this {SiteServerAPI}
 */
function SiteServerAPI() {
  this.endpointURL = process.env.SITESERVER_URL;
}

/**
 *
 * @param url
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.request = function(url, params) {
  return new Promise((resolve, reject) => {
    const urlTemplate = `${urljoin(this.endpointURL, url)}?${filterBuilder(params)}`;
    Logger.info('SiteServer', `Requesting: ${urlTemplate}`);
    request({
      url: urlTemplate,
      json: true
    }, (err, response, body) => {
      if (err) {
        reject(err);
      } else {
        if (!body.SSResponse) {
          reject(new Error('no SSResponse'));
        } else if (!body.SSResponse.children || !body.SSResponse.children.length) {
          reject(new Error('empty SSResponse'));
        } else if (body.SSResponse.children[0].error) {
          reject(new Error(body.SSResponse.children[0].error.desc));
        } else {
          resolve(body);
        }
      }
    });
  });
};

/**
 *
 * @param eventIdSet
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.requestEventToMarketForEvent = function(eventIdSet, params) {
  return this.request(`EventToMarketForEvent/${eventIdSet}`, params);
};

/**
 *
 * @param typeIdSet
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.requestEventToOutcomeForType = function(typeIdSet, params) {
  return this.request(`EventToOutcomeForType/${typeIdSet}`, params);
};

/**
 *
 * @param outcomeIdSet
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.requestEventToOutcomeForOutcome = function(outcomeIdSet, params) {
  return this.request(`EventToOutcomeForOutcome/${outcomeIdSet}`, params);
};

/**
 *
 * @param typeIdSet
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.requestClassToSubTypeForType = function(typeIdSet, params) {
  return this.request(`ClassToSubTypeForType/${typeIdSet}`, params);
};

/**
 *
 * @param typeIdSet
 * @param params
 * @returns {Promise}
 */
SiteServerAPI.prototype.requestClassToSubType = function(params) {
  return this.request('ClassToSubType', params);
};

/**
 *
 * @param typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @param marketCode
 * @param marketNames
 * @returns {Promise}
 */
SiteServerAPI.prototype.getEventsByTypeAndMarket = function(typeId, from, to, marketCode, marketNames, customParams) {
  const currDate = new Date().toISOString(),
    params = {
      startTime: from,
      endTime: to,
      suspendAtTime: currDate,
      dispSortName: marketCode,
      isFinished: false,
      marketCollectionNamesIntersects: marketNames,
      translationLang: 'en',
      prune: ['event', 'market']
    };

  if (customParams) {
    const customParamsKeys = Object.keys(customParams);
    customParamsKeys.forEach(key => {
      params[key] = customParams[key];
    });
  }

  return this.requestEventToOutcomeForType(typeId, params);
};

/**
 *
 * @param {string} typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {Promise}
 */
SiteServerAPI.prototype.getEventsByType = function(typeId, from, to) {
  const currDate = new Date().toISOString();

  return this.requestEventToOutcomeForType(typeId, {
    startTime: from,
    endTime: to,
    isFinished: false,
    suspendAtTime: currDate,
    translationLang: 'en'
  });
};

/**
 *
 * @param {string} typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {Promise}
 */
SiteServerAPI.prototype.getEventsByRaceType = function(typeId, from, to) {
  const currDate = new Date().toISOString();

  return this.requestEventToOutcomeForType(typeId, {
    startTime: from,
    endTime: to,
    suspendAtTime: currDate,
    isFinished: false,
    marketCollectionNamesIntersects: 'Win or Each Way',
    translationLang: 'en',
    prune: ['event', 'market']
  });
};

/**
 *
 * @param {string} typeId
 * @param {string} from - date in ISO format
 * @param {string} to - date in ISO format
 * @returns {Promise}
 */
SiteServerAPI.prototype.getOutrights = function(typeId, from, to) {
  const currDate = new Date().toISOString();

  return this.requestEventToOutcomeForType(typeId, {
    startTime: from,
    endTime: to,
    suspendAtTime: currDate,
    isFinished: false,
    siteChannels: 'M',
    eventSortCode: 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,' +
      'TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20',
    translationLang: 'en',
    prune: ['event', 'market']
  });
};

/**
 *
 * @param {string} typeId
 * @returns {Promise}
 */
SiteServerAPI.prototype.getClassToSubTypeForType = function(typeId) {
  return this.requestClassToSubTypeForType(typeId);
};

/**
 *
 * @param {Object} params
 * @returns {Promise}
 */
SiteServerAPI.prototype.getClassToSubType = function(params) {
  return this.requestClassToSubType(params);
};

/**
 *
 * @param {string} outcomeId
 * @returns {Promise}
 */
SiteServerAPI.prototype.getOutcomeByOutcome = function(outcomeId) {
  return this.requestEventToOutcomeForOutcome(outcomeId, {
    translationLang: 'en'
  });
};

/**
 *
 * @param {string} eventIds
 * @returns {Promise}
 */
SiteServerAPI.prototype.getMarketsCountByEventIds = function(eventIds) {
  return this.requestEventToMarketForEvent(eventIds, {
    count: 'event:market'
  });
};

module.exports = new SiteServerAPI();
