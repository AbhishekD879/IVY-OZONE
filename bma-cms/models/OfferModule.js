const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  Q = require('q'),

  OfferModule = new keystone.List('offerModule', {
    map: { name: 'name' },
    sortable: true,
    track: true
  });

OfferModule.add({
  name: { type: String, required: true, initial: true },
  showModuleOn: {
    type: Types.Select,
    options: [
      { value: 'desktop', label: 'Desktop' },
      { value: 'tablet', label: 'Tablet' },
      { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false
  },
  disabled: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true }
});

OfferModule.relationship({ path: 'offers', ref: 'offer', refPath: '_id' });

OfferModule.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

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

OfferModule.schema.post('save', doc => {
  regenCache(doc.brand);
});

OfferModule.schema.post('remove', doc => {
  regenCache(doc.brand);
});

OfferModule.defaultColumns = 'name, showModuleOn, disabled';
OfferModule.register();
