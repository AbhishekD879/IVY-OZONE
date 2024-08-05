'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  akamai = require('../bma-betstone/lib/akamai'),
  fs = require('fs'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  path = require('path'),

  SSOPage = new keystone.List('ssoPage', {
    map: { name: 'title' },
    autokey: { from: 'title brand', path: 'title_brand', unique: true },
    track: true,
    singular: 'SSO Page item',
    plural: 'SSO Page items',
    path: 'sso-page',
    sortable: true
  });

SSOPage.add({
  title: { type: Types.Text, required: true, initial: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive' },

  filename: {
    type: Types.AkamaiFile,
    dest: 'images/uploads/sso-page',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  uriOriginal: { type: Types.Url, hidden: true },
  uriMedium: { type: Types.Url, hidden: true },
  widthMedium: { type: Number, hidden: true },
  heightMedium: { type: Number, hidden: true },
  openLink: { type: Types.Text, default: '', initial: true },
  showOnAndroid: { type: Types.Boolean, default: false, initial: true },
  targetAndroid: { type: Types.Text, label: 'Target Android', dependsOn: { showOnAndroid: true }, initial: true },
  showOnIOS: { type: Types.Boolean, label: 'Show on iOS', default: false, initial: true },
  targetIOS: { type: Types.Text, label: 'Target iOS', dependsOn: { showOnIOS: true }, initial: true }
});

SSOPage.schema.pre('save', function(next) {
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

SSOPage.schema.post('save', regenCache);

SSOPage.schema.pre('remove', function(next) {
  if (this.uriMedium) {
    akamai.deleteModelFields(this, ['uriOriginal', 'uriMedium']).then(
      () => next(),
      next
    );
  } else {
    next();
  }
});

SSOPage.schema.post('remove', regenCache);

function regenCache(item) {
  ['ios', 'android'].forEach(os => {
    apiManager.run('ssoPage', {
      brand: item.brand,
      osType: os
    });

    // Solution for a need to keep 'retail' brand
    if (item.brand === 'connect') {
      apiManager.run('ssoPage', { brand: 'retail', osType: os });
    }
  });
}

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
  const
    widthMedium = item.widthMedium = 160,
    heightMedium = item.heightMedium = 160,
    mediumImagePath = path.join(
      options.dest,
      'medium',
      `${path.basename(file.name, path.extname(file.name))}-${widthMedium}x${heightMedium}${path.extname(file.name)}`
    ),
    originalImagePath = path.join(
      options.dest,
      path.basename(file.name, path.extname(file.name)) + path.extname(file.name));

  item.uriMedium = mediumImagePath;
  item.uriOriginal = originalImagePath;

  thumbnailGenerator.generateThumb(file.path, { width: widthMedium, height: heightMedium }, (generationErr, destination) => {
    if (generationErr) {
      next({ message: generationErr });
    }
    akamai.upload(item.brand, fs.createReadStream(destination), mediumImagePath, err => {
      if (err) {
        next({ message: err });
      }
      next();
    });
  });
}

SSOPage.defaultColumns = 'title, disabled, openLink, showOnIOS, targetIOS, showOnAndroid, targetAndroid';
SSOPage.register();
