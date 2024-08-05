const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  path = require('path'),
  fs = require('fs'),
  thumbnailGenerator = require('../bma-betstone/lib/thumbnailGenerator'),
  async = require('async'),
  akamai = require('../bma-betstone/lib/akamai'),
  apiManager = require('../lib/api'),
  Q = require('q'),
  utils = require('../lib/utils'),
  Logger = require('../lib/logger'),

  Offer = new keystone.List('offer', {
    map: { name: 'name' },
    sortable: true,
    track: true
  });

Offer.add({
  name: { type: String, required: true },
  displayFrom: { type: Types.Datetime, required: true, initial: true },
  displayTo: { type: Types.Datetime, required: true, initial: true },
  image: {
    type: Types.AkamaiFile,
    dest: 'img/offers',
    allowedTypes: ['image/jpeg', 'image/png', 'image/jpg'],
    pre: { upload: preUpload }
  },
  useDirectImageUrl: { type: Types.Boolean, default: false, label: 'Use Image URL' },
  directImageUrl: { type: Types.Url, label: 'Image URL' },
  imageUri: { type: String, hidden: true },
  targetUri: { type: Types.Text, required: true, initial: true },
  showOfferOn: {
    type: Types.Select,
    options: [
      { value: 'desktop', label: 'Desktop' },
      { value: 'tablet', label: 'Tablet' },
      { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false
  },
  showOfferTo: {
    type: Types.Select,
    options: [
      { value: 'new', label: 'New User' },
      { value: 'existing', label: 'Existing User' },
      { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false,
    initial: true
  },
  vipLevelsInput: { type: Types.Text, initial: true, label: 'Include VIP Levels' },
  disabled: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  module: { type: Types.Relationship, ref: 'offerModule', required: true, initial: true }
});

Offer.schema.add({
  vipLevels: []
});

function preUpload(item, file, options) {
  const imageWidth = item.imageWidth = 290,
    imageHeight = item.imageHeight = 180,
    imageUri = path.join(
      options.dest,
      'medium',
      `${path.basename(file.name, path.extname(file.name))}-${imageWidth}x${imageHeight}${path.extname(file.name)}`
    );

  item.imageUri = imageUri;

  async.series([
    function(callback) {
      thumbnailGenerator.generateThumb(file.path, { width: imageWidth, height: imageHeight }, (err, destination) => {
        if (err) {
          callback(err, null);
        } else {
          const stream = fs.createReadStream(destination);
          akamai.upload(item.brand, stream, imageUri, callback);
        }
      });
    }
  ], err => {
    if (err) {
      Logger.error('AKAMAI', err);
    }
  });
}

Offer.schema.path('vipLevelsInput').validate(function() {
  if (this.vipLevelsInput !== '' && !utils.validateRange(this.vipLevelsInput)) {
    this.invalidate('vipLevelsInput', 'VIP Levels Range has incorrect format');
  }
}, 'VIP Levels Range has incorrect format');

Offer.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  this.vipLevels = (this.vipLevelsInput && this.vipLevelsInput !== '') ? utils.getListByRange(this.vipLevelsInput) : [];

  next();
});

function regenCache(brand) {
  const promises = [],
    deviceTypes = ['tablet', 'desktop'];

  deviceTypes.forEach(deviceType => {
    promises.push(
      apiManager.run('offersV2', {
        brand,
        deviceType
      })
    );
  });

  return Q.all(promises);
}

Offer.schema.post('save', doc => {
  regenCache(doc.brand);
});

Offer.schema.post('remove', doc => {
  regenCache(doc.brand);
});

Offer.defaultColumns = 'name, module, displayFrom, displayTo, showOfferOn, showOfferTo, disabled, vipLevelsInput';
Offer.register();
