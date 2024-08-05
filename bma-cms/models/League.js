'use strict';

const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  apiManager = require('../lib/api'),

  League = new keystone.List('league', {
    map: { name: 'name' },
    sortable: true,
    track: true
  });

League.add({
  name: { type: String, required: true, label: 'League Title' },
  typeId: { type: Types.Number, initial: true, default: '' },
  categoryId: { type: Types.Number, initial: true, default: '' },
  ssCategoryCode: { type: String, required: false, label: 'SS Category Code' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  lang: { type: Types.Text, default: 'en', hidden: true },
  banner: { type: Types.Relationship, ref: 'betReceiptBanner', label: 'Mobile Banner', initial: true },
  tabletBanner: { type: Types.Relationship, ref: 'betReceiptBannerTablet', initial: true },
  betBuilderUrl: { type: Types.Url, label: 'BetBuilder URL', initial: true },
  leagueUrl: { type: Types.Text, initial: true },
  redirectionUrl: { type: Types.Text, label: 'Redirection URL', initial: true }
});

function regenCache(brand) {
  apiManager.run('leagues', { brand });
}

League.schema.post('save', item => regenCache(item.brand));

League.schema.post('remove', item => regenCache(item.brand));

League.defaultColumns = 'name, typeId, categoryId, ssCategoryCode, betBuilderUrl, leagueUrl, redirectionUrl, banner, tabletBanner';
League.register();
