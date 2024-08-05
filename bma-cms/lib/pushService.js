'use strict';

const EventEmitter = require('events'),
  util = require('util'),
  PubNub = require('pubnub'),
  Logger = require('./logger');

/**
 * Push Service Constructor
 * @constructor
 */
function PushService() {
  EventEmitter.call(this);

  this.pubnub = null;
}

util.inherits(PushService, EventEmitter);

/**
 * Init Push Service
 * @param {string} pubnubPublishKey - PubNub Publish Key
 * @param {string} pubnubSubscribeKey - PubNub Subscribe Key
 */
PushService.prototype.init = function(pubnubPublishKey, pubnubSubscribeKey) {
  this.pubnub = PubNub.init({
    ssl: true,
    publish_key: pubnubPublishKey,
    subscribe_key: pubnubSubscribeKey
  });
  Logger.info('PUSH', 'PubNub initialised');
};

/**
 * Push data to selected CMS channel
 * @param {string} channel - channel to push data to
 * @param {object} data - data to push
 * @returns {Promise}
 */
PushService.prototype.push = function(channel, data) {
  return new Promise((resolve, reject) => {
    if (this.pubnub) {
      this.pubnub.publish({
        channel: `cms_${channel}`,
        message: data,
        callback: m => {
          Logger.info('PUSH', m);
          if (m[0] === 1) {
            resolve(m);
          } else {
            reject(m);
          }
        }
      });
    } else {
      Logger.error('PUSH', 'PubNub is not initialised');
      reject('PubNub is not initialised');
    }
  });
};

module.exports = new PushService();
