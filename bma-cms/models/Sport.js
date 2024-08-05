'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  spriteManager = require('../lib/spriteManager'),
  utils = require('../lib/utils'),
  siteServer = require('../lib/siteServer'),
  path = require('path'),
  Logger = require('../lib/logger'),

  Sport = new keystone.List('sport', {
    map: { name: 'imageTitle' },
    sortable: true,
    track: true
  });

Sport.add({
  imageTitle: { type: String, required: true, label: 'Sport Title' },
  categoryId: { type: String, required: false, initial: true, default: '' },
  ssCategoryCode: { type: String, required: false, hidden: true, label: 'SS Category Code' },
  typeIds: { type: String, required: false, initial: true, default: '', note: 'Comma separated' },
  alt: { type: String },
  filename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads',
    allowedTypes: ['image/png']
  },
  icon: { type: Types.LocalFile, dest: 'public/images/uploads', allowedTypes: ['image/png'] },
  svgFilename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads/sport',
    allowedTypes: ['image/svg+xml'],
    label: 'SVG Icon'
  },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  targetUri: { type: String, default: '' },
  dispSortName: { type: String, required: true, default: 'MR', note: 'Comma separated' },
  primaryMarkets: { type: String, required: true, default: '|Match Betting|' },
  outcomesTemplateType1: {
    type: Types.Select,
    options: 'homeDrawAwayType, oneTwoType',
    default: 'homeDrawAwayType',
    emptyOption: false,
    label: 'Template Type 1'
  },
  disabled: { type: Types.Boolean, default: false },
  inApp: { type: Types.Boolean, default: true },
  collectionType: { type: String, hidden: true, default: '/sport/' },
  spriteClass: { type: String, hidden: true },
  uriSmall: { type: String, hidden: true },
  uriMedium: { type: String, hidden: true },
  uriLarge: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },
  widthSmallIcon: { type: Number, hidden: true },
  heightSmallIcon: { type: Number, hidden: true },
  widthMediumIcon: { type: Number, hidden: true },
  heightMediumIcon: { type: Number, hidden: true },
  widthLargeIcon: { type: Number, hidden: true },
  heightLargeIcon: { type: Number, hidden: true },
  uriSmallIcon: { type: String, hidden: true },
  uriMediumIcon: { type: String, hidden: true },
  uriLargeIcon: { type: String, hidden: true },
  showInPlay: { type: Types.Boolean, default: true, label: 'Show in In Play' },
  isOutrightSport: { type: Types.Boolean, default: false },
  isMultiTemplateSport: { type: Types.Boolean, default: false },
  tabLive: { type: Types.TextWithCheckbox, default: { tabLabel: 'Live', visible: true } },
  tabMatches: { type: Types.TextWithCheckbox, default: { tabLabel: 'Events', visible: true } },
  // tabCompetitions: {type: Types.TextWithCheckbox},
  // tabCoupons: {type: Types.TextWithCheckbox},
  tabOutrights: { type: Types.TextWithCheckbox, default: { tabLabel: 'Outrights', visible: true } },
  tabSpecials: { type: Types.TextWithCheckbox, default: { tabLabel: 'Specials', visible: true } },
  // tabJackpot: {type: Types.TextWithCheckbox},
  defaultTab: {
    type: Types.Select,
    options: [
      { value: 'live', label: 'Tab Live' },
      { value: 'matches', label: 'Tab Matches' },
      { value: 'outrights', label: 'Tab Outrights' },
      { value: 'specials', label: 'Tab Specials' }
    ],
    default: 'matches',
    emptyOption: false
  },
  // TODO: it will be uncommented when sport module supports all sports
  // isOlympicSport: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

Sport.schema.path('svg').validate(function(value, respond) {
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

Sport.schema.path('categoryId').validate(function() {
  if (!this.categoryId && !this.typeIds) {
    this.invalidate('categoryId', 'Category Id or Type Ids should be set');
    this.invalidate('typeIds', 'Category Id or Type Ids should be set');
  } else {
    if (/^[0-9]*$/.test(this.categoryId) === false) {
      this.invalidate('categoryId', 'Category Id should be a number');
    }

    if (this.typeIds && /^([0-9]+,)*[0-9]+$/.test(this.typeIds) === false) {
      this.invalidate('typeIds', 'Type Ids should be comma-separated numbers');
    }
  }
}, 'Category Id or Type Ids should be set');

Sport.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  next();
});

Sport.schema.pre('save', function(next) {
  if (this.typeIds) {
    siteServer.getCategoriesByTypeIds(this.typeIds)
      .then(categories => {
        if (categories.length === 1) {
          return categories[0];
        }
        return Promise.reject(new Error('Type Ids from more than 1 category were set'));
      })
      .then(category => {
        if (!this.categoryId) {
          this.categoryId = category.categoryId;
        }

        if (category.categoryId === this.categoryId) {
          this.ssCategoryCode = category.categoryCode;
          return true;
        }
        return Promise.reject(new Error('Category Id doesn\'t contain entered Type Ids'));
      })
      .then(() => next())
      .catch(err => {
        if (err) {
          this.invalidate('typeIds', err.message, this.typeIds);
          this.validate(next);
        }
      });
  } else {
    siteServer.getTypeIdsAndCategoryByCategoryId(this.categoryId)
      .then(data => {
        this.typeIds = data.typeIds.join(',');
        this.ssCategoryCode = data.categoryCode;
        return this.typeIds;
      })
      .then(() => next())
      .catch(err => {
        if (err) {
          this.invalidate('typeIds', err.message, this.typeIds);
          this.validate(next);
        }
      });
  }
});

Sport.schema.pre('save', function(next) {
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

Sport.schema.pre('remove', function(next) {
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
  apiManager.run('sports', { brand });
  initialDataManager.regenCache(brand);
}

Sport.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'sports by user',
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

Sport.schema.post('remove', item => regenCache(item.brand));

Sport.defaultColumns = 'imageTitle, categoryId, alt, filename, targetUri, inApp, disabled, showInPlay, isOutrightSport';
Sport.register();
