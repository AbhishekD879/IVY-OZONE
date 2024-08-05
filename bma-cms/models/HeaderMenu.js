const keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),
  Types = keystone.Field.Types,

  HeaderMenu = new keystone.List('headerMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

HeaderMenu.add({
  linkTitle: { type: String, required: true, initial: true, unique: false },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  disabled: { type: Types.Boolean, default: false, initial: true },
  inApp: { type: Types.Boolean, default: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  level: { type: Types.Select, options: ['1', '2'], default: '1', initial: true },
  parent: {
    type: Types.Relationship,
    dependsOn: {
      level: '2'
    },
    filters: { level: '1' },
    ref: 'headerMenu',
    initial: true
  }
});

HeaderMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }

  if (this.level === '1') {
    this.parent = null;
  }
  next();
});

HeaderMenu.schema.post('save', item => {
  apiManager.run('headerMenu', {
    brand: item.brand
  });
});

HeaderMenu.schema.post('remove', item => {
  apiManager.run('headerMenu', {
    brand: item.brand
  });
});

HeaderMenu.defaultColumns = 'linkTitle, targetUri, inApp, level, parent, disabled';
HeaderMenu.register();
