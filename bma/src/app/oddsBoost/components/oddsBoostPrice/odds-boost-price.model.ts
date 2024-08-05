export interface IPrice {
  decimal?: number|string;
  num?: number|string;
  den?: number|string;
}

export interface IPriceRangeItem {
  divider?: string;
  range?: (number|string)[];
  scrollUp?: boolean;
}
