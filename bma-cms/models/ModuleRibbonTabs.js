const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),
  Logger = require('../lib/logger'),

  moduleRibbonTabs = new keystone.List('ModuleRibbonTabs', {
    map: { name: 'title' },
    autokey: { from: 'title brand', path: 'title_brand', unique: true },
    sortable: true,
    track: true
  });

moduleRibbonTabs.add({
  title: { type: Types.Text },
  directiveName: {
    type: Types.Select,
    options: 'Featured, Coupons, InPlay, LiveStream, Multiples, NextRaces, TopBets',
    default: 'Featured',
    emptyOption: false,
    initial: true
  },
  ID: { type: Types.Text, noedit: true, label: 'ID', initial: true, required: true },
  url: { type: Types.Text, noedit: true, label: 'URL', initial: true, required: true },
  visible: { type: Types.Boolean, default: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  showTabOn: {
    type: Types.Select,
    options: [
                          { value: 'desktop', label: 'Desktop' },
                          { value: 'mobtablet', label: 'Mobile/Tablet' },
                          { value: 'both', label: 'Both' }
    ],
    default: 'both',
    emptyOption: false
  },
  lang: { type: Types.Text, default: 'en', hidden: true },
  devices: {
    ios: { type: Types.Boolean, default: true, label: 'ios' },
    android: { type: Types.Boolean, default: true, label: 'android' },
    wp: { type: Types.Boolean, default: true, label: 'Windows Phone' }
  }
});

moduleRibbonTabs.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  next();
});

moduleRibbonTabs.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'module-ribbon-tabs by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  apiManager.run('modularContent', { brand: item.brand });
});

moduleRibbonTabs.schema.post('remove', item => {
  apiManager.run('modularContent', { brand: item.brand });
});

moduleRibbonTabs.defaultColumns = 'title, directiveName, visible, showTabOn';
moduleRibbonTabs.register();
