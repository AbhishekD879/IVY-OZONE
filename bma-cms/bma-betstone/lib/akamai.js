var akamaiAPI = require('akamai-http-api'),
  akamai = Object.create(akamaiAPI),
  path = require('path'),
  _ = require('underscore'),
  request = require('request'),
  url = require('url'),
  urljoin = require('url-join'),
  writeToLogsModel = require('../../lib/writeInLogsModel'),
  fs = require('fs-extra'),
  newrelic = require('newrelic');
  Logger = require('../../lib/logger');


/**
 * 
 * @param config
 */
akamai.setConfig = function (config) {
  config = _.extend({}, {
    ssl: true,
    verbose: true,
    brands: {}
  }, config);
  akamaiAPI.setConfig.call(this, config);
};

/**
 * set brand specific akamai config
 * @param {String} brand
 * @param {Object} config
 */
akamai.setBrandConfig = function (brand, config) {
  if (brand !== '' && config.hasOwnProperty('path') && config.path !== '' && config.hasOwnProperty('url') && config.url !== '') {
    this.config.brands[brand] = {
      url: config.url,
      path: config.path
    };
  }
};

akamai.getBrandedConfig = function (brand) {
  var config = _.clone(this.config);

  if (brand && config.brands.hasOwnProperty(brand)) {
    config.path = config.brands[brand].path;
    config.url = config.brands[brand].url;
  }

  return config;
};

/**
 * upload file to Akamai CDN
 * @param {ReadStream} stream
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.upload = function (brand, stream, filepath, callback) {
  const config = this.getBrandedConfig(brand);
  const self = this;

  if(!process.env.AKAMAI_DISABLED) {
    const transaction = newrelic.createWebTransaction(`/Akamai/Upload`, () => {
      Logger.info('AKAMAI', 'Upload to akamai started newrelic integration is done');
      uploadToAkamai(config.path);
      newrelic.endTransaction();
    });
    transaction();
  } else {
    Logger.error('AKAMAI', 'Akamai disabled', 'File wasn\'t uploaded:', filepath);
    saveImageInCMSfolder();
    callback(null, null, urljoin(config.url, filepath));
  }

  // As a temporary solution for a need to keep 'retail' brand,
  // this code duplicates images uploaded for 'connect' brand into the 'retail' akamai folder.
  if (brand === 'connect' && filepath.match(/\.(jpe?g|png|gif|bmp)$/i)) {
    uploadToAkamai(this.getBrandedConfig('retail').path, true);
  }

  function saveImageInCMSfolder() {
    if(filepath.match(/\.(jpe?g|png|gif|bmp)$/i)) {
      fs.move(stream.path, 'public/'+filepath, function(err) {
        if(err) {
          Logger.error('CMS FOLDER', 'File wasn\'t uploaded:', 'public/'+filepath, err);
        }
      });
    }
  }

  function uploadToAkamai(configPath, secondUpload) {
    akamaiAPI.upload.call(self, stream, path.join(configPath, filepath), function (err, data) {
      if (err) {
        Logger.error('AKAMAI', 'File wasn\'t uploaded:', filepath, err, 'data:', data, '[STREAM]', JSON.stringify(stream) );
        newrelic.noticeError(err);
      } else {
        Logger.info('AKAMAI', 'File uploaded:', filepath, data, '[STREAM]', JSON.stringify(stream) );
      }

      if (!secondUpload) {
        callback(err, data, urljoin(config.url, filepath));
      }
    });
  }

};

/**
 * download file from Akamai CDN
 * @param {String} remotePath
 * @param {WriteStream} stream
 * @param {Function} callback
 */
akamai.download = function (brand, remotePath, stream, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.download.call(this, path.join(config.path, filepath), stream, callback);
};

/**
 * change modify time
 * @param {String} filepath
 * @param {Date} date
 * @param {Function} callback
 */
akamai.mtime = function (brand, filepath, date, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.mtime.call(this, path.join(config.path, filepath), date, callback);
};

