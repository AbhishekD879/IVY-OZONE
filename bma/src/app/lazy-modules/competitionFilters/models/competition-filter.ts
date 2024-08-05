export interface ICompetitionFilter {
  id: string;
  active: boolean;
  name: string; // e.g. Top Leagues | 1h
  type: string; // From FILTER_TYPES
  value: number | number[];  // e.g. [442, 443] | 1
}

export enum FILTER_TYPES {
  TIME = 'TIME',
  LEAGUE = 'LEAGUE'
}

