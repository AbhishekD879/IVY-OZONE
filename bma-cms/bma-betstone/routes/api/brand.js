var keystone = require('../../'),
  Brand = require('../../../models/Brand'),
  Logger = require('../../../lib/logger');

exports = module.exports = function(req, res) {

  if(req.session.userId) {

    var sendResponse = function(status) {
      res.json(status);
    };

    var sendError = function(key, err, msg) {
      msg = msg || 'API Error';
      key = key || 'unknown error';
      msg += ' (' + key + ')';
      Logger.info('BRAND', msg + (err ? ':' : ''));
      if (err) {
        Logger.error('BRAND', err);
      }
      res.status(500);
      sendResponse({ error: key || 'error', detail: err ? err.message : '' });
    };

    switch ( req.method ) {

      case 'GET':
        var resultArr = [];
        keystone.mongoose.model('brand').find(function (err, brandList) {
          if(err) sendError(err);
          brandList.forEach(function(item) {
            resultArr.push({
              title     : item.title,
              disabled  : item.disabled,
              code      : item.brandCode
            });
          });
          sendResponse( resultArr );
        });
        break;

      default:
        return res.redirect("/keystone");
        break;
    }
  }

};
