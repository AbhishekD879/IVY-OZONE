export interface IUkTotePotBetConfig {
  MULTIPLE_LEGS_TOTE_BETS: Array<string>;
  SUSPENDED_STATUS_CODE: string;
  channelName: {
    event: string;
    market: string;
    selection: string;
  };
  displayOrder: Array<string>;
  poolTypesMap: { [key: string]: { name: string, path: string } };
  scoopSixPoolType: string;
  toteBetsToExcludeFavourites: Array<string>;
}
