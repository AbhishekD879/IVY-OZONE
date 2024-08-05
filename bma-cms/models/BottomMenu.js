const keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),
  Types = keystone.Field.Types,

  BottomMenu = new keystone.List('bottomMenu', {
    map: { name: 'linkTitle' },
    autokey: { from: 'linkTitle brand', path: 'linkTitle_brand', unique: true },
    sortable: true,
    track: true
  });

BottomMenu.add({
  linkTitle: { type: String, required: true, initial: true, unique: false },
  targetUri: { type: String, required: false, default: '', initial: true, unique: false },
  section: {
    type: Types.Select,
    required: true,
    initial: true,
    options: 'help, quickLinks',
    default: 'help',
    emptyOption: false
  },
  disabled: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  inApp: { type: Types.Boolean, default: true },
  authRequired: { type: Types.Boolean, label: 'Authentication Required', default: false },
  systemID: { type: Types.Number, label: 'SystemID' }
});

BottomMenu.schema.pre('save', function(next) {
  if (this._req_user && this._req_user.brandCode) {
    this.brand = this._req_user.brandCode;
  }
  next();
});

function regenCache(brand) {
  apiManager.run('bottomMenu', { brand });
  initialDataManager.regenCache(brand);
}

BottomMenu.schema.post('save', item => regenCache(item.brand));

BottomMenu.schema.post('remove', item => regenCache(item.brand));

BottomMenu.defaultColumns = 'linkTitle, targetUri, inApp, section, disabled, authRequired';
BottomMenu.register();
