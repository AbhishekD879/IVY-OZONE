'use strict';

const path = require('path'),
  _ = require('underscore'),
  im = require('imagemin'),
  imageminMozjpeg = require('imagemin-mozjpeg'),
  imageminOptipng = require('imagemin-optipng'),
  Logger = require('./logger');

/**
 * Imagemin constructor
 *
 * @constructor
 * @this {Imagemin}
 */
function Imagemin() {
  this.config = {
    enabled: false,
    jpeg: {
      quality: 95
    },
    png: {
      optimizationLevel: 3
    }
  };
}

/**
 * Set imagemin custom config
 * @param {object} [config]
 */
Imagemin.prototype.setConfig = function(config) {
  if (_.isObject(config)) {
    this.config = _.defaults(config, this.config);
  }
};

/**
 * Callback of image minimization method
 *
 * @callback minCallback
 * @param {Error} err - error
 * @param {string} destination - result filename
 */

/**
 * minimize image file size
 * @param {string} sourceFile – src image
 * @param {string} [destination] - directory to save minimized image
 * @param {minCallback} callback - callback method
 */
Imagemin.prototype.min = function(sourceFile, destination, callback) {
  const filename = path.basename(sourceFile);

  /* eslint-disable */
  if (_.isUndefined(callback)) {
    callback = _.values(arguments).pop();
    destination = path.dirname(sourceFile);
  }
  /* eslint-enable */

  if (this.config.enabled) {
    im([sourceFile], destination, {
      plugins: [
        imageminMozjpeg({ progressive: true }),
        imageminOptipng({ optimizationLevel: this.config.png.optimizationLevel })
      ]
    })
      .then(files => {
        Logger.info('IMAGEMIN', 'image optimized', path.join(destination, filename));
        callback(null, path.join(destination, filename));
      })
      .catch(err => {
        Logger.error('IMAGEMIN', err);
        callback(err, null);
      });
  } else {
    callback(null, sourceFile);
  }
};

module.exports = new Imagemin();
