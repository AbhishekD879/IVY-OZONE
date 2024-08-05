export interface IYourcallMappedMarket {
  title?: string;
  type: IYourcallMappedMarketType;
  multi?: boolean;
  edit?: boolean;
  unit?: string;
}

export interface IYourcallMappedMarketType {
  [key: string]: string;
}
