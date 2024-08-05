var React = require('react'),
	Field = require('../Field');

// Scope jQuery and the bootstrap-markdown editor so it will mount
var $ = require('jquery');
require('./lib/bootstrap-markdown');

// Append/remove ### surround the selection
// Source: https://github.com/toopay/bootstrap-markdown/blob/master/js/bootstrap-markdown.js#L909
var toggleHeading = function(e, level) {
	var chunk, cursor, selected = e.getSelection(), content = e.getContent(), pointer, prevChar;

	if (selected.length === 0) {
		// Give extra word
		chunk = e.__localize('heading text');
	} else {
		chunk = selected.text + '\n';
	}

	// transform selection and set the cursor into chunked text
	if ((pointer = level.length + 1, content.substr(selected.start-pointer,pointer) === level + ' ')
		|| (pointer = level.length, content.substr(selected.start-pointer,pointer) === level)) {
		e.setSelection(selected.start-pointer, selected.end);
		e.replaceSelection(chunk);
		cursor = selected.start-pointer;
	} else if (selected.start > 0 && (prevChar = content.substr(selected.start-1, 1), !!prevChar && prevChar !== '\n')) {
		e.replaceSelection('\n\n' + level + ' ' + chunk);
		cursor = selected.start + level.length + 3;
	} else {
		// Empty string before element
		e.replaceSelection(level + ' ' + chunk);
		cursor = selected.start + level.length + 1;
	}

	// Set the cursor
	e.setSelection(cursor, cursor + chunk.length);
};

var renderMarkdown = function(component) {
	// dependsOn means that sometimes the component is mounted as a null, so account for that & noop
	if (!component.refs.markdownTextarea) {
		return;
	}

	var options = {
		autofocus: false,
		savable: false,
		resize: 'vertical',
		height: component.props.height,
		hiddenButtons: ['Heading'],

		// Heading buttons
		additionalButtons: [{
			name: 'groupHeaders',
			data: [{
				name: 'cmdH1',
				title: 'Heading 1',
				btnText: 'H1',
				callback: function(e) {
					toggleHeading(e, '#');
				}
			}, {
				name: 'cmdH2',
				title: 'Heading 2',
				btnText: 'H2',
				callback: function(e) {
					toggleHeading(e, '##');
				}
			}, {
				name: 'cmdH3',
				title: 'Heading 3',
				btnText: 'H3',
				callback: function(e) {
					toggleHeading(e, '###');
				}
			}, {
				name: 'cmdH4',
				title: 'Heading 4',
				btnText: 'H4',
				callback: function(e) {
					toggleHeading(e, '####');
				}
			}]
		}],

		// Insert Header buttons into the toolbar
		reorderButtonGroups: ['groupFont', 'groupHeaders', 'groupLink', 'groupMisc', 'groupUtil']
	};

	if (component.props.toolbarOptions.hiddenButtons) {
		var hiddenButtons = ('string' === typeof component.props.toolbarOptions.hiddenButtons) ? component.props.toolbarOptions.hiddenButtons.split(',') : component.props.toolbarOptions.hiddenButtons;
		options.hiddenButtons = options.hiddenButtons.concat(hiddenButtons);
	}
	
	$(component.refs.markdownTextarea.getDOMNode()).markdown(options);
};

module.exports = Field.create({
	
	displayName: 'MarkdownField',

	// Override `shouldCollapse` to check the markdown field correctly
	shouldCollapse : function() {
		return this.props.collapse && !this.props.value.md;
	},
	
	// only have access to `refs` once component is mounted
	componentDidMount: function() {
		if (this.props.wysiwyg) {
			renderMarkdown(this);
		}
	},

	// only have access to `refs` once component is mounted
	componentDidUpdate : function() {
		if (this.props.wysiwyg) {
			renderMarkdown(this);
		}
	},
	
	renderField: function() {
		var styles = {
			padding: 8,
			height: this.props.height
		};
		
		return (
			<div className="md-editor">
				<textarea name={this.props.paths.md} style={styles} defaultValue={this.props.value.md} ref="markdownTextarea" className="form-control markdown code"></textarea>
			</div>
		);
	}
});
