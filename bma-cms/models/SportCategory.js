'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  spriteManager = require('../lib/spriteManager'),
  utils = require('../lib/utils'),
  path = require('path'),
  Logger = require('../lib/logger'),

  SportCategory = new keystone.List('sportCategory', {
    map: { name: 'imageTitle' },
    sortable: true,
    track: true
  });

SportCategory.add({
  imageTitle: { type: String, required: true },
  categoryId: { type: Number, required: true, initial: true, default: 0 },
  ssCategoryCode: { type: String, required: true, initial: true, label: 'SS Category Code' },
  alt: { type: String },
  filename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads',
    allowedTypes: ['image/png']
  },
  icon: {
    type: Types.LocalFile,
    dest: 'public/images/uploads',
    allowedTypes: ['image/png']
  },
  svgFilename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads/sport-category',
    allowedTypes: ['image/svg+xml'],
    label: 'SVG Icon'
  },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  path: { type: String, default: 'public/images/uploads', hidden: true },
  targetUri: { type: String, default: '' },
  disabled: { type: Types.Boolean, default: false },
  inApp: { type: Types.Boolean, default: true },
  collectionType: { type: String, hidden: true, default: '/sport_category/' },
  spriteClass: { type: String, hidden: true },
  uriSmall: { type: String, hidden: true },
  uriMedium: { type: String, hidden: true },
  uriLarge: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  widthMedium: { type: Number, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },
  widthSmallIcon: { type: Number, hidden: true },
  heightSmallIcon: { type: Number, hidden: true },
  widthMediumIcon: { type: Number, hidden: true },
  heightMediumIcon: { type: Number, hidden: true },
  widthLargeIcon: { type: Number, hidden: true },
  heightLargeIcon: { type: Number, hidden: true },
  uriSmallIcon: { type: String, hidden: true },
  uriMediumIcon: { type: String, hidden: true },
  showInPlay: { type: Types.Boolean, default: true, label: 'Show in In Play' },
  showInHome: { type: Types.Boolean, default: true, label: 'Show in Sports Ribbon' },
  showInAZ: { type: Types.Boolean, default: true, label: 'Show in A-Z' },
  showScoreboard: { type: Types.Boolean, default: false, label: 'Show Scoreboard' },
  scoreBoardUrl: { type: String, label: 'ScoreBoard Url' },
  isTopSport: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

SportCategory.relationship({ path: 'banners', ref: 'Banner', refPath: 'categoryId' });

SportCategory.schema.path('svg').validate(function(value, respond) {
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

SportCategory.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  const qTasks = [];

  this.spriteClass = this.imageTitle.replace(utils.regExp, '');

  if (this.brand !== 'bma') {
    this.spriteClass = `${this.brand}_${this.spriteClass}`;
  }

  this.widthSmall = this.heightSmall = 104;
  this.widthMedium = this.heightMedium = 32;
  this.widthLarge = this.heightLarge = 96;
  this.widthSmallIcon = this.heightSmallIcon = 20;
  this.widthMediumIcon = this.heightMediumIcon = 32;
  this.widthLargeIcon = this.heightLargeIcon = 96;

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

  if (this.icon && this.icon.filename) {
    qTasks.push(spriteManager.createSizes(this, 'icon'));
  } else {
    qTasks.push(spriteManager.removeSizes(this, 'icon'));
  }

  if (qTasks.length > 0) {
    Promise.all(qTasks)
      .then(
        () => next(),
        next
      );
  } else {
    next();
  }
});

SportCategory.schema.pre('remove', function(next) {
  Promise.all([
    spriteManager.removeSizes(this, 'filename'),
    spriteManager.removeSizes(this, 'icon')
  ])
    .then(
      () => next(),
      next
    );
});

function regenCache(brand) {
  apiManager.run('sportCategory', { brand });
  apiManager.run('sportCategoryNative', { brand, isNative: true });
  initialDataManager.regenCache(brand);
}

SportCategory.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'sport-categories by user',
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

SportCategory.schema.post('remove', item => regenCache(item.brand));

SportCategory.defaultColumns =
  'imageTitle, categoryId, alt, filename, targetUri, inApp, disabled, showInHome, showInPlay, showInAZ, showScoreboard';

SportCategory.register();
