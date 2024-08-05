export interface IMarketSelectorConfig {
  SPORT_ID?: Number;
  DEFAULT_SELECTED_OPTION: string;
  MARKETS_NAMES: {
    [key: string]: string;
  };
  MARKETS_NAME_ORDER: string[];
}

export interface IMarketSelectorOption {
  name: string;
  text: string;
}

export interface IReloadData {
  useCache: boolean;
  additionalParams: {
    marketSelector: string;
  };
}

export interface ICouponMarketSelector {
  id?: string;
  title: string;
  templateMarketName: string;
  header?: string[];
}
