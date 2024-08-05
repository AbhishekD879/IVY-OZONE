'use strict';

const keystone = require('../bma-betstone'),
  path = require('path'),
  fs = require('fs'),
  Types = keystone.Field.Types,
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),

  MaintenancePage = new keystone.List('maintenancePage', {
    map: { name: 'name' },
    track: true
  });

MaintenancePage.add({
  name: { type: String, required: true },
  filename: {
    type: Types.AkamaiFile,
    dest: 'images/uploads/maintenance-page',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },
  uriMedium: { type: Types.Url, hidden: true },
  uriOriginal: { type: Types.Url, hidden: true },
  mobile: { type: Types.Boolean, default: false },
  tablet: { type: Types.Boolean, default: false },
  desktop: { type: Types.Boolean, default: false }
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
  const widthMedium = item.widthMedium = 1057,
    heightMedium = item.heightMedium = 1136,
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
      next({ message: err });
    }
    akamai.upload(item.brand, fs.createReadStream(destination), mediumImagePath, error => {
      if (error) {
        next({ message: error });
      }
      next();
    });
  });
}

MaintenancePage.schema.path('validityPeriodStart').validate((value, respond) => {
  if (this.validityPeriodStart > this.validityPeriodEnd) {
    respond(false);
  } else {
    respond(true);
  }
}, 'Start date should be less or equal to End date');

MaintenancePage.schema.pre('save', function(next) {
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

MaintenancePage.schema.pre('remove', function(next) {
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
  ['desktop', 'mobile', 'tablet'].forEach(deviceType => {
    apiManager.run('maintenancePage', { brand, deviceType });
  });
}

MaintenancePage.schema.post('save', item => regenCache(item.brand));

MaintenancePage.schema.post('remove', item => regenCache(item.brand));

MaintenancePage.defaultColumns = 'name, targetUri, validityPeriodStart, validityPeriodEnd, mobile, tablet, desktop, disabled';
MaintenancePage.register();
