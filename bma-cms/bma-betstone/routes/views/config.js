var keystone = require('../../'),
    Config = require('../../../models/ModulesConfigsCollection'),
    configJSON = require('../config.json');

exports = module.exports = function(req, res, next) {

  function keystoneRender(data){
    keystone.render(req, res, 'config', {
      config: data
    });
  }

  function createConfigModel(brand) {
    var config = new Config(configJSON);
    config.brand = brand;

    return new Promise((resolve, reject) => {
      config.save((err, configVal) => {
        if (err) {
          reject(err);
        } else {
          resolve(configVal);
        }
      });
    });
  }

  if (req.user) {
    const brand = req.user.brandCode;

    Config.findOne({ brand: brand }).exec()
      .then(value => value ? value : createConfigModel(brand))
      .then(keystoneRender, next);

  } else {
    return res.redirect("/keystone");
  }

};
