import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';

import { YOURCALL_BANACH_MARKETS } from '../../constants/yourcall-banach-markets';
import { YOURCALL_DATA_PROVIDER } from '../../constants/yourcall-data-provider';

import { YourCallMarketPlayer } from '../../models/markets/yourcall-market-player';
import { YourCallMarketGroupPlayer } from '../../models/markets/yourcall-market-group-player';
import { YourCallMarketGroupItem } from '../../models/markets/yourcall-market-group-item';
import { YourCallMarket } from '../../models/markets/yourcall-market';
import { YourCallMarketGroup } from '../../models/markets/yourcall-market-group';

@Injectable({ providedIn: 'root' })
export class YourCallMarketsProviderService {

  constructor(private locale: LocaleService) {}

  /**
   * Get instance for Banach markets
   * @param data
   * @returns {YourCallMarket}
   * @constructor
   */
  BYB_MAP(data: any): YourCallMarket {
    if (data.grouping && data.grouping !== 'Player Bets') {
      return new YourCallMarketGroup(data);
    } else if (data.grouping && data.grouping === 'Player Bets') {
      return new YourCallMarketPlayer(data);
    }
    if (data.parent) {
        switch (data.groupName) {
        case YOURCALL_BANACH_MARKETS.SHOWN_CARD:
        case YOURCALL_BANACH_MARKETS.FIRST_GOAL:
        case YOURCALL_BANACH_MARKETS.PLAYER_2_GOALS:
        case YOURCALL_BANACH_MARKETS.PLAYER_3_GOALS:
        case YOURCALL_BANACH_MARKETS.ANYTIME_GOAL:
        case YOURCALL_BANACH_MARKETS.FIRST_BOOKING:
          return new YourCallMarketGroupPlayer(data);
        default:
          return new YourCallMarketGroupItem(data);
      }
    }
    return new YourCallMarket(data);
  }

  /**
   * Create instance of YourCallMarket
   * @param data
   * @returns {YourCallMarket}
   */
  getInstance(data: any): YourCallMarket {
    _.extend(data, { _locale: this.locale });
    if (data.provider === YOURCALL_DATA_PROVIDER.BYB) {
      return this.BYB_MAP(data);
    }
    return new YourCallMarket(data);
  }
}
