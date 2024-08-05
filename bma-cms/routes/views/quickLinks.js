const keystone = require('../../bma-betstone'),
  Logger = require('../../lib/logger');

exports = module.exports = function(req, res) {
  // Load the Quick Link model
  keystone.list('quickLink')
    .model.find()
    .where('validityPeriodStart')// .lte(new Date())
    .where('validityPeriodEnd')// .gt(new Date().setDate(new Date().getDate() - 1))
    .sort('sortOrder')
    .exec()
    .then(quickLinks => {
      if (quickLinks !== null) {
        const resultArr = { collapsed: false, quick_links: [] };
        quickLinks.forEach((item, key) => {
          resultArr.quick_links[key] = {};
          resultArr.quick_links[key].title = item.title;
          resultArr.quick_links[key].validityPeriodStart = Date.parse(item.validityPeriodStart);
          resultArr.quick_links[key].validityPeriodEnd = Date.parse(item.validityPeriodEnd);
          resultArr.quick_links[key].url = item.url;
        });
        res.apiResponse(resultArr);
      } else {
        res.apiResponse([]);
      }
    }, err => { // first promise rejected
      res.apiError('error', err);
      // ToDo: Need cases to handle error response.
      Logger.error('QUICK_LINKS', err);
    });
};

