export interface IQuickbetSelectionPriceModel {
  id?: string;
  priceDec?: number;
  priceDen?: number;
  priceNum?: number;
  priceType?: string;
  isPriceChanged?: boolean;
  isPriceUp?: boolean;
  isPriceDown?: boolean;
  priceTypeRef?: {
    id: string;
  };
  handicapValueDec?: string;
}
