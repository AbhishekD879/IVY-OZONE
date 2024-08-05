import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { SportsLegPriceModel } from './sports-leg-price';
import { IPrice as IBasePrice } from '@core/models/price.model';
import { IPrice } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Injectable({ providedIn: BetslipApiModule })
export class SportsLegPriceService {
  constructor() {
  }

  construct(data: IBasePrice): SportsLegPriceModel {
    return new SportsLegPriceModel(data);
  }

  parse(someDoc: IBasePrice) {
    return new SportsLegPriceModel({
      priceNum: someDoc.priceNum,
      priceDen: someDoc.priceDen,
      priceType: <string>someDoc.priceTypeRef.id
    });
  }

  convert(obj: IPrice): IBasePrice {
    return obj && {
      priceNum: obj.num,
      priceDen: obj.den,
      priceType: obj.type
    };
  }
}
