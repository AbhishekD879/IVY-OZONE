export const SPORT_TAB_TIME_FILTER = 'time';
export const SPORT_TAB_LEAGUE_FILTER = 'league';

export const SPORT_TAB_FILTERS_CONFIG = {
  [SPORT_TAB_TIME_FILTER]: {
    tabs: ['matches', 'competitions'],
    params: {
      pattern: /^([1-9]|[1-6][0-9]|7[0-2])$/,
      validationMessage: 'Values between 1 and 72 are allowed',
      defaults: ['1', '3', '6', '12', '24', '48'],
      templateName: `${SPORT_TAB_TIME_FILTER}-filter`
    }
  },
  [SPORT_TAB_LEAGUE_FILTER]: {
    tabs: ['matches'],
    params: {
      tableColumns: [
        { name: 'Filter Name', property: 'leagueName' },
        { name: 'LeagueIDs', property: 'leagueIds' }
      ],
      searchBy: ['leagueName'],
      templateName: `${SPORT_TAB_LEAGUE_FILTER}-filter`
    }
  }
};
