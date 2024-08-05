var React = require('react'),
	Field = require('../Field');

module.exports = Field.create({
	displayName: 'TextWithCheckboxField',

  checkboxValueChanged: function(which, event) {
    this.props.value[which] = event.target.checked;
    this.props.onChange({
      path: this.props.path.visible,
      value: event.target.checked
    });
  },

  textValueChanged: function(which, event) {
    this.props.value[which] = event.target.value;
    this.props.onChange({
      path: this.props.path,
      value: this.props.value
    });
  },
  
  renderField: function() {
    return (
      <div className="form-row">
        <div className="col-sm-6">
          <input type="text" name={this.props.paths.tablabel} id={this.props.paths.tablabel} placeholder="Tab Label" ref="tabLabel" value={this.props.value.tablabel} className="form-control" onChange={this.textValueChanged.bind(this, 'tablabel')} />
        </div>
        <div className="col-sm-6">
          <input type="checkbox" name={this.props.paths.visible} value='true' checked={this.props.value.visible} onChange={this.checkboxValueChanged.bind(this, 'visible')} /> <span> Visible</span>
        </div>
      </div>
    );
  }
});
