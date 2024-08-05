const Config = require('../../models/ModulesConfigsCollection'),
  initialDataManager = require('../../lib/api/initialDataManager');

exports = module.exports = function(req, res) {
  if (req.user) {
    const brand = req.body.brand;
    console.info('[%s] [INFO] %s', 'api.setConfig', JSON.stringify(req.body));
    Config.findOne({ brand }).exec()
      .then(doc => {
        doc.config = req.body.config;
        return doc;
      })
      .then(doc => {
        return new Promise((resolve, reject) => {
          doc.save((err, val) => {
            if (err) {
              console.error('[%s] [INFO] %s', 'api.setConfig', JSON.stringify(err.stack));
              reject(err);
            } else {
              initialDataManager.regenCache(brand);
              resolve(val);
            }
          });
        });
      })
      .then(
        () => {
          res.status(200);
          res.end();
        },
        err => {
          console.error('[%s] [INFO] %s', 'api.setConfig', JSON.stringify(err.stack));
          res.status(500);
          res.end(err);
        }
      );
  } else {
    res.redirect('/keystone');
  }
};
