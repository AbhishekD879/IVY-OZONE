/**
 * inplay config for sport tabs
 */
export const inplayConfig = {
  moduleName: 'inplay',
  expandedSportsCount: 1,
  expandedLeaguesCount: 3,
  viewByFilters: [
    'livenow',
    'upcoming'
  ]
};

/**
 * inplay config for 'Watch Live' tab
 */
export const inplayLiveStreamConfig = {
  expandedSportsCount: 1,
  viewByFilters: [
    'liveStream',
    'upcomingLiveStream'
  ]
};

/**
 * inplay config for caching data of sport tabs and watch live tab
 */
export const inplayCacheConfig = {
  cacheInterval: 30 * 1000, // 30 sec
  sportCacheInterval: 5 * 1000, // 5 sec
  viewByFilters: [
    'liveStream',
    'livenow',
    'upcoming',
    'upcomingLiveStream'
  ]
};
