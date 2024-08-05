const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  cacheManager = require('../lib/cacheManager'),

  YCStaticBlock = new keystone.List('ycStaticBlock', {
    map: { name: 'title' },
    label: 'YourCall Static Block',
    autokey: { from: 'title brand', path: 'title_brand', unique: true },
    track: true
  });

YCStaticBlock.add({
  title: { type: String, required: true },
  htmlMarkup: { type: Types.Html, wysiwyg: true, height: 150 },
  enabled: { type: Types.Boolean, default: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

YCStaticBlock.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  next();
});

YCStaticBlock.schema.post('save', item => {
  apiManager.run('ycStaticBlock', {
    brand: item.brand,
    uri: item.uri
  });
});

YCStaticBlock.schema.post('remove', item => {
  cacheManager.removeCache('ycStaticBlock', {
    brand: item.brand,
    uri: item.uri
  });
});

YCStaticBlock.defaultColumns = 'title, htmlMarkup, enabled';
YCStaticBlock.register();