/**
 * get du-info of folder
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.du = function (brand, filepath, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.du.call(this, path.join(config.path, filepath), callback);
};

/**
 * get directory content
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.dir = function (brand, filepath, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.dir.call(this, path.join(config.path, filepath), callback);
};

/**
 * get stat of item
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.stat = function (brand, filepath, callback) {
  if (arguments.length === 3) {
    const config = this.getBrandedConfig(brand);
    akamaiAPI.stat.call(this, path.join(config.path, filepath), callback);  
  } else {
    // shift arguments
    var f = brand;
    var cb = filepath;
    akamaiAPI.stat.call(this, f, cb);
  }
};

/**
 * delete an item from Akamai CDN
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.delete = function (brand, filepath, callback) {
  Logger.info('AKAMAI', `File deleted: ${filepath}`);
  const config = this.getBrandedConfig(brand);
  akamaiAPI.delete.call(this, path.join(config.path, filepath), err => {
    if (!err || err.code === 404) {
      callback();
    } else {
      callback(err);
    }
  });
};

/**
 * Delete items from Akamai, reset model fields
 * @param {Object} model - keystone model
 * @param {Array} akamaiFields - fields with Akamai paths
 * @returns {Promise.<*>}
 * Consult models/FooterLogos.js for optimal usage.
 */
akamai.deleteModelFields = function (model, akamaiFields) {
  return Promise.all(
    akamaiFields.map(akamaiField => {
      if (model[akamaiField]) {
        return new Promise((resolve, reject) => {
          akamai.delete(model.brand, model[akamaiField], err => {
            if (err) {
              reject(err);
            } else {
              model[akamaiField] = '';
              resolve();
            }
          })
        })
      } else {
        return Promise.resolve();
      }
    })
  )
};

/**
 * create a directory on Akamai CDN
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.mkdir = function (brand, filepath, callback) {
  
  const config = this.getBrandedConfig(brand);
  akamaiAPI.mkdir.call(this, path.join(config.path, filepath), callback);
};

/**
 * remove dir from Akamai CDN
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.rmdir = function (brand, filepath, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.rmdir.call(this, path.join(config.path, filepath), callback);
};

/**
 * rename an item on Akamai CDN
 * @param {String} pathFrom
 * @param {String} pathTo
 * @param {Function} callback
 */
akamai.rename = function (brand, pathFrom, pathTo, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.rename.call(this, path.join(config.path, pathFrom), path.join(config.path, pathTo), callback);
};

/**
 * create a symlink
 * @param {String} filepathTo
 * @param {String} filepathFrom
 * @param {Function} callback
 */
akamai.symlink = function (brand, filepathTo, filepathFrom, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.symlink.call(this, path.join(config.path, filepathTo), path.join(config.path, filepathFrom), callback);
};

/**
 * check if file exists
 * @param {String} filepath
 * @param {Function} callback
 */
akamai.fileExists = function (brand, filepath, callback) {
  const config = this.getBrandedConfig(brand);
  akamaiAPI.fileExists.call(this, path.join(config.path, filepath), callback);
};

/**
 * force clear cache for selected files
 * @param {Array} files
 * @param {Function} callback
 */
akamai.forceCache = function (brand, files, callback) {
  const config = this.getBrandedConfig(brand);

  var objects = [];

  _.each(files, function(file) {
    objects.push(urljoin(config.url, file));
    
    if (brand === 'bma' && process.env.AKAMAI_URL_2) {

      // Needed on PROD to force clear cache on synchronized Oxy folder, used by mobile apps.
      objects.push(urljoin(process.env.AKAMAI_URL_2, file))
    }
  });

  request({
    method: 'post',
    body: {objects: objects},
    json: true,
    url: 'https://api.ccu.akamai.com/ccu/v2/queues/default',
    auth: {
      user: config.cred_user,
      pass: config.cred_pass
    }
  }, function (err, res, body) {
    if (err) {
      callback(body, null);
      Logger.error('AKAMAI', 'Cache2 purging requested:', objects, 'Response: ', JSON.stringify(body), 'Error: ', JSON.stringify(err));
    } else if(body && body.purgeId) {
      writeToLogsModel(objects, body);
      Logger.info('AKAMAI', 'Cache2 purging requested:', objects, '\tpurgeId:', body.purgeId, '\testimatedSeconds: ', body.estimatedSeconds);
      callback(null, body);
    } else {
      callback(body, null);
    }
  });
};

module.exports = akamai;
