import { IIdRef } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IPrice {
  priceDen: number;
  priceNum: number;

  externalKeys?: any;
  priceDec?: number | string;
  priceType?: string;
  doc?: string;
  priceTypeRef?: IIdRef;
}
