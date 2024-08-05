/*!
 * Module dependencies.
 */

var _ = require('underscore'),
  moment = require('moment'),
  keystone = require('../../../'),
  util = require('util'),
  utils = require('keystone-utils'),
  grappling = require('grappling-hook'),
  super_ = require('../Type'),
  akamai = require('../../../lib/akamai'),
  path = require('path');

/**
 * S3File FieldType Constructor
 * @extends Field
 * @api public
 */

function akamaifile(list, path, options) {
  grappling.mixin(this)
    .allowHooks('pre:upload');
  this._underscoreMethods = ['format', 'uploadFile'];
  this._fixedSize = 'full';

  // TODO: implement filtering, usage disabled for now
  options.nofilter = true;

  // TODO: implement initial form, usage disabled for now
  if (options.initial) {
    throw new Error('Invalid Configuration\n\n' +
      'Akamai fields (' + list.key + '.' + path + ') do not currently support being used as initial fields.\n');
  }

  akamaifile.super_.call(this, list, path, options);

  // validate akamai config (has to happen after super_.call)
  if (!this.akamaiconfig) {
    throw new Error('Invalid Configuration\n\n' +
      'Akamai fields (' + list.key + '.' + path + ') require the "akamai config" option to be set.\n');
  }

  // Could be more pre- hooks, just upload for now
  if (options.pre && options.pre.upload) {
    this.pre('upload', options.pre.upload);
  }

}

/*!
 * Inherit from Field
 */

util.inherits(akamaifile, super_);

/**
 * Exposes the custom or keystone s3 config settings
 */

Object.defineProperty(akamaifile.prototype, 'akamaiconfig', { get: function() {
  return this.options.akamaiconfig || keystone.get('akamai config');
}});


/**
 * Registers the field on the List's Mongoose Schema.
 *
 * @api public
 */

akamaifile.prototype.addToSchema = function() {

  var field = this,
    schema = this.list.schema;

  var paths = this.paths = {
    // fields
    filename:   this._path.append('.filename'),
    originalname: this._path.append('.originalname'),
    path:     this._path.append('.path'),
    size:     this._path.append('.size'),
    filetype:   this._path.append('.filetype'),
    // virtuals
    exists:     this._path.append('.exists'),
    upload:     this._path.append('_upload'),
    action:     this._path.append('_action')
  };

  var schemaPaths = this._path.addTo({}, {
    filename:   String,
    originalname: String,
    path:     String,
    size:     Number,
    filetype:   String
  });

  schema.add(schemaPaths);

  var exists = function(item) {
    return (item.get(paths.url) ? true : false);
  };

  // The .exists virtual indicates whether a file is stored
  schema.virtual(paths.exists).get(function() {
    return schemaMethods.exists.apply(this);
  });

  var reset = function(item) {
    item.set(field.path, {
      filename: '',
      originalname: '',
      path: '',
      size: 0,
      filetype: ''
    });
  };

  var schemaMethods = {
    exists: function() {
      return exists(this);
    },
    /**
     * Resets the value of the field
     *
     * @api public
     */
    reset: function() {
      var self = this,
        path = require('path');

      akamai.delete(this.get('brand'), path.join(this.get(paths.path), this.get(paths.filename)), function(err, data) {
        if (err) {
          throw err;
        }
      });
      reset(self);
    },
    /**
     * Deletes the file from Akamai and resets the field
     *
     * @api public
     */
    delete: function() {
      // TODO: find when it's called and implement 
      var self = this;
      var remoteFilePath = this.get(paths.path) + this.get(paths.filename);

      //console.log('delete', this);
    }
  };

  _.each(schemaMethods, function(fn, key) {
    field.underscoreMethod(key, fn);
  });

  // expose a method on the field to call schema methods
  this.apply = function(item, method) {
    return schemaMethods[method].apply(item, Array.prototype.slice.call(arguments, 2));
  };

  this.bindUnderscoreMethods();
};


/**
 * Formats the field value
 *
 * @api public
 */

