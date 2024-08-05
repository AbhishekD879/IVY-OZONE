import { ISportConfigEventMethods } from '@app/core/services/cms/models';

export const tier2EventMethods: ISportConfigEventMethods = {
  today: 'todayEventsByClasses',
  tomorrow: 'todayEventsByClasses',
  future: 'todayEventsByClasses',
  upcoming: 'todayEventsByClasses',
  antepost: 'todayEventsByClasses',
  coupons: 'coupons',
  outrights: 'outrights',
  live: 'blocker',
  results: 'results',
  specials: 'specials',
  allEvents: 'todayEventsByClasses',
  matchesTab: 'todayEventsByClasses'
};

export const tier1EventMethods: ISportConfigEventMethods = {
  ...tier2EventMethods,
  competitions: 'competitionsInitClassIds'
};

export const footballEventMethods: ISportConfigEventMethods = {
  ...tier1EventMethods,
  matches: 'blocker',
  jackpot: 'jackpot',
};

export const outrightsEventMethods: ISportConfigEventMethods = {
  ...tier2EventMethods,
  today: 'outrights',
  tomorrow: 'outrights',
  future: 'outrights',
  upcoming: 'outrights',
  antepost: 'outrights',
};

export const olympicsEventMethods: ISportConfigEventMethods = {
  ...tier2EventMethods,
  today: 'todayEventsByTypesIds',
  tomorrow: 'todayEventsByTypesIds',
  upcoming: 'todayEventsByTypesIds',
  antepost: 'todayEventsByTypesIds',
  specials: 'specials'
};
