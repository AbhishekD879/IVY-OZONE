const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  Q = require('q'),
  apiManager = require('../lib/api'),
  spriteManager = require('../lib/spriteManager'),
  utils = require('../lib/utils'),
  path = require('path'),
  Logger = require('../lib/logger'),

  RightMenu = new keystone.List('rightMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

RightMenu.add({
  linkTitle: { type: String, required: true, unique: false },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  section: { type: Types.Select, options: 'top, center, bottom', default: 'top', emptyOption: false },
  type: { type: Types.Select, options: 'link, button', default: 'link', emptyOption: false },
  disabled: { type: Types.Boolean, default: false },
  inApp: { type: Types.Boolean, default: true },
  QA: { type: Types.Text, initial: true },
  filename: { type: Types.LocalFile, dest: 'public/images/uploads', allowedTypes: ['image/png'] },
  svgFilename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads/right-menu',
    allowedTypes: ['image/svg+xml']
  },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  path: { type: String, default: 'public/images/uploads', hidden: true },
  collectionType: { type: String, hidden: true, default: '/right_menu/' },
  showItemFor: { type: Types.Select, options: 'loggedIn, loggedOut, both', default: 'both', emptyOption: false },
  showOnlyOnIOS: { type: Types.Boolean, default: false },
  showOnlyOnAndroid: { type: Types.Boolean, default: false },
  menuItemView: { type: Types.Select, options: 'icon, description, both', default: 'description', emptyOption: false },
  iconAligment: { type: Types.Select, options: 'left, right', default: 'left', emptyOption: false },
  spriteClass: { type: String, hidden: true },
  uriSmall: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  uriMedium: { type: String, hidden: true },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  uriLarge: { type: String, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },

  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  authRequired: { type: Types.Boolean, label: 'Authentication Required', default: false },
  systemID: { type: Types.Number, label: 'SystemID' }
});

RightMenu.schema.path('svg').validate(function(value, respond) {
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

RightMenu.schema.path('section').validate(function(value, respond) {
  const itemId = this.id,
    sectionState = value;

  // Get list of all menu items
  keystone.list('rightMenu')
    .model.find()
    .exec((err, res) => {
      if (err) {
        respond(false);
        Logger.error('AKAMAI', err);
      } else {
        const itemWasBottom = res.some((element, index, array) => {
          return (String(itemId) === String(array[index]._id)) && array[index].section === 'bottom';
        });
        if (itemWasBottom) {
          respond(true);
        }
      }
    });

  // Validate max amount of menu items in bottom section
  keystone.list('rightMenu')
    .model.count()
    .where({ section: 'bottom' })
    .exec((err, count) => {
      if (err) {
        respond(false);
        Logger.error('AKAMAI', err);
      }
      if (sectionState === 'bottom' && count >= 3) {
        respond(false);
      } else {
        respond(true);
      }
    });
}, 'You cannot create more than 3 items in bottom section');

RightMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  const qTasks = [];

  this.spriteClass = this.linkTitle.replace(utils.regExp, '');

  if (this.brand !== 'bma') {
    this.spriteClass = `${this.brand}_${this.spriteClass}`;
  }

  this.widthSmall = this.heightSmall = 40;
  this.widthMedium = this.heightMedium = 156;
  this.widthLarge = this.heightLarge = 468;

  if (this.filename && this.filename.filename) {
    qTasks.push(spriteManager.createSizes(this, 'filename'));
  } else {
    qTasks.push(spriteManager.removeSizes(this, 'filename'));
  }

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
    Q.all(qTasks)
      .then(() => {
        next();
      }, err => {
        next(err);
      });
  } else {
    next();
  }
});

RightMenu.schema.pre('remove', function(next) {
  spriteManager.removeSizes(this, 'filename')
    .then(() => {
      next();
    }, err => {
      next(err);
    });
});

RightMenu.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'right-menu by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  // TODO: call api for old brand, if brand value was changed
  apiManager.run('rightMenu', {
    brand: item.brand
  });

  // Solution for a need to keep 'retail' brand
  if (item.brand === 'connect') {
    apiManager.run('rightMenu', { brand: 'retail' });
  }
});

RightMenu.schema.post('remove', item => {
  apiManager.run('rightMenu', {
    brand: item.brand
  });

  // Solution for a need to keep 'retail' brand
  if (item.brand === 'connect') {
    apiManager.run('rightMenu', { brand: 'retail' });
  }
});

RightMenu.defaultColumns = 'linkTitle, targetUri, section, disabled, inApp, filename,' +
  'showItemFor, showOnlyOnIOS, showOnlyOnAndroid, menuItemView, iconAligment, authRequired';

RightMenu.register();
