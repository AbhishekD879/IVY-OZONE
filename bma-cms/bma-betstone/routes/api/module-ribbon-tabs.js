var keystone = require('../../'),
  ModuleRibbonTabs = require('../../../models/ModuleRibbonTabs'),
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
      Logger.info('MODULE_RIBBON', msg + (err ? ':' : ''));
      if (err) {
        Logger.error('MODULE_RIBBON', err);
      }
      res.status(500);
      sendResponse({ error: key || 'error', detail: err ? err.message : '' });
    };

    switch ( req.method ) {
      case 'GET':
        var resultArr = [];
        keystone.mongoose.model('ModuleRibbonTabs').find(function (err, moduleRibbonTabs) {
          if(err) sendError(err);
          moduleRibbonTabs.forEach(function(item, key) {
            resultArr[key] = {};
            resultArr[key].title = item.title;
            resultArr[key].targetUri = item.targetUri;
            resultArr[key].visible = item.visible;
            resultArr[key].sortBy = item.sortBy;
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
