'use strict';

const keystone = require('../bma-betstone'),
  path = require('path'),
  fs = require('fs'),
  Types = keystone.Field.Types,
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),

  BetReceiptBannerTablet = new keystone.List('betReceiptBannerTablet', {
    map: { name: 'name' },
    label: 'Bet Receipt Banners Tablet',
    sortable: true,
    track: true
  });

BetReceiptBannerTablet.add({
  name: { type: String, required: true },
  filename: {
    type: Types.AkamaiFile,
    dest: 'images/uploads/betReceiptBannersTablet',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  description: { type: Types.Text },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },
  disabled: { type: Types.Boolean, default: false },
  uriMedium: { type: Types.Url, hidden: true },
  uriOriginal: { type: Types.Url, hidden: true }
});

function preUpload(item, file, options, next) {
  if (item.uriMedium) {
    akamai.deleteModelFields(item, ['uriOriginal', 'uriMedium']).then(
      () => uploadNew(item, file, options, next),
      next
    );
  } else {
    uploadNew(item, file, options, next);
  }
}

function uploadNew(item, file, options, next) {
  const widthMedium = item.widthMedium = 720,
    heightMedium = item.heightMedium = 170,
    mediumImagePath = path.join(
      options.dest,
      'medium',
      `${path.basename(file.name, path.extname(file.name))}-${widthMedium}x${heightMedium}${path.extname(file.name)}`
    ),
    originalImagePath = path.join(
      options.dest,
      path.basename(file.name, path.extname(file.name)) + path.extname(file.name)
    );

  item.uriMedium = mediumImagePath;
  item.uriOriginal = originalImagePath;

  thumbnailGenerator.generateThumb(file.path, { width: widthMedium, height: heightMedium }, (err, destination) => {
    if (err) {
      next(err);
    }
    akamai.upload(item.brand, fs.createReadStream(destination), mediumImagePath, error => {
      if (error) {
        next(error);
      }
      next();
    });
  });
}

BetReceiptBannerTablet.schema.path('validityPeriodStart').validate((value, respond) => {
  if (this.validityPeriodStart > this.validityPeriodEnd) {
    respond(false);
  } else {
    respond(true);
  }
}, 'Start date should be less or equal to End date');

BetReceiptBannerTablet.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  if (!this.filename.filename && this.uriMedium) {
    // Remove uriMedium only because uriOriginal is removed in AkamaiFileType
    // TODO: fix this split of logic between models and AkamaiFileType
    akamai.deleteModelFields(this, ['uriMedium']).then(
      () => {
        this.uriOriginal = '';
        next();
      },
      next
    );
  } else {
    next();
  }
});

BetReceiptBannerTablet.schema.pre('remove', function(next) {
  if (this.uriMedium) {
    akamai.deleteModelFields(this, ['uriOriginal', 'uriMedium']).then(
      () => next(),
      next
    );
  } else {
    next();
  }
});

function regenCache(brand) {
  apiManager.run('betReceiptBannersTablet', { brand, modelName: 'betReceiptBannerTablet' });
}

BetReceiptBannerTablet.schema.post('save', item => regenCache(item.brand));

BetReceiptBannerTablet.schema.post('remove', item => regenCache(item.brand));

BetReceiptBannerTablet.defaultColumns = 'name, validityPeriodStart, validityPeriodEnd, disabled';
BetReceiptBannerTablet.register();
