import { Injectable } from '@angular/core';
import { IGoalscorerCoupon } from '@core/models/goalscorer-coupon.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import * as _ from 'underscore';

@Injectable({
  providedIn: 'root'
})
export class GoalscorerCouponService {

  goalScorersToShow: number = 5;
  goalScorersLimit: number = 5;
  private marketsParams = [
    { templateMarketName: 'First Goalscorer', name: '1st', sortOrder: 1 },
    { templateMarketName: 'Last Goalscorer', name: 'Last', sortOrder: 2 },
    { templateMarketName: 'Anytime Goalscorer', name: 'Anytime', sortOrder: 3 }
  ];
  private orderedMarkets = _.sortBy(this.marketsParams, 'sortOrder');
  private orderedTMNames = this.orderedMarkets.map(m => m.templateMarketName);
  private scorersOrder = ['priceDec', 'name'];

  /**
   * Filter coupon events with outcomes available
   * @param {Object} event
   * @return boolean
   */
  private static checkCouponOutcomes(event: ISportEvent): boolean {
    if (event.hasOwnProperty('markets') && event.markets.length) {
      return event.markets.every(market => !!market.outcomes.length);
    }
  }

  constructor(
    private filtersService: FiltersService
  ) { }

  /**
   * formGoalScorers()
   * @param {ICoupon[]} couponEvents
   * @returns {ICoupon[]}
   */
  formGoalScorers(couponEvents: IGoalscorerCoupon[]): IGoalscorerCoupon[] {
    return couponEvents.map((couponByTypeName: IGoalscorerCoupon, index: number) => {
      couponByTypeName.events = this.extendEvents(couponByTypeName.events);
      couponByTypeName.isExpanded = index < 1;
      return couponByTypeName;
    }).filter(coupon => !!coupon.events.length);
  }

  /**
   * extendEvents()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  private extendEvents(events: ISportEvent[]): ISportEvent[] {
    return events.map(event => {
      if (event.markets.length) {
        const teamNames = this.teamsNames(event.name),
          validTMNames = _.intersection(this.orderedTMNames, event.markets.map(m => m.templateMarketName)),
          missingMarketsCount = this.orderedTMNames.length - validTMNames.length;

        event.goalScorersShowAll = false;
        event.goalScorersToShow = this.goalScorersToShow;
        event.markets = this.sortMarketsByTemplateMarketNames(event.markets, validTMNames);
        event.goalScorersHeader = validTMNames.map(tMN => _.indexBy(this.marketsParams, 'templateMarketName')[tMN].name);
        event.goalScorers = this.filtersService.orderBy(this.goalScorers(event.markets, teamNames, missingMarketsCount), this.scorersOrder);
      }

      return event;
    }).filter(GoalscorerCouponService.checkCouponOutcomes);
  }

  /**
   * goalScorers()
   * @param {IMarket[]} markets
   * @param {Object} teamNames
   * @param {Number} missingMarketsCount
   */
  private goalScorers(markets: IMarket[], teamNames: Object, missingMarketsCount: number) {
    return markets.length ? markets[0].outcomes.filter(o => o.outcomeMeaningMinorCode !== 'N')
      .map(outcome => ({
        name: outcome.name,
        priceDec: (outcome.prices[0] && outcome.prices[0].priceDec),
        teamName: teamNames[(outcome.outcomeMeaningMinorCode as any)],
        selections: this.selectionsByName(markets, outcome.name, missingMarketsCount)
      })) : [];
  }

  /**
   * selectionsByName()
   * @param {IMarket} markets
   * @param {string} outcomeName
   * @param {number} missingMarketsCount
   * @returns {IMarket[]}
   */
  private selectionsByName(markets: IMarket[], outcomeName: string, missingMarketsCount: number): IMarket[] {
    return _.flatten(markets.map((m, mI) => m.outcomes.filter(o => {
      o.correctedOutcomeMeaningMinorCode = mI + 1 + missingMarketsCount;
      o.marketIndex = mI;

      return o.name === outcomeName;
    })));
  }

  /**
   * sortMarketsByTemplateMarketNames()
   * @param {IMarket[]} markets
   * @param {string[]} templateMarketNames
   * @returns {IMarket[]}
   */
  private sortMarketsByTemplateMarketNames(markets: IMarket[], templateMarketNames: string[]): IMarket[] {
    const indexedMarkets = _.indexBy(markets, 'templateMarketName');

    return templateMarketNames.map(tMN => indexedMarkets[tMN]);
  }

  /**
   * teamsNames()
   * @param {string} eventName
   * @return {Object}
   */
  private teamsNames(eventName: string) {
    return {
      H: this.filtersService.getTeamName(eventName, 0),
      A: this.filtersService.getTeamName(eventName, 1)
    };
  }
}
