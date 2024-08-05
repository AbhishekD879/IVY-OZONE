import { IPrice } from '@core/models/price.model';

export interface IOutcomePrice extends IPrice {
  priceType?: string;
  type?: string;
  props?: any;
  id?: string;
  isActive?: string;
  displayOrder?: string;
  isDisplayed?: boolean;

  // TODO: Dynamic properties remove dynamic param
  liveShowTimer?: any;
  handicapValueDec?: any;
  rawHandicapValue?: any;
  livePriceNum?: string;
  livePriceDec?: string;
  livePriceDen?: string;
}
