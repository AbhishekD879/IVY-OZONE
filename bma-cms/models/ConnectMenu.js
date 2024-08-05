const path = require('path'),
  keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),
  utils = require('../lib/utils'),
  Types = keystone.Field.Types,

  ConnectMenu = new keystone.List('connectMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

ConnectMenu.add({
  linkTitle: { type: String, required: true, initial: true, unique: false },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  disabled: { type: Types.Boolean, default: false },
  inApp: { type: Types.Boolean, default: true },
  svgFilename: { type: Types.LocalFile, dest: 'public/images/uploads/connect-menu', allowedTypes: ['image/svg+xml'] },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  showItemFor: { type: Types.Select, options: 'loggedIn, loggedOut, both', default: 'both', emptyOption: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  level: { type: Types.Select, options: ['1', '2'], default: '1', initial: true },
  parent: {
    type: Types.Relationship,
    dependsOn: {
      level: '2'
    },
    filters: { level: '1' },
    ref: 'connectMenu',
    initial: true
  }
});

ConnectMenu.schema.path('svg').validate(function(value, respond) {
  if (this.svgFilename && this.svgFilename.filename) {
    utils
      .readFile(path.join(this.svgFilename.path, this.svgFilename.filename), 'utf8')
      .then(utils.validateSvg)
      .then(() => {
        respond();
      })
      .catch(err => {
        this.invalidate('svgFilename', err);
        respond();
      });
  } else {
    respond();
  }
}, 'Wrong format SVG File');

ConnectMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  if (this.level === '1') {
    this.parent = null;
  }

  const qTasks = [];

  if (this.svgFilename && this.svgFilename.filename) {
    qTasks.push(
      utils.readFile(path.join(this.svgFilename.path, this.svgFilename.filename), 'utf8')
        .then(utils.processSvg)
        .then(processedSvg => {
          this.svg = processedSvg.svg;
          this.svgId = processedSvg.id;
        })
    );
  } else {
    this.svg = '';
    this.svgId = '';
  }

  if (qTasks.length > 0) {
    Promise.all(qTasks)
      .then(() => next(), next);
  } else {
    next();
  }
});

ConnectMenu.schema.post('save', item => {
  apiManager.run('connectMenu', {
    brand: item.brand
  });
});

ConnectMenu.schema.post('remove', item => {
  apiManager.run('connectMenu', {
    brand: item.brand
  });
});

ConnectMenu.defaultColumns = 'linkTitle, targetUri, disabled, inApp, level, parent, showItemFor';
ConnectMenu.register();
