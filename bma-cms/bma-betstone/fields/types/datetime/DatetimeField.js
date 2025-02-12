var React = require('react'),
	Field = require('../Field'),
	Note = require('../../components/Note'),
	DateInput = require('../../components/DateInput'),
	moment = require('moment');

module.exports = Field.create({
	
	displayName: 'DatetimeField',

	focusTargetRef: 'dateInput',

	// default input formats
	dateInputFormat: 'YYYY-MM-DD',
	timeInputFormat: 'HH:mm:ss',

	// parse formats (duplicated from lib/fieldTypes/datetime.js)
	parseFormats: ['YYYY-MM-DD HH:mm:ss', 'YYYY-MM-DD H:m:s', 'YYYY-MM-DD H:m'],

	getInitialState: function() {
		return { 
			dateValue: this.props.value ? moment(this.props.value).format(this.dateInputFormat) : '',
			timeValue: this.props.value ? moment(new Date(this.props.value)).format(this.timeInputFormat) : ''
		};
	},

	getDefaultProps: function() {
		return { 
			formatString: 'Do MMM YYYY, HH:mm:ss'
		};
	},

	// TODO: Move isValid() so we can share with server-side code
	isValid: function(value) {
		return moment(value, this.parseFormats).isValid();
	},

	// TODO: Move format() so we can share with server-side code
	format: function(value, format) {
		format = format || this.dateInputFormat + ' ' + this.timeInputFormat;
		return value ? moment(value).format(format) : '';
	},

	handleChange: function(dateValue, timeValue) {
		var value = dateValue + ' ' + timeValue,
			datetimeFormat = this.dateInputFormat + ' ' + this.timeInputFormat;
		this.props.onChange({
			path: this.props.path,
			value: this.isValid(value) ? moment(value, datetimeFormat).toISOString() : null
		});
	},

	dateChanged: function(value) {
		this.setState({ dateValue: value });
		this.handleChange(value, this.state.timeValue);
	},
	timepickerChanged: function(event) {
		var time = $('.timepickerAnchor.changed').val();
		this.setState({ timeValue: time });
		this.handleChange(this.state.dateValue, time);
	},
	timeChanged: function(event) {
		this.setState({ timeValue: event.target.value });
		this.handleChange(this.state.dateValue, event.target.value);
	},
	setNow: function() {

    var timeNow = new Date();
		var dateValue = moment().format(this.dateInputFormat),
			timeValue = moment(timeNow).format(this.timeInputFormat);

		this.setState({
			dateValue: dateValue,
			timeValue: timeValue
		});
		this.handleChange(dateValue, timeValue);
	},

	renderUI: function() {
		
		var input,
			fieldClassName = 'field-ui';
		
		if (this.shouldRenderField()) {
			input = (
				<div className={fieldClassName}>
					<DateInput ref="dateInput" name={this.props.paths.date} value={this.state.dateValue} format={this.dateInputFormat} onChange={this.dateChanged} />
					<span className="bootstrap-timepicker timepicker">
            <input name={this.props.paths.time} type="text" className="timepickerAnchor form-control" autoComplete="off" placeholder="HH:mm:ss" value={this.state.timeValue} onChange={this.timeChanged} />
        	</span>
					<button type="button" className="btn btn-default btn-set-now" onClick={this.setNow}>Now</button>
					<button type="button" className="btn btn-default btn-set-time hidden" onClick={this.timepickerChanged}>Now</button>
				</div>
			);
		} else {
			input = (
				<div className={fieldClassName}>
					<div className="field-value">{this.format(this.props.value, this.props.formatString)}</div>
				</div>
			);
		}
		
		return (
			<div className="field field-type-datetime">
				<label className="field-label">{this.props.label}</label>
				{input}
				<div className="col-sm-9 col-md-10 col-sm-offset-3 col-md-offset-2 field-note-wrapper">
					<Note note={this.props.note} />
				</div>
			</div>
		);
	}

});
