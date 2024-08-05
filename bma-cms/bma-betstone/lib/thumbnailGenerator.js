var os = require('os'),
  crypto = require('crypto'),
  path = require('path'),
  mkdirp = require('mkdirp'),
  lwip = require('lwip'),
  imagemin = require('../../lib/imagemin');

var thumbnailGenerator = Object.create(null);

/**
 * generate thumbnail of filename
 * @param {String} filename - source filename
 * @param {Object} options 
 *  {Number} width
 *  {Number} height
 *  {String} destination – optional
 *  {Bool} skipResize. If set to true, only optimization will be performed (no resizing)
 * @param {Function} callback - function (err, destination) which will be called after generation
 */
thumbnailGenerator.generateThumb = function (filename, options, callback) {
  var destination = options.hasOwnProperty('destination') ? options.destination : path.join(os.tmpdir(), rename(filename)) + path.extname(filename);

  mkdirp(path.dirname(destination), function (err) {
    if (err) {
      return callback(err);
    }

    lwip.open(filename, function (err, image) {
      if (err) {
        return callback(err);
      }

      if (options.skipResize) {
        image.writeFile(destination, function (err) {
          if (err) {
            callback(err);
          } else {
            imagemin.min(destination, callback);
          }
        });
      } else {
        image.batch()
          .resize(options.width, options.height)
          .writeFile(destination, function (err) {
            if (err) {
              callback(err);
            } else {
              imagemin.min(destination, callback);
            }
          });
      }
    });
  });
};

var rename = function(filename) {
  var random_string = filename + Date.now() + Math.random();
  return crypto.createHash('md5').update(random_string).digest('hex');
};

module.exports = thumbnailGenerator;
