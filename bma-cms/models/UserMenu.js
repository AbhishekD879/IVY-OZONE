const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  Q = require('q'),
  apiManager = require('../lib/api'),
  spriteManager = require('../lib/spriteManager'),
  utils = require('../lib/utils'),
  path = require('path'),
  Logger = require('../lib/logger'),

  UserMenu = new keystone.List('userMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

UserMenu.add({
  linkTitle: { type: String, required: true, unique: false },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  disabled: { type: Types.Boolean, default: false },
  filename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads',
    allowedTypes: ['image/png', 'image/jpg', 'image/jpeg']
  },
  svgFilename: {
    type: Types.LocalFile,
    dest: 'public/images/uploads/user-menu',
    allowedTypes: ['image/svg+xml']
  },
  svgId: { type: String, default: '', hidden: true },
  svg: { type: String, default: '', hidden: true },
  path: { type: String, default: 'public/images/uploads', hidden: true },
  spriteClass: { type: String, hidden: true },
  activeIfLogout: { type: Types.Boolean, default: false },
  QA: { type: Types.Text, initial: true },
  uriSmall: { type: String, hidden: true },
  uriMedium: { type: String, hidden: true },
  uriLarge: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },
  collectionType: { type: String, hidden: true, default: '/user_menu/' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  showUserMenu: {
    type: Types.Select,
    options: [
      { value: 'mobtablet', label: 'Mobile/Tablet' },
      { value: 'desktop', label: 'Desktop' },
      { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false
  }
});

UserMenu.schema.path('svg').validate(function(value, respond) {
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

UserMenu.schema.pre('save', function(next) {
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

UserMenu.schema.pre('remove', function(next) {
  spriteManager.removeSizes(this, 'filename')
    .then(() => {
      next();
    }, err => {
      next(err);
    });
});

UserMenu.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'user-menu by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  // TODO: call api for old brand, if brand value was changed
  apiManager.run('userMenu', {
    brand: item.brand
  });
});

UserMenu.schema.post('remove', item => {
  apiManager.run('userMenu', {
    brand: item.brand
  });
});

UserMenu.defaultColumns = 'linkTitle, targetUri, disabled, showUserMenu, activeIfLogout, filename';
UserMenu.register();
