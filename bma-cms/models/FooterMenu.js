'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  spriteManager = require('../lib/spriteManager'),
  utils = require('../lib/utils'),
  path = require('path'),
  Logger = require('../lib/logger'),

  FooterMenu = new keystone.List('footerMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true,
    note: 'Only top 5 or 6 items (depending on brand) of each device type, will be displayed'
  });

FooterMenu.add({
  linkTitle: { type: String, required: true, initial: true, unique: false },
  targetUri: {
    type: String,
    required: false,
    default: '',
    initial: true,
    unique: false,
    dependsOn: { itemType: 'link' }
  },
  disabled: { type: Types.Boolean, default: false },
  inApp: { type: Types.Boolean, default: true, dependsOn: { itemType: 'link' } },
  filename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads',
    allowedTypes: ['image/png'],
    dependsOn: { itemType: 'link' }
  },
  svgFilename: { type: Types.LocalFile, dest: 'public/images/uploads/footer-menu', allowedTypes: ['image/svg+xml'] },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  showItemFor: {
    type: Types.Select,
    options: 'loggedIn, loggedOut, both',
    default: 'both',
    emptyOption: false,
    dependsOn: { itemType: 'link' }
  },
  mobile: { type: Types.Boolean, default: false },
  tablet: { type: Types.Boolean, default: false },
  desktop: { type: Types.Boolean, default: false, dependsOn: { itemType: 'link' } },
  uriSmall: { type: String, hidden: true },
  uriMedium: { type: String, hidden: true },
  uriLarge: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  spriteClass: { type: String, hidden: true },
  path: { type: String, default: 'public/images/uploads', hidden: true },
  collectionType: { type: String, hidden: true, default: '/footer_menu/' },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  itemType: { type: Types.Select, options: ['link', 'widget'], default: 'link', emptyOption: false, hidden: true },
  widgetName: {
    type: Types.Select,
    options: ['myBets', 'betslip', 'cashout'],
    dependsOn: { itemType: 'widget' },
    noedit: true
  },
  authRequired: { type: Types.Boolean, label: 'Authentication Required', default: false },
  systemID: { type: Types.Number, label: 'SystemID' }
});

FooterMenu.schema.path('svg').validate(function(value, respond) {
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
    respond(true);
  }
}, 'Wrong format SVG File');

FooterMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  const qTasks = [];

  this.spriteClass = this.linkTitle.replace(utils.regExp, '');

  if (this.brand !== 'bma') {
    this.spriteClass = `${this.brand}_${this.spriteClass}`;
  }

  this.widthSmall = this.heightSmall = 40;
  this.widthMedium = this.heightMedium = 32;
  this.widthLarge = this.heightLarge = 96;

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

  if (this.filename && this.filename.filename) {
    qTasks.push(spriteManager.createSizes(this, 'filename'));
  } else {
    qTasks.push(spriteManager.removeSizes(this, 'filename'));
  }

  if (qTasks.length > 0) {
    Promise.all(qTasks)
      .then(() => next(), next);
  } else {
    next();
  }
});

FooterMenu.schema.pre('remove', function(next) {
  spriteManager.removeSizes(this, 'filename')
    .then(() => {
      next();
    }, err => {
      next(err);
    });
});

FooterMenu.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'footer-menu by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  regenCache(item.brand);
});

FooterMenu.schema.post('remove', item => {
  regenCache(item.brand);
});

function regenCache(brand) {
  const devices = ['mobile', 'tablet', 'desktop'],
    results = devices.map(device => {
      // TODO: call api for old brand, if brand value was changed
      return Promise.all([
        apiManager.run('footerMenuV2', {
          brand,
          deviceType: device
        }),
        apiManager.run('footerMenuV3', {
          brand
        })
      ]);
    });
  initialDataManager.regenCache(brand);
  return Promise.all(results);
}

FooterMenu.defaultColumns =
  'linkTitle, itemType, targetUri, disabled, inApp, filename, showItemFor, mobile, tablet, desktop, authRequired';
FooterMenu.register();
