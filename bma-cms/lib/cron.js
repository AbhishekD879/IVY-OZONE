const cron = require('node-cron'),
  updateModules = require('./siteServer/update-modules'),
  Logger = require('./logger');

Logger.info('CRON', 'cron initialised');

// run every hour in 00 minutes
cron.schedule('0 * * * *', () => {
  updateModules()
    .then(() => {
      Logger.info('CRON', 'Update modules cron job success');
    })
    .catch(err => {
      Logger.error('CRON', err);
    });
}, true);
