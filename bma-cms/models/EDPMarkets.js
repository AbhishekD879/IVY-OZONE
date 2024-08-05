'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),

  EDPMarkets = new keystone.List('edpMarket', {
    map: { name: 'name' },
    label: 'EDP Markets',
    sortable: true,
    track: true
  });

EDPMarkets.add({
  name: { type: String, required: true, label: 'Market Name' },
  lastItem: { type: Types.Boolean, default: false },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true }
});

function regenCache(brand) {
  apiManager.run('edpMarkets', { brand });
}

EDPMarkets.schema.pre('save', function(next) {
  EDPMarkets.model.find({ lastItem: true }).exec()
    .then(markets => {
      if (markets.length > 0 && this.lastItem) {
        return next(new Error('Last Item is already selected.'));
      }
      return next();
    })
    .catch(err => {
      next(new Error(err));
    });
});

EDPMarkets.schema.post('save', item => {
  return regenCache(item.brand);
});

EDPMarkets.schema.post('remove', item => regenCache(item.brand));

EDPMarkets.defaultColumns = 'name, marketId, lastItem';
EDPMarkets.register();
