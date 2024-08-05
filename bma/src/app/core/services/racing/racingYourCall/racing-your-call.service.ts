import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Injectable()
export class RacingYourCallService {
  /**
   * prepareData()
   * @param {any[]} destinationCollection
   * @param {any[]} data
   */
  prepareData(destinationCollection: any[], data: any[]): any {
    _.each(data, (event: ISportEvent) => {
      _.each(event.markets, market => {
        this.setEventAndMarket(event, market, market.outcomes);
        const existedMarket = _.findWhere(destinationCollection, { name: market.name });
        if (existedMarket) {
          existedMarket.selections = existedMarket.selections.concat(market.outcomes);
        } else {
          destinationCollection.push({ displayOrder: Number(market.displayOrder), name: market.name });
          destinationCollection[destinationCollection.length - 1].selections = market.outcomes;
        }
      });
    });

    this.clearEmptyMarkets(destinationCollection);

    return destinationCollection;
  }

  /**
   * setEventAndMarket()
   * @param {ISportEvent} event
   * @param {IMarket} market
   * @param {IOutcome[]} outcomes
   */
  private setEventAndMarket(event: ISportEvent, market: IMarket, outcomes: IOutcome[]): void {
    _.each(outcomes, outcome => {
      outcome.event = event;
      outcome.market = market;
    });
  }

  /**
   * clearEmptyMarkets()
   * @param {any[]} accumulatedMarkets
   */
  private clearEmptyMarkets(accumulatedMarkets: any[]): void {
    const resultArr = _.reject(accumulatedMarkets,
      accumulatedMarket => !accumulatedMarket.selections || !accumulatedMarket.selections.length);

    accumulatedMarkets.length = 0;

    _.each(resultArr, obj => {
      accumulatedMarkets.push(obj);
    });
  }
}
