var keystone = require('../../'),
  Structure = require('../../../models/ModulesStructuresCollection'),
  Config = require('../../../models/ModulesConfigsCollection'),
  structureJSON = require('../structure.json');

exports = module.exports = function(req, res, next) {

  function keystoneRender(data) {
    keystone.render(req, res, 'structure', {
      data: data
    });
  }

  function setMainProps(obj, brand, lang) {
    obj.brand = brand;
    obj.lang = lang;
    return obj;
  }

  function setNewStructure(brand, lang, configValue) {
    var structure = new Structure(setMainProps(structureJSON, brand, lang));

    return new Promise((resolve, reject) => {
      structure.save((err, structureValue) => {
        if (err) {
          reject(err);
        } else {
          resolve([configValue, structureValue]);
        }
      });
    });
  }

  function renderTemplate(configValue, structureValue) {
    keystoneRender({config: configValue, structure: structureValue});
  }

  if (req.user) {
    const brand = req.user.brandCode;
    const lang = 'en';

    Promise.all([
      Config.findOne({ brand: brand }).exec(),
      Structure.findOne({ brand: brand, lang: lang }).exec()
    ])
      .then(data => data[1] ? data : setNewStructure(brand, lang, data[0]))
      .then(data => renderTemplate(data[0], data[1]))
      .catch(next);

  } else {
    return res.redirect("/keystone");
  }
};
