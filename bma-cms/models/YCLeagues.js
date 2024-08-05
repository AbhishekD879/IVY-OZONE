'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),

  YCLeague = new keystone.List('ycLeague', {
    map: { name: 'name' },
    label: 'YourCall Leagues',
    sortable: true,
    track: true
  });

YCLeague.add({
  name: { type: String, required: true, label: 'League Title' },
  typeId: { type: Types.Number, initial: true, default: '' },
  enabled: { type: Types.Boolean, default: true },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

function regenCache(brand) {
  apiManager.run('ycLeagues', { brand });
}

YCLeague.schema.post('save', item => regenCache(item.brand));

YCLeague.schema.post('remove', item => regenCache(item.brand));

YCLeague.defaultColumns = 'name, typeId, enabled';
YCLeague.register();
