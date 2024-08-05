const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  Q = require('q'),
  spriteManager = require('../lib/spriteManager'),
  apiManager = require('../lib/api'),
  utils = require('../lib/utils'),
  Logger = require('../lib/logger'),

  TopGames = new keystone.List('topGames', {
    map: { name: 'imageTitle' },
    sortable: true,
    track: true
  });

TopGames.add({
  imageTitle: { type: String, required: true },
  alt: { type: String },
  filename: { type: Types.LocalFile, dest: 'public/images/uploads', allowedTypes: ['image/png'] },
  icon: { type: Types.LocalFile, dest: 'public/images/uploads', allowedTypes: ['image/png'] },
  path: { type: String, default: 'public/images/uploads', hidden: true },
  targetUri: { type: String },
  disabled: { type: Types.Boolean, default: false },
  spriteClass: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  widthLarge: { type: Number, hidden: true },
  heightLarge: { type: Number, hidden: true },
  collectionType: { type: String, hidden: true, default: '/top_games/' },
  uriSmall: { type: String, hidden: true },
  uriMedium: { type: String, hidden: true },
  uriLarge: { type: String, hidden: true },
  uriSmallIcon: { type: String, hidden: true },
  uriMediumIcon: { type: String, hidden: true },
  uriLargeIcon: { type: String, hidden: true },
  widthSmallIcon: { type: Number, hidden: true },
  heightSmallIcon: { type: Number, hidden: true },
  widthMediumIcon: { type: Number, hidden: true },
  heightMediumIcon: { type: Number, hidden: true },
  widthLargeIcon: { type: Number, hidden: true },
  heightLargeIcon: { type: Number, hidden: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

TopGames.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  const qTasks = [];

  this.spriteClass = this.imageTitle.replace(utils.regExp, '');

  if (this.brand !== 'bma') {
    this.spriteClass = `${this.brand}_${this.spriteClass}`;
  }

  this.widthSmall = this.heightSmall = 104;
  this.widthMedium = this.heightMedium = 60;
  this.widthLarge = this.heightLarge = 180;
  this.widthSmallIcon = this.heightSmallIcon = 20;
  this.widthMediumIcon = this.heightMediumIcon = 32;
  this.widthLargeIcon = this.heightLargeIcon = 96;

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

TopGames.schema.pre('remove', function(next) {
  Q.all([
    spriteManager.removeSizes(this, 'filename'),
    spriteManager.removeSizes(this, 'icon')
  ])
    .then(() => {
      next();
    }, err => {
      next(err);
    });
});

TopGames.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info('AKAMAI',
          'top-games by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  apiManager.run('topGames', {
    brand: item.brand
  });
});

TopGames.schema.post('remove', item => {
  apiManager.run('topGames', {
    brand: item.brand
  });
});

TopGames.defaultColumns = 'imageTitle, categoryId, alt, filename, targetUri, disabled, showInMenu';
TopGames.register();
