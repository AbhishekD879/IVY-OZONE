import { Injectable } from '@angular/core';

import { SPORT_INPLAY } from '@platform/shared/components/marketSelector/market-selector.constant';

import { IMarketSelectorConfig } from '@shared/components/marketSelector/market-selector.model';

@Injectable()
export class MarketSelectorConfigService {
  sportInplay: IMarketSelectorConfig[];

  private SPORT_INPLAY = SPORT_INPLAY;
  constructor() {
    this.sportInplay = this.SPORT_INPLAY;
  }
}
