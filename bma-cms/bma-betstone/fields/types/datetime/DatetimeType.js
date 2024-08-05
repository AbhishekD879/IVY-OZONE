/*!
 * Module dependencies.
 */

var util = require('util'),
	moment = require('moment'),
	moment_time_zone = require('moment-timezone'),
	super_ = require('../Type');

var parseFormats = ['YYYY-MM-DD HH:mm:ss', 'YYYY-MM-DD h:m a', 'YYYY-MM-DD H:m:s', 'YYYY-MM-DD H:m', 'YYYY-MM-DD HH:MM:SS ZZ'];

/**
 * DateTime FieldType Constructor
 * @extends Field
 * @api public
 */

function datetime(list, path, options) {

	this._nativeType = Date;
	this._underscoreMethods = ['format', 'moment', 'parse'];
	this._fixedSize = 'large';
	this._properties = ['formatString'];

	this.typeDescription = 'date and time';
	this.formatString = (options.format === false) ? false : (options.format || 'YYYY-MM-DD HH:mm:ss');

	if (this.formatString && 'string' !== typeof this.formatString) {
		throw new Error('FieldType.DateTime: options.format must be a string.');
	}

	datetime.super_.call(this, list, path, options);

	this.paths = {
		date: this._path.append('_date'),
		time: this._path.append('_time')
	};

}

/*!
 * Inherit from Field
 */

util.inherits(datetime, super_);


/**
 * Formats the field value
 *
 * @api public
 */
datetime.prototype.format = function(item, format) {
	if (format || this.formatString) {
		return item.get(this.path) ? moment(item.get(this.path)).format(format || this.formatString) : '';
	} else {
		return item.get(this.path) || '';
	}
};


/**
 * Returns a new `moment` object with the field value
 *
 * @api public
 */

datetime.prototype.moment = function(item) {
	return moment(item.get(this.path));
};


/**
 * Parses input using moment, sets the value, and returns the moment object.
 *
 * @api public
 */

datetime.prototype.parse = function(item) {
	var newValue = moment.apply(moment, Array.prototype.slice.call(arguments, 1));
	item.set(this.path, (newValue && newValue.isValid()) ? newValue.toDate() : null);
	return newValue;
};


/**
 * Get the value from a data object; may be simple or a pair of fields
 *
 * @api private
 */

datetime.prototype.getInputFromData = function(data) {
	if (this.paths.date in data && this.paths.time in data) {
		return (data[this.paths.date] + ' ' + data[this.paths.time]).trim();
	} else {
		return data[this.path];
	}
};


/**
 * Checks that a valid date has been provided in a data object
 *
 * An empty value clears the stored value and is considered valid
 *
 * @api public
 */

datetime.prototype.validateInput = function(data, required, item) {

	if (!(this.path in data && !(this.paths.date in data && this.paths.time in data)) && item && item.get(this.path)) return true;

	var newValue = moment(this.getInputFromData(data), parseFormats);

	if (required && (!newValue || !newValue.isValid())) {
		return false;
	} else if (this.getInputFromData(data) && newValue && !newValue.isValid()) {
		return false;
	} else {
		return true;
	}

};


/**
 * Updates the value for this field in the item from a data object
 *
 * @api public
 */

datetime.prototype.updateItem = function(item, data) {

	if (!(this.path in data || (this.paths.date in data && this.paths.time in data))) {
		return;
	}

	function checkWinterTime(winterTimeCompensation) {
		return (winterTimeCompensation)?reverseSign(winterTimeCompensation):0;
	}

	function reverseSign(number){
		return (number > 0)?-Math.abs(number):Math.abs(number);
	}

	// Time string should contain 2-digit hours to work properly with moment-timezone
	// DateTimeField returns format "2016-04-18 2:00:00" because of bootstrap-timepicker limitation
	function applyFormattingFix(time_template) {
		var hoursIndex = 11;
		var properLength = 19; // as in "2016-04-18 12:00:00"
    
		if (time_template.length !== properLength) {
			return time_template.slice(0, hoursIndex) + '0' + time_template.slice(hoursIndex);
		}

		return time_template;
	}

  var server_zone = parseInt(-new Date().getTimezoneOffset(), 10),
  		user_zone = global.time_zone,
  		time_zone_name = global.time_zone_name,
  		time_template = applyFormattingFix(this.getInputFromData(data)),
 			time_zone_difference = reverseSign(user_zone),
 			time = moment_time_zone.tz(time_template, time_zone_name).utcOffset(user_zone),
 			time = time.add(checkWinterTime(time._offset + time_zone_difference), 'minutes');

	if (time && time.isValid()) {
		if (!item.get(this.path) || !time.isSame(item.get(this.path))) {
			item.set(this.path, time.toDate());
		}
	} else if (item.get(this.path)) {
		item.set(this.path, null);
	}

};


/*!
 * Export class
 */

exports = module.exports = datetime;
