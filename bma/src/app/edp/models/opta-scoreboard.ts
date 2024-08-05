export interface IOptaScoreboardEndpoints {
  prematch: string;
  bymapping: string;
}

export interface IOptaScoreboardConfig {
  apiKeys: Object | string;
  endpoints: IOptaScoreboardEndpoints;
}
