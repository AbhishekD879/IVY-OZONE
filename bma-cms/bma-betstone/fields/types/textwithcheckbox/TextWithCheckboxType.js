/*!
 * Module dependencies.
 */

var _ = require('underscore'),
  util = require('util'),
	super_ = require('../Type');

/**
 * Text FieldType Constructor
 * @extends Field
 * @api public
 */

function textwithcheckbox(list, path, options) {

  this._fixedSize = 'full';
  options.nosort = true;
  options.nofilter = true;

  if (!options.defaults) {
    options.defaults = {};
  }
  
  textwithcheckbox.super_.call(this, list, path, options);
}

/*!
 * Inherit from Field
 */

util.inherits(textwithcheckbox, super_);

/**
 * Registers the field on the List's Mongoose Schema.
 *
 * Adds ...
 *
 * @api public
 */
textwithcheckbox.prototype.addToSchema = function() {
  
  var field = this,
      schema = this.list.schema,
      options = this.options;

  this.paths = {
    tablabel:   this._path.append('.tablabel'),
    visible: 		this._path.append('.visible')
  };

  var getFieldDef = (type, key)  =>  ({
    type: type,
    default: (options.default && options.default[key] !== undefined) ? options.default[key] : undefined
  });
  
  schema.nested[this.path] = true;
  schema.add({
    tablabel:   getFieldDef(String, 'tabLabel'),
    visible: 	  getFieldDef(Boolean, 'visible')
  }, this.path + '.');
  
  schema.pre('save', function(next) {
    
    this.set(field.path, {
      tablabel: this[field.path].tablabel,
      visible: this[field.path].visible
    });
    
    return next();

  });
  
  this.bindUnderscoreMethods();
};


/**
 * Detects whether the field has been modified
 *
 * @api public
 */

textwithcheckbox.prototype.isModified = function(item) {
  return item.isModified(this.paths.tablabel) || item.isModified(this.paths.visible);
};

/**
 * Checks if tab label is not empty
 *
 * @api public
 */

textwithcheckbox.prototype.validateInput = function(data, required, item) {

  return !required || data[this.path + '.' + 'tablabel'] !== '';

};

/**
 * Updates the value for this field in the item from a data object
 *
 * @api public
 */

textwithcheckbox.prototype.updateItem = function(item, data) {
  var obj = {};
  if(data[this.path + '.' + 'tablabel']) {
    obj['tablabel'] = data[this.path + '.' + 'tablabel'];
  } else {
    obj['tablabel'] = '';  
  }
  
  if(data[this.path + '.' + 'visible']) {
    obj['visible'] = data[this.path + '.' + 'visible'] === 'true';
  } else {
    obj['visible'] = false;
  }

  item.set(this.path, obj);
  
};

exports = module.exports = textwithcheckbox;
