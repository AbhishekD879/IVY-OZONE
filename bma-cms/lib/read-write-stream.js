const util = require('util'),
  Transform = require('stream').Transform;

util.inherits(ReadWriteStream, Transform);

function ReadWriteStream(options) {
  if (!(this instanceof ReadWriteStream)) {
    return new ReadWriteStream(options);
  }

  Transform.call(this, options);
}

ReadWriteStream.prototype._transform = function(data, encoding, callback) {
  callback(null, data);
};

module.exports = ReadWriteStream;
