const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  cacheManager = require('../lib/cacheManager'),
  Logger = require('../lib/logger'),

  StaticBlock = new keystone.List('staticBlock', {
    map: { name: 'title' },
    autokey: { from: 'title brand', path: 'title_brand', unique: true },
    track: true
  });

StaticBlock.add({
  title: { type: String, required: true },
  uri: { type: String, required: true, initial: true },
  htmlMarkup: { type: Types.Html, wysiwyg: true, height: 150 },
  enabled: { type: Types.Boolean, default: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

StaticBlock.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  next();
});

StaticBlock.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'static-blocks by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  apiManager.run('staticBlock', {
    brand: item.brand,
    uri: item.uri
  });
});

StaticBlock.schema.post('remove', item => {
  cacheManager.removeCache('staticBlock', {
    brand: item.brand,
    uri: item.uri
  });
});

StaticBlock.defaultColumns = 'title, uri, htmlMarkup, enabled';
StaticBlock.register();
