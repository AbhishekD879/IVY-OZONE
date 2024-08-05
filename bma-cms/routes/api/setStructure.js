const Structure = require('../../models/ModulesStructuresCollection'),
  Config = require('../../models/ModulesConfigsCollection'),
  async = require('async'),
  fs = require('fs'),
  path = require('path'),
  _ = require('underscore'),
  akamai = require('../../bma-betstone/lib/akamai'),
  uploadsDir = '/images/uploads/structure',
  utils = require('../../lib/utils.js'),
  initialDataManager = require('../../lib/api/initialDataManager'),
  Logger = require('../../lib/logger');

exports = module.exports = (req, res) => {
  if (req.user) {
    const brand = req.body.data.structure.brand;
    console.error('[%s] [INFO] %s', 'api.setStructure', JSON.stringify(req.body.data.structure));
    _getConfig(brand)
      .then(config => restoreDataTypes(config, req.body.data.structure))
      .then(newModel => doSet(req, newModel))
      .then(
        results => {
          initialDataManager.regenCache(brand);
          return successCallback(req, res, results);
        },
        err => {
          console.error('[%s] [ERROR] %s', 'api.setStructure', JSON.stringify(err.stack));
          res.status(500).send(err);
        }
      );
  } else {
    res.redirect('/keystone');
  }
};

function _getConfig(brand) {
  return Config.findOne({ brand }).exec();
}

/*
 Convert 'true', 'false' to Boolean if type 'checkbox'.
 Conversion is needed because multipart/form-data request supports only strings.
*/
function restoreDataTypes(config, model) {
  _.forEach(config.config, (fieldSet, key) => {
    _.forEach(fieldSet, field => {
      model.structure[key][field.name] = (field.type === 'checkbox')
        ? model.structure[key][field.name] === 'true'
        : model.structure[key][field.name];
    });
  });
  return model;
}

function doSet(req, newModel) {
  return new Promise((resolve, reject) => {
    Structure.findOne({ lang: newModel.lang ? newModel.lang : 'en', brand: newModel.brand }, (findErr, doc) => {
      if (findErr) {
        console.error('[%s] [ERROR] %s', 'api.setStructure', JSON.stringify(findErr.stack));
        reject(findErr);
      } else {
        async.waterfall([
          function(callback) {
            if (req.files) {
              // some files were uploaded
              changeFiles(req.files, newModel.brand, doc.structure, newModel.structure, callback);
            } else {
              callback(null, newModel.structure, null);
            }
          },
          function(newStructure, callback) {
            doc.structure = newStructure;

            doc.save(error => {
              if (error) {
                callback(error, null);
              } else {
                const apiManager = require('../../lib/api');

                apiManager.run('systemConfiguration', { brand: doc.brand });
                callback(null, newStructure);
              }
            });
          }
        ], (err, results) => {
          if (err) {
            console.error('[%s] [ERROR] %s', 'api.setStructure', JSON.stringify(err.stack));
            reject(err);
          } else {
            resolve(results);
          }
        });
      }
    });
  });
}

function successCallback(req, res, results) {
  Logger.info(
    'AKAMAI',
    'system-configuration user',
    req.user.email,
    req.headers['x-forwarded-for'] || req.connection.remoteAddress || req.socket.remoteAddress ||
      req.connection.socket.remoteAddress
  );
  res.json(results).status(200);
  res.end();
}

function changeFiles(reqFiles, brand, oldStructure, newStructure, mainCallback) {
  const files = _.values(reqFiles);
  _getConfig(brand)
    .then(config => {
      async.mapSeries(files, getFileHandler.bind(null, brand, config, oldStructure), (err, structureMappers) => {
        if (err) {
          console.error('[%s] [ERROR] %s', 'api.setStructure', JSON.stringify(err.stack));
          mainCallback(err, null);
        } else {
          for (let i = 0; i < structureMappers.length; i++) {
            const structureMapper = structureMappers[i];
            structureMapper(newStructure);
          }
          mainCallback(null, newStructure);
        }
      });
    })
    .catch(err => mainCallback(err, null));
}

/**
 * Choose file handler based on Field type.
 * @param brand {String}
 * @param config {Object}
 * @param oldStructure {Object}
 * @param file {File}
 * @param mapCallback {Function}. This callback should be passed a callback, what accepts
 * and modifies Structure.
 */
function getFileHandler(brand, config, oldStructure, file, mapCallback) {
  const fieldname = file.fieldname.split('-'),
    key = fieldname[0],
    name = fieldname[1];

  const fieldConfig = _.find(config.config[key], fieldset => fieldset.name === name);
  if (fieldConfig.type === 'svg') {
    handleSvgChange(file, mapCallback);
  } else {
    handleImageChange(brand, oldStructure, file, mapCallback);
  }
}

// SVG file is validated, transformed into { symbol, id } and saved into structure.
function handleSvgChange(file, mapCallback) {
  const fieldname = file.fieldname.split('-'),
    key = fieldname[0],
    name = fieldname[1];

  fs.readFile(file.path, 'utf8', (error, data) => {
    if (error) {
      Logger.error('SVG', 'System configuration save error: SVG file not found');
      mapCallback(error, null);
    } else {
      utils.validateSvg(data)
        .catch(err => {
          Logger.error('SVG', 'System configuration save error: Invalid SVG file');
          mapCallback(err, null);
        })
        .then(() => mapCallback(null, structure => {
          structure[key][name] = Object.assign(structure[key][name], utils.processSvg(data));
        }));
    }
  });
}

// Regular file is uploaded to Akamai, path saved into structure
function handleImageChange(brand, oldStructure, file, mapCallback) {
  const fieldname = file.fieldname.split('-'),
    key = fieldname[0],
    name = fieldname[1],
    newFilename = path.join(uploadsDir, file.name);
  // move new file to uploads
  // remove old uploaded file
  async.series([
    function(callback) {
      const stream = fs.createReadStream(file.path);
      akamai.upload(brand, stream, newFilename, callback);
    },
    function(callback) {
      // if value not new
      if (oldStructure[key] && oldStructure[key][name]) {
        const oldFilename = oldStructure[key][name];

        akamai.fileExists(brand, oldFilename, (err, exists) => {
          if (err) {
            callback(err);
          } else {
            if (exists) {
              akamai.delete(brand, oldFilename, callback);
            } else {
              callback(null);
            }
          }
        });
      } else {
        callback(null);
      }
    }
  ], err => {
    if (err) {
      mapCallback(err, null);
    } else {
      mapCallback(null, structure => {
        structure[key][name] = newFilename;
      });
    }
  });
}
