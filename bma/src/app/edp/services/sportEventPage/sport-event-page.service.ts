import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { FiltersService } from '@core/services/filters/filters.service';

@Injectable()
export class SportEventPageService {

  constructor(
    private filtersService: FiltersService,
    private smartBoostsService: SmartBoostsService){}

  /**
   * Transform markets data
   * @param {IMarket[]} markets
   */
  public transformMarkets(markets: IMarket[]): void {
    _.each(markets, (market: IMarket) => {
      market.isSmartBoosts = this.smartBoostsService.isSmartBoosts(market);
      if(market?.outcomes && market.outcomes.length>0){
        _.each(market.outcomes, (outcome: IOutcome) => {
          if (market.viewType === 'Scorer' || market.viewType === 'WDW') {
            outcome.alphabetName = this.filtersService.filterAlphabetsOnly(outcome.name);
            outcome.numbersName = this.filtersService.filterNumbersOnly(outcome.name);
          }
          if (!market.isSmartBoosts) { return; }
          const parsedName = this.smartBoostsService.parseName(outcome.name);
          if (!parsedName.wasPrice) { return; }
          outcome.name = parsedName.name;
          outcome.wasPrice = parsedName.wasPrice;
        });
        market.groupedOutcomes = _.toArray(this.filtersService.groupBy(market.outcomes, 'outcomeMeaningMinorCode'));
        market.groupedOutcomes = _.filter(market.groupedOutcomes, outcomes => !_.isEmpty(outcomes));
      }
    });
  }
}