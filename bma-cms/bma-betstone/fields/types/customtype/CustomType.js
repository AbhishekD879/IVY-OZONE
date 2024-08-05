/*!
 * Module dependencies.
 */

var util = require('util'),
	numeral = require('numeral'),
	utils = require('keystone-utils'),
	super_ = require('../Type');

/**
 * Custom FieldType Constructor
 * @extends Field
 * @api public
 */

function custom(list, path, options) {

	this._nativeType = Number;
	this._underscoreMethods = ['format'];
	this._fixedSize = 'small';
	this._formatString = (options.format === false) ? false : (options.format || '$0,0.00');

	if (this._formatString && 'string' !== typeof this._formatString) {
		throw new Error('FieldType.custom: options.format must be a string.');
	}

	custom.super_.call(this, list, path, options);

}

/*!
 * Inherit from Field
 */

util.inherits(custom, super_);


/**
 * Formats the field value
 *
 * @api public
 */

custom.prototype.format = function(item, format) {
	return item.get(this.path) || '';

};


/**
 * Checks that a valid number has been provided in a data object
 *
 * An empty value clears the stored value and is considered valid
 *
 * @api public
 */

custom.prototype.validateInput = function(data, required, item) {

	if (!(this.path in data) && item && (item.get(this.path) || item.get(this.path) === 0)) return true;

	if (data[this.path]) {
		var newValue = utils.number(data[this.path]);
		return (!isNaN(newValue));
	} else {
		return (required) ? false : true;
	}

};


/**
 * Updates the value for this field in the item from a data object
 *
 * @api public
 */

custom.prototype.updateItem = function(item, data) {

	if (!(this.path in data))
		return;

	var newValue = utils.number(data[this.path]);

	if (!isNaN(newValue)) {
		if (newValue !== item.get(this.path)) {
			item.set(this.path, newValue);
		}
	} else if ('number' === typeof item.get(this.path)) {
		item.set(this.path, null);
	}

};


/*!
 * Export class
 */

exports = module.exports = custom;
