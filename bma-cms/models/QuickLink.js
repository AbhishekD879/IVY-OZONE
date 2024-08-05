const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  path = require('path'),
  async = require('async'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  akamai = require('../bma-betstone/lib/akamai'),
  fs = require('fs'),
  apiManager = require('../lib/api'),
  Logger = require('../lib/logger'),

  QuickLink = new keystone.List('quickLink', {
    label: 'HR Quick Links',
    map: { name: 'title' },
    sortable: true
  });

QuickLink.add({
  title: { type: String, required: true },
  body: { type: Types.Textarea, required: true, initial: true },
  raceType: {
    type: Types.Select,
    options: [
      { value: 'horseracing', label: 'Horse Racing' },
      { value: 'greyhound', label: 'Greyhound Racing' }
    ],
    default: 'horseracing',
    emptyOption: false,
    initial: true,
    required: true
  },
  filename: {
    type: Types.AkamaiFile,
    label: 'Icon',
    dest: 'images/uploads/quick-links',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  linkType: {
    type: Types.Select,
    options: [
      { value: 'url', label: 'URL' },
      { value: 'selection', label: 'Selection' }
    ],
    default: 'url',
    emptyOption: false,
    initial: true,
    required: true
  },
  target: { type: String, required: true, initial: true, label: 'URL or Selection ID' },
  validityPeriodStart: { type: Types.Datetime, required: true, initial: true },
  validityPeriodEnd: { type: Types.Datetime, required: true, initial: true },

  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive', index: true },
  uriMedium: { type: Types.Url, hidden: true },
  widthMedium: { type: Types.Number, hidden: true },
  heightMedium: { type: Types.Number, hidden: true }
});

QuickLink.schema.path('validityPeriodStart').validate(function(value, respond) {
  if (this.validityPeriodStart > this.validityPeriodEnd) {
    respond(false);
  } else {
    respond(true);
  }
}, 'Start date should be less or equal to End date');

function preUpload(item, file, options) {
  const widthMedium = item.widthMedium = 160,
    heightMedium = item.heightMedium = 160,
    mediumImagePath = path.join(
      options.dest,
      'medium',
      `${path.basename(file.name, path.extname(file.name))}-${widthMedium}x${heightMedium}${path.extname(file.name)}`
    );

  item.uriMedium = mediumImagePath;

  async.series([
    function(callback) {
      thumbnailGenerator.generateThumb(file.path, { width: widthMedium, height: heightMedium }, (err, destination) => {
        if (err) {
          callback(err, null);
        } else {
          const stream = fs.createReadStream(destination);
          akamai.upload(item.brand, stream, mediumImagePath, callback);
        }
      });
    }
  ], err => {
    if (err) {
      Logger.error('AKAMAI', err);
    }
  });
}

QuickLink.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  next();
});

QuickLink.schema.post('save', item => {
  apiManager.run('quickLinks', {
    brand: item.brand,
    raceType: item.raceType
  });
});

QuickLink.schema.post('remove', item => {
  apiManager.run('quickLinks', {
    brand: item.brand,
    raceType: item.raceType
  });
});

QuickLink.defaultColumns = 'title, raceType, linkType, target, validityPeriodStart, validityPeriodEnd, disabled';
QuickLink.register();
