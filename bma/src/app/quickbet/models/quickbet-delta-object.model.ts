export interface IQuickbetDeltaObjectModel {
  hcap_values?: IQuickbetDeltaHandicap;
  isPriceChanged?: boolean;
  isPriceDown?: boolean;
  isPriceUp?: boolean;
  priceDec?: number;
  priceDen?: number;
  priceNum?: number;
  priceType?: string;
  handicapValueDec?: string;
  ew_avail?: string;
}

export interface IQuickbetDeltaHandicap {
  A?: string;
  H?: string;
  L?: string;
}
