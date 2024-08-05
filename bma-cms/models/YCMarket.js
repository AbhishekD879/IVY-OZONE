'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),

  YCMarket = new keystone.List('ycMarket', {
    map: { name: 'name' },
    label: 'YourCall Markets',
    sortable: true,
    track: true
  });

YCMarket.add({
  name: { type: String, required: true, label: 'Market' },
  dsMarket: { type: String, initial: true, default: '', label: 'DS Market' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

function regenCache(brand) {
  apiManager.run('ycMarkets', { brand });
}

YCMarket.schema.post('save', item => regenCache(item.brand));

YCMarket.schema.post('remove', item => regenCache(item.brand));

YCMarket.defaultColumns = 'name, dsMarket';
YCMarket.register();
