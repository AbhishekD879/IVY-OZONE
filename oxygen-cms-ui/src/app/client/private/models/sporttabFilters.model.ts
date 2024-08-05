export interface SportTabFilters {
  time?: SportTabFilter<string>;
  league?: SportTabFilter<SportTabLeagueFilterValue>;
}

export interface SportTabLeagueFilterValue {
  leagueName: string;
  leagueIds: string[];
}

export interface SportTabFilter<T> {
  enabled: boolean;
  values: T[];
}

export interface SportTabFilterInstance<T> {
  name: string;
  data: SportTabFilter<T>;
  params: { [key: string]: any };
}

export interface ISportTabPopularBetsFilter {
  isEnabled: boolean;
  displayName:string;
  time: number;
  isTimeInHours: boolean;
  isDefault?: boolean;
}