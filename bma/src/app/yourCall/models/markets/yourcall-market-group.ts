import { YourCallMarketGroupItem } from './yourcall-market-group-item';
import * as _ from 'underscore';

import { YourCallMarket } from './yourcall-market';
import { IYourcallGameData } from '../game-data.model';
import { YOURCALL_MARKETS_TYPES } from '../../constants/yourcall-markets-types';

export class YourCallMarketGroup extends YourCallMarket {
  grouping: string;
  available: boolean = true;
  // Array of child markets
  markets: YourCallMarketGroupItem[] = [];
  type: string = YOURCALL_MARKETS_TYPES.GROUP;

  constructor(data: IYourcallGameData[]) {
    super(data);

    this.parseTitle();
  }

  /**
   * Add child market
   * @param market
   */
  add(market: YourCallMarketGroupItem): void {
    this.markets.push(market);
  }

  /**
   * Get market id
   * @returns {*}
   */
  // @ts-ignore
  get id(): string {
    return _.map(this.markets, market => market.id).join(',');
  }
  set id(value:string){}

  /**
   * Get amount of child markets
   * @returns {number}
   */
  get count(): number {
    return this.markets.length;
  }
  set count(value:number){}

  /**
   * Populate market with data
   * @param data
   */
  _populate(data: IYourcallGameData[]): boolean {
    _.each(data, (gameData: IYourcallGameData) => {
      const market = _.findWhere(this.markets, { id: gameData.id });
      if (market) {
        market.populate(gameData.selections);
      }
    });
    return true;
  }

  /**
   * Replace placeholder with actual value
   * @private
   */
  parseTitle(): void {
    if (this.game && this.game.homeTeam && this.game.visitingTeam) {
      this.title = this.title
        .replace(/\bHOME\b/ig, this.game.homeTeam.title)
        .replace(/\bAWAY\b/ig, this.game.visitingTeam.title);
    }
  }
}
