export interface IOutputPrice {
  priceType: string;
  priceNum: number;
  priceDen: number;
  id?: string;
  priceDec?: number | string;
  handicapValueDec?: string;
  rawHandicapValue?: number;
}
