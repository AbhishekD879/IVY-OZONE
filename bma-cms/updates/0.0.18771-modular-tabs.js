'use strict';

const fieldsByDirectives = {
  Featured : { ID: 'tab-featured', url: '#/home/featured' },
  Coupons : { ID: 'tab-coupons', url: '#/home/coupons' },
  InPlay : { ID: 'tab-in-play', url: '#/home/in-play' },
  LiveStream : { ID: 'tab-live-stream', url: '#/home/live-stream' },
  Multiples : { ID: 'tab-multiples', url: '#/home/multiples' },
  NextRaces : { ID: 'tab-next-races', url: '#/home/next-races' },
  TopBets : { ID: 'tab-top-bets', url: '#/home/top-bets' }
},
keystone = require('../bma-betstone'),
ModuleRibbonTabs = keystone.list('ModuleRibbonTabs').model.find().exec();

module.exports = function(next) {
  ModuleRibbonTabs.then(tabs => Promise.all(tabs.map(extrapolateRibbonTabsModels))).then(_ => next(), next);
};

function extrapolateRibbonTabsModels(tab) {
  if (tab.directiveName && tab.directiveName in fieldsByDirectives)  {
    Object.assign(tab, fieldsByDirectives[tab.directiveName]);
  }
  return tab.save();
}
