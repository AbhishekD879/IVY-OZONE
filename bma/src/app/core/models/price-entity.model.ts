import { IPrice } from '@core/models/price.model';

export interface IPriceEntity {
  price: IPrice;
  historicPrice?: any;
}