akamaifile.prototype.format = function(item) {
  if (!item.get(this.paths.filename)) {
    return '';
  }
  if (this.hasFormatter()) {
    var file = item.get(this.path);
    file.href = this.href(item);
    return this.options.format.call(this, item, file);
  }
  return this.href(item);
};


/**
 * Detects the field have formatter function
 *
 * @api public
 */

akamaifile.prototype.hasFormatter = function() {
  return 'function' === typeof this.options.format;
};

/**
 * Return the public href for the stored file
 *
 * @api public
 */

akamaifile.prototype.href = function(item) {
  if (!item.get(this.paths.filename)) {
    return '';
  }
  var prefix = this.options.prefix ? this.options.prefix : item.get(this.paths.path);
  return path.join(prefix, item.get(this.paths.filename));
};

/**
 * Detects whether the field has been modified
 *
 * @api public
 */

akamaifile.prototype.isModified = function(item) {
  return item.isModified(this.paths.filename);
};


/**
 * Validates that a value for this field has been provided in a data object
 *
 * @api public
 */

akamaifile.prototype.validateInput = function(data) {
  // TODO - how should file field input be validated?
  return true;
};


/**
 * Updates the value for this field in the item from a data object
 *
 * @api public
 */

akamaifile.prototype.updateItem = function(item, data) {
  // TODO - direct updating of data (not via upload)
};


/**
 * Uploads the file for this field
 *
 * @api public
 */

akamaifile.prototype.uploadFile = function(item, file, update, callback) {

  var field = this,
    filepath = field.options.dest ? field.options.dest : '',
    prefix = field.options.datePrefix ? moment().format(field.options.datePrefix) + '-' : '',
    filename = prefix + file.name,
    filetype = file.mimetype || file.type;

  if ('function' === typeof update) {
    callback = update;
    update = false;
  }

  if (field.options.allowedTypes && !_.contains(field.options.allowedTypes, filetype)) {
    return callback(new Error('Unsupported File Type: ' + filetype));
  }

  var doUpload = function() {
    if ('function' === typeof field.options.filename) {
      filename = field.options.filename(item, filename);
    }

    var fs = require('fs'),
      path = require('path');
    var stream = fs.createReadStream(file.path);
    akamai.upload(item.get('brand'), stream, path.join(filepath, filename), function(err, data) {
      if (err) {
        return callback(err);
      } else {
        var fileData = {
          filename: filename,
          originalName: file.originalName,
          path: filepath,
          size: file.size,
          filetype: filetype
        };

        if (update) {
          item.set(field.path, fileData);
        }

        callback(null, fileData);
      }
      
    });
  };

  this.callHook('pre:upload', [item, file, field.options], function(err) {
    if (err) return callback(err);
    doUpload();
  });

};


/**
 * Returns a callback that handles a standard form submission for the field
 *
 * Expected form parts are
 * - `field.paths.action` in `req.body` (`clear` or `delete`)
 * - `field.paths.upload` in `req.files` (uploads the file to akamaifile)
 *
 * @api public
 */

akamaifile.prototype.getRequestHandler = function(item, req, paths, callback) {

  var field = this;

  if (utils.isFunction(paths)) {
    callback = paths;
    paths = field.paths;
  } else if (!paths) {
    paths = field.paths;
  }

  callback = callback || function() {};

  return function() {
    if (req.body) {
      var action = req.body[paths.action];

      if (/^(delete|reset)$/.test(action)) {
        field.apply(item, action);
      }
    }

    if (req.files && req.files[paths.upload] && req.files[paths.upload].size) {
      return field.uploadFile(item, req.files[paths.upload], true, callback);
    }

    return callback();

  };

};


/**
 * Immediately handles a standard form submission for the field (see `getRequestHandler()`)
 *
 * @api public
 */

akamaifile.prototype.handleRequest = function(item, req, paths, callback) {
  this.getRequestHandler(item, req, paths, callback)();
};


/*!
 * Export class
 */

exports = module.exports = akamaifile;
