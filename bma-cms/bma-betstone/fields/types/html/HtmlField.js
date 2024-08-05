var tinymce = require('tinymce'),
  React = require('react'),
  Field = require('../Field'),
  _ = require('underscore');

var lastId = 0;

tinymce.PluginManager.add('stylebuttons', function(editor, url) {
  ['h1', 'h2'].forEach(function(name){
    editor.addButton("style-" + name, {
      tooltip: "Toggle " + name,
      text: name.toUpperCase(),
      onClick: function() { editor.execCommand('mceToggleFormat', false, name); },
      onPostRender: function() {
        var self = this, setup = function() {
          editor.formatter.formatChanged(name, function(state) {
            self.active(state);
          });
        };
        editor.formatter ? setup() : editor.on('init', setup);
      }
    })
  });
});

function getId() {
  return 'keystone-html-' + lastId++;
}

module.exports = Field.create({
  displayName: 'HtmlField',

  getInitialState: function() {
    return {
      id: getId(),
      isFocused: false
    };
  },

  initWysiwyg: function() {
    if (!this.props.wysiwyg) return;

    var self = this;
    var opts = this.getOptions();

    opts.setup = function (editor) {
      self.editor = editor;
      editor.on('change', self.valueChanged);
      editor.on('focus', self.focusChanged.bind(self, true));
      editor.on('blur', self.focusChanged.bind(self, false));
      // set default font to Lato
      editor.on('init', function(e) {
        !editor.getContent() && editor.execCommand('fontName', false, 'Lato');
      });
    };

    this._currentValue = this.props.value;

    opts.extended_valid_elements = "h1[*],h2[*],h3[*],h4[*],p[*],div[*],span[*],img[*],a[*],altGlyph[*],altGlyphDef[*],altGlyphItem[*],animate[*],animateColor[*],animateMotion[*],animateTransform[*],animation[*],audio[*],canvas[*],circle[*],clipPath[*],color-profile[*],cursor[*],defs[*],desc[*],discard[*],ellipse[*],feBlend[*],feColorMatrix[*],feComponentTransfer[*],feComposite[*],feConvolveMatrix[*],feDiffuseLighting[*],feDisplacementMap[*],feDistantLight[*],feDropShadow[*],feFlood[*],feFuncA[*],feFuncB[*],feFuncG[*],feFuncR[*],feGaussianBlur[*],feImage[*],feMerge[*],feMergeNode[*],feMorphology[*],feOffset[*],fePointLight[*],feSpecularLighting[*],feSpotLight[*],feTile[*],feTurbulence[*],filter[*],font[*],font-face[*],font-face-format[*],font-face-name[*],font-face-src[*],font-face-uri[*],foreignObject[*],g[*],glyph[*],glyphRef[*],handler[*],hatch[*],hatchpath[*],hkern[*],iframe[*],image[*],line[*],linearGradient[*],listener[*],marker[*],mask[*],mesh[*],meshpatch[*],meshrow[*],metadata[*],missing-glyph[*],mpath[*],path[*],pattern[*],polygon[*],polyline[*],prefetch[*],radialGradient[*],rect[*],script[*],set[*],solidColor[*],solidcolor[*],stop[*],style[*],svg[*],switch[*],symbol[*],tbreak[*],text[*],textArea[*],textPath[*],title[*],tref[*],tspan[*],unknown[*],use[*],video[*],view[*],vkern[*]";
    opts.file_browser_callback = function(field_name, url, type, win) {
      if(type=='image') $('#file-form-input').click();
    };
    opts.plugins.push( 'BMA' );
    opts.plugins.push( 'preview' );
    opts.plugins.push( 'stylebuttons' );
    opts.toolbar += ' | style-h1 style-h2 | fontselect |addCollapsePanel makeButton images | preview';
    opts.content_css = ['/keystone/js/lib/tinymce/plugins/bma/content.css'];
    opts.font_formats = 'Arial=Arial,Helvetica,Sans-Serif;Lato=Lato;';
    tinymce.init(opts);
  },

  componentDidUpdate: function(prevProps, prevState) {
    if (prevState.isCollapsed && !this.state.isCollapsed) {
      this.initWysiwyg();
    }

    if (_.isEqual(this.props.dependsOn, this.props.currentDependencies)
      && !_.isEqual(this.props.currentDependencies, prevProps.currentDependencies)) {
      var instance = tinymce.get(prevState.id);
      if (instance) {
        tinymce.EditorManager.execCommand('mceRemoveEditor', true, prevState.id)
        this.initWysiwyg();
      } else {
        this.initWysiwyg();
      }
    }
  },

  componentDidMount: function() {

    // Render fileForm form outside current component, because forms can't be nested in React.
    this.formContainer = document.createElement('div', { className: 'file-form-container' });
    document.body.appendChild(this.formContainer);
    this.renderFileForm(this.formContainer);

    this.initWysiwyg();
  },

  componentWillReceiveProps: function(nextProps) {
    if (this.editor && this._currentValue !== nextProps.value) {
      this.editor.setContent(nextProps.value);
    }
  },

  componentWillUnmount() {
    document.body.removeChild(this.formContainer);
  },

  renderFileForm: function(container) {
    React.render(this.getFileForm(), container);
  },

  handleFileInputChange: function() {
    var submitInput = $("<input id='file-form-submit' type='submit' />");
    $('#file-form').append(submitInput);
    submitInput.trigger('click').remove();
    $('#file-form-input').val('');
  },

  handleFileFormSubmit: function(e) {
    const fd = new FormData(document.getElementById('file-form'));
    fd.append('itemId', Keystone.itemId);
    fd.append('listId', Keystone.list.key);

    $.ajax({
      url: '/keystone/api/wysiwyg-image-upload',
      data: fd,
      cache: false,
      contentType: false,
      processData: false,
      type: 'POST',
      success: function(data) {
        top.$('.mce-btn.mce-open').parent().find('.mce-textbox').val(data.path);
      },
      error: function(data) {
        // Reload to show flash message if wrong file type
        if (data.status === 415) {
          document.location.reload();
        }
      }
    });
    e.preventDefault();
  },

  getFileForm: function() {
    return (<div>
      <form
        id='file-form'
        onSubmit={this.handleFileFormSubmit}
        encType='multipart/form-data'
        style={{width:'0px', height:'0', overflow:'hidden'}}
      >
        <input
          id='file-form-input'
          name='image'
          type='file'
          onChange={this.handleFileInputChange}
        />
      </form>
    </div>)
  },

  focusChanged: function(focused) {
    this.setState({
      isFocused: focused
    });
  },

  valueChanged: function () {
    var content;
    if (this.editor) {
      content = this.editor.getContent();
    } else if (this.refs.editor) {
      content = this.refs.editor.getDOMNode().value;
    } else {
      return;
    }

    this._currentValue = content;
    this.props.onChange({
      path: this.props.path,
      value: content
    });
  },

  getOptions: function() {
    var plugins = ['code', 'link'],
      options = _.defaults(
        {},
        this.props.wysiwyg,
        Keystone.wysiwyg.options
      ),
      toolbar = options.overrideToolbar ? '' : 'bold italic | alignleft aligncenter alignright | bullist numlist | outdent indent | link';

    if (options.enableImages) {
      plugins.push('image');
      toolbar += ' | image';
    }

    if (options.enableCloudinaryUploads) {
      plugins.push('uploadimage');
      toolbar += options.enableImages ? ' uploadimage' : ' | uploadimage';
    }

    if (options.additionalButtons) {
      var additionalButtons = options.additionalButtons.split(',');
      for (var i = 0; i < additionalButtons.length; i++) {
        toolbar += (' | ' + additionalButtons[i]);
      }
    }
    if (options.additionalPlugins) {
      var additionalPlugins = options.additionalPlugins.split(',');
      for (var i = 0; i < additionalPlugins.length; i++) {
        plugins.push(additionalPlugins[i]);
      }
    }
    if (options.importcss) {
      plugins.push('importcss');
      var importcssOptions = {
        content_css: options.importcss,
        importcss_append: true,
        importcss_merge_classes: true
      };

      _.extend(options.additionalOptions, importcssOptions);
    }

    if (!options.overrideToolbar) {
      toolbar += ' | code';
    }

    var opts = {
      selector: '#' + this.state.id,
      toolbar:  toolbar,
      plugins:  plugins,
      menubar:  options.menubar || false,
      skin:     options.skin || 'keystone',
      relative_urls: options.relative_urls,
      script_host: options.script_host,
      convert_urls: options.convert_urls
    };

    if (this.shouldRenderField()) {
      opts.uploadimage_form_url = '/keystone/api/cloudinary/upload';
    } else {
      _.extend(opts, {
        mode: 'textareas',
        readonly: true,
        menubar: false,
        toolbar: 'code',
        statusbar: false
      });
    }

    if (options.additionalOptions){
      _.extend(opts, options.additionalOptions);
    }

    return opts;
  },

  getFieldClassName: function() {
    var className = this.props.wysiwyg ? 'wysiwyg' : 'code';
    return className;
  },

  renderEditor: function(readOnly) {
    var className = this.state.isFocused ? 'is-focused' : '';
    var style = {
      height: this.props.height
    };
    return (
      <div className={className}>
        <textarea ref='editor' style={style} onChange={this.valueChanged} id={this.state.id} className={this.getFieldClassName()} name={this.props.path} readOnly={readOnly} value={this.props.value}></textarea>
      </div>
    );
  },

  renderField: function() {
    return this.renderEditor();
  },

  renderValue: function() {
    return this.renderEditor(true);
  }

});
