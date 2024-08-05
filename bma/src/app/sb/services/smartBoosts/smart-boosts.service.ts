import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IMarket } from '@core/models/market.model';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Injectable()
export class SmartBoostsService {
  private readonly smartBoostsTags = ['MKTFLAG_PR1', 'MKTFLAG_PB'];

  constructor(private fracToDecService: FracToDecService) {}

  isSmartBoosts(market: IMarket): boolean {
    const marketDrilldownTagNames: string[] = market.drilldownTagNames ? market.drilldownTagNames.split(',') : [];
    return _.intersection(marketDrilldownTagNames, this.smartBoostsTags).length > 0;
  }

  parseName(name: string): { name: string, wasPrice: string } {
    const regExp = /(.*?)\s*\(was\s*(\d*)\/(\d*)\)\s*(.*)/i;
    const parsedName = regExp.exec(name);

    if (!parsedName) {
      return { name, wasPrice: '' };
    }

    const wasPrice = this.fracToDecService
      .getFormattedValue(Number(parsedName[2]), Number(parsedName[3]))
      .toString();

    return { name: `${parsedName[1]} ${parsedName[4]}`, wasPrice };
  }
}
