'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  utils = require('../lib/utils'),
  apiManager = require('../lib/api'),
  spriteManager = require('../lib/spriteManager'),

  DesktopQuickLink = new keystone.List('Desktop QuickLink', {
    map: { name: 'title' },
    sortable: true
  });

DesktopQuickLink.add({
  title: { type: String, required: true },
  filename: { type: Types.LocalFile, label: 'Icon', dest: 'public/images/uploads', allowedTypes: ['image/png'] },
  target: { type: String, required: true, initial: true, label: 'URL' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive', index: true },
  uriSmall: { type: String, hidden: true },
  widthSmall: { type: Number, hidden: true },
  heightSmall: { type: Number, hidden: true },
  uriMedium: { type: Types.Url, hidden: true },
  widthMedium: { type: Types.Number, hidden: true },
  heightMedium: { type: Types.Number, hidden: true },
  uriLarge: { type: Types.Url, hidden: true },
  widthLarge: { type: Types.Number, hidden: true },
  heightLarge: { type: Types.Number, hidden: true },
  spriteClass: { type: String, hidden: true },
  collectionType: { type: String, hidden: true, default: '/desktop_quick_links/' }
});

DesktopQuickLink.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  const tasks = [];

  this.spriteClass = this.title.replace(utils.regExp, '');

  if (this.brand !== 'bma') {
    this.spriteClass = `${this.brand}_${this.spriteClass}`;
  }

  // TODO: If small size will not be used - it should be removed here and made optional in spriteManager
  this.widthSmall = this.heightSmall = 1;

  this.widthMedium = this.heightMedium = 160;

  this.widthLarge = this.heightLarge = 480;

  if (this.filename && this.filename.filename) {
    tasks.push(spriteManager.createSizes(this, 'filename'));
  } else {
    tasks.push(spriteManager.removeSizes(this, 'filename'));
  }

  if (tasks.length > 0) {
    Promise.all(tasks)
      .then(
        () => next(),
        next
      );
  } else {
    next();
  }
});

DesktopQuickLink.schema.pre('remove', function(next) {
  spriteManager.removeSizes(this, 'filename')
    .then(
      () => next(),
      next
    );
});

DesktopQuickLink.schema.post('save', item => regenCache(item.brand));

DesktopQuickLink.schema.post('remove', item => regenCache(item.brand));

function regenCache(brand) {
  apiManager.run('desktopQuickLinks', { brand });
}

DesktopQuickLink.defaultColumns = 'title, target, disabled';
DesktopQuickLink.register();
