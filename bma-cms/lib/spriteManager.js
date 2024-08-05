'use strict';

const fs = require('fs'),
  path = require('path'),
  utils = require('./utils'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  akamai = require('../bma-betstone/lib/akamai');

/**
 * SpriteManager constructor
 */
function SpriteManager() {
  this.config = {
    akamaiDest: 'images/uploads'
  };
}

/**
 * method to generate corresponding sizes for images
 * @param {Object} item
 * @param {String} field
 * @returns {*|promise}
 */
SpriteManager.prototype.createSizes = function(item, field) {
  return new Promise((resolve, reject) => {
    const
      self = this,
      sizes = ['medium', 'small', 'large'],
      ffield = field[0].toUpperCase() + field.substr(1),
      ext = (field === 'filename') ? '' : ffield,
      tasks = [];

    for (let i = 0; i < sizes.length; i++) {
      const size = sizes[i],
        ssize = size[0].toUpperCase() + size.substr(1),
        width = item[`width${ssize}${ext}`],
        height = item[`height${ssize}${ext}`],
        file = item[field];

      if (file && file.filename) {
        const destination = path.join(
          file.path,
          item.collectionType,
          size + (ext ? `_${field}` : ''),
          item.spriteClass + path.extname(file.filename)
        );
        item[`uri${ssize}${ext}`] = destination;

        tasks.push(new Promise((resolve, reject) => { // eslint-disable-line no-shadow
          thumbnailGenerator.generateThumb(
            path.join(file.path, file.filename),
            { width, height, destination },
            (err, result) => {
              if (err) {
                reject(err);
              } else {
                self.uploadToAkamai(
                  item.brand,
                  [destination],
                  path.join(
                    self.config.akamaiDest,
                    item.collectionType,
                    size + (ext ? '_' + field : '') // eslint-disable-line prefer-template
                  )
                );
                resolve(result);
              }
            }
          );
        }));
      }
    }
    if (tasks.length > 0) {
      Promise.all(tasks)
        .then(() => resolve(true))
        .catch(reject);
    } else {
      resolve(true);
    }
  });
};

/**
 * method to remove corresponding sizes for images
 * @param {Object} item
 * @param {String} field
 * @returns {Promise}
 */
SpriteManager.prototype.removeSizes = function(item, field) {
  const sizes = ['medium', 'small', 'large'],
    ffield = field[0].toUpperCase() + field.substr(1),
    ext = (field === 'filename') ? '' : ffield,
    files = [];

  for (let i = 0; i < sizes.length; i++) {
    const size = sizes[i],
      ssize = size[0].toUpperCase() + size.substr(1);

    if (item[`uri${ssize}${ext}`]) {
      files.push(item[`uri${ssize}${ext}`]);
      item[`uri${ssize}${ext}`] = '';
    }
  }

  return utils.removeFiles(files);
};

/**
 * upload files to akamai and purge cache
 * @param {String} brand
 * @param {Array} filesArr
 * @param {String} akamaiDest
 * @returns {*|promise}
 */
SpriteManager.prototype.uploadToAkamai = function(brand, filesArr, akamaiDest = this.config.akamaiDest) {
  /**
   * promise for uploading 1 file to Akamai
   * @param {String} file
   * @param {String} filepath
   * @returns {Promise}
   */
  function uploadFile(file, filepath) {
    return new Promise((resolve, reject) => {
      const stream = fs.createReadStream(file);

      akamai.upload(brand, stream, filepath, err => {
        if (!err) {
          resolve(filepath);
        } else {
          reject(err);
        }
      });
    });
  }

  /**
   * Upload Files
   * @param {Array} files
   * @returns {Promise}
   */
  function uploadFiles(files) {
    return Promise.all(
      files.map(
        file => uploadFile(file, path.join(akamaiDest, path.basename(file)))
      )
    );
  }

  /**
   * purge cache for files list
   * @param {Array} files
   * @returns {Promise}
   */
  function forceCache(files) {
    return new Promise((resolve, reject) => {
      akamai.forceCache(brand, files, (err, data) => {
        if (err) {
          reject(err);
        } else {
          resolve(data);
        }
      });
    });
  }

  const pngFiles = filesArr.filter(file => path.extname(file) === '.png');

  return uploadFiles.bind(this)(pngFiles)
    .then(forceCache);
};

exports = module.exports = new SpriteManager();
