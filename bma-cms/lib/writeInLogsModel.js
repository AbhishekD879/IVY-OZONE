'use strict';
let keystone;
const moment = require('moment'),
  Logger = require('./logger');

module.exports = function(domains, response) {
  keystone = keystone || require('../bma-betstone');
  const logsModel = keystone.list('dashboard'),
    files = JSON.stringify(domains),
    progressUrlSplited = response.progressUri.split('/');
  new logsModel.model({
    estimatedTime: response.estimatedSeconds,
    status: response.httpStatus,
    purgeID: response.purgeId,
    progressURI: `/api/purgeStatus/${progressUrlSplited[progressUrlSplited.length - 1]}`,
    supportID: response.supportId,
    type: `${files.substring(0, 200)}...`,
    domains: files,
    currentTime: moment().toDate()
  })
  .save(clearLogs);
};

function clearLogs() {
  keystone = keystone || require('../bma-betstone');
  const logsModel = keystone.list('dashboard'),
    lastWeek = moment().add(-7, 'days');
  logsModel.model.find()
      .where('currentTime')
      .lt(lastWeek.toDate())
      .exec()
      .then(logs => {
        Promise.all(logs.map(log => log.remove())).then(() => {
          Logger.info('DASHBOARD', 'Old logs were removed');
        }, Logger.error);
      });
}
