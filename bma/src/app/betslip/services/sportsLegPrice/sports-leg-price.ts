import * as _ from 'underscore';

import { IDocSportsLegPriceModel } from './sports-leg-price.model';
import { IPrice } from '@core/models/price.model';

export class SportsLegPriceModel {

  data: IPrice;

  constructor(data: IPrice) {
    this.data = data;
  }

  get num(): number {
    return this.toNum(this.data.priceNum);
  }
  set num(value:number){}
  get den(): number {
    return this.toNum(this.data.priceDen);
  }
  set den(value:number){}
  get type(): string {
    return this.data.priceType;
  }
  set type(value:string){}
  get props(): IPrice {
    return this.data;
  }

  set props(props: IPrice) {
    _.extend(this.data, props);
  }


  toNum(arg: string | number): number {
    return arg && Number(arg);
  }

  doc(isPlacingBet: boolean, hasBPG: boolean): IDocSportsLegPriceModel {
    const priceAttr = this.type === 'SP'
      ? {}
      : _.pick({ num: this.num, den: this.den },
        val => !_.isUndefined(val)),
      price = {
        price: _.extend(priceAttr, {
          priceTypeRef: {
            id: (isPlacingBet && this.type === 'LP' && hasBPG) ? 'GUARANTEED'
              : this.type
          }
        })
      };

    return price;
  }
}
