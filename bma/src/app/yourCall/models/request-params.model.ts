export interface IYourcallAPIRequestData {
  path: string;
  method?: string;
  params?: any; // request query params
}

export interface IBYBPostRequestData extends IYourcallAPIRequestData {
  method: string;
  params: any;
}

export interface IBYBLeaguesPeriod {
  dateFrom: string;
  dateTo: string;
}

export interface IEmptyMethodResult {
  resolve: {
    data?: any;
  };
}

export interface IGetMarketSelectionsParams {
  marketIds: string;
  obEventId: number;
}

export interface IYourcallPlayerStatisticParams {
  obEventId: string;
  playerId: number;
}

export interface IYourcalStatValuesParams  extends IYourcallPlayerStatisticParams {
  statId: number;
}
