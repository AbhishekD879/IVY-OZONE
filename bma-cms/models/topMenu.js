const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  Logger = require('../lib/logger'),

  TopMenu = new keystone.List('topMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

TopMenu.add({
  linkTitle: { type: String, required: true },
  targetUri: { type: String, required: true, initial: true },
  disabled: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

TopMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  next();
});

TopMenu.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'top-menu by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  // TODO: call api for old brand, if brand value was changed
  apiManager.run('topMenu', {
    brand: item.brand
  });
});

TopMenu.schema.post('remove', item => {
  apiManager.run('topMenu', {
    brand: item.brand
  });
});

TopMenu.defaultColumns = 'linkTitle, targetUri, disabled';
TopMenu.register();
