import { horseracingConfig } from '@core/services/racing/config/horseracing.config';

horseracingConfig.GROUPED_MARKETS_NAME = ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish',
  'Top 3 Finish', 'Top 4 Finish', 'Top 2', 'Top 3', 'Top 4', 'To Finish 2nd', 'To Finish 3rd', 'Place Insurance 2',
  'Place Insurance 3', 'Place Insurance 4'];
horseracingConfig.MARKETS_NAME_SORT_ORDER = ['', 'Win or Each Way', 'Win Only', 'Betting Without', 'Place Only',
  'To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish',
  'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4', 'Insurance - Place 2', 'Insurance - Place 3',
  'Insurance - Place 4'];
horseracingConfig.GROUPED_MARKETS_NAME = ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish',
  'Top 3 Finish', 'Top 4 Finish', 'Top 2', 'Top 3', 'Top 4', 'To Finish 2nd', 'To Finish 3rd',
  'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places',
  'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
  'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4'];
horseracingConfig.tabs = [
  { id: 'tab-featured', label: 'sb.tabsNameFeatured', url: '/horse-racing/featured' },
  { id: 'tab-races', label: 'sb.tabsNameNext', url: '/horse-racing/races/next' },
  { id: 'tab-future', label: 'sb.tabsNameAntepost', url: '/horse-racing/future' },
  { id: 'tab-specials', label: 'sb.tabsNameSpecials', url: '/horse-racing/specials' },
];
horseracingConfig.config.eventMethods = {
  featured: 'todayEventsByClasses',
  antepost: 'getAntepostEvents',
  today: 'todayEventsByClasses',
  tomorrow: 'todayEventsByClasses',
  future: 'todayEventsByClasses',
  results: 'results',
  past: 'results',
  specials: 'todayEventsByClasses',
  ms: 'getFeatured'
};
horseracingConfig.sectionTitle = {
  INT: 'sb.flagINTLong',
  UK: 'sb.flagUkLong',
  VR: 'sb.flagVRaces',
  US: 'sb.flagUSLong',
  ZA: 'sb.flagZALong',
  AE: 'sb.flagAELong',
  CL: 'sb.flagCLLong',
  IN: 'sb.flagINLong',
  AU: 'sb.flagAULong',
  FR: 'sb.flagFRLong',
  ALL: 'sb.flagALL',
  ENHRCS: 'sb.flagENHRCS'
};

horseracingConfig.config.tabs.specials = {
  hidden: true,
  isNotStarted: true,
  typeFlagCodes: 'SP',
  isNotResulted: true,
  limitOutcomesCount: 1,
  limitMarketCount: 1,
  excludeEventsClassIds: '',
  externalKeysEvent: false
};

export const ladbrokesHorseracingConfig = horseracingConfig;
