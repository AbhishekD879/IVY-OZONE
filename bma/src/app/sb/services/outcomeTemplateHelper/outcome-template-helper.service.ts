import { Injectable } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { TemplateService } from '@shared/services/template/template.service';

@Injectable()
export class OutcomeTemplateHelperService {
  constructor(
    private filtersService: FiltersService,
    private templateService: TemplateService,
  ) { }

  /**
   * setOutcomeMeaningMinorCode()
   * @param {IMarket[]} markets
   * @param {ISportEvent[]} event
   */
  setOutcomeMeaningMinorCode(markets: IMarket[], event: ISportEvent): void {
    markets.forEach((market: IMarket) => {
      if (market.outcomes && market.outcomes.length > 0) {
        this.setMeaningMinorCode(market, event);

        market.outcomes.sort((a, b) => a.correctedOutcomeMeaningMinorCode - b.correctedOutcomeMeaningMinorCode);
      }
    });
  }

  /**
   * getMinorCode()
   * @param {IOutcome} outcomeEntity
   * @param {ISportEvent} eventEntity
   * @param {number} index
   * @param {boolean} isOne
   * @returns {number}
   */
  private getMinorCode(outcomeEntity: IOutcome, eventEntity: ISportEvent, index: number, isOne: boolean): number {
    let result = index;

    if (outcomeEntity.outcomeMeaningMinorCode) {
      outcomeEntity.isUS = eventEntity.isUS;
      result = this.templateService.getCorrectedOutcomeMeaningMinorCode(outcomeEntity);
    } else if (isOne && outcomeEntity.name) {
      const name = outcomeEntity.name.toLowerCase();
      const homeTeamName = this.filtersService.getTeamName(eventEntity.name, 0);
      const isYesNo = name === 'yes';
      const isHomeName = (homeTeamName && name === homeTeamName.trim().toLowerCase());

      result = isYesNo || isHomeName ? 1 : 3;
    }

    return result;
  }

  /**
   * setMeaningMinorCode()
   * @param {IMarket} market
   * @param {ISportEvent} event
   */
  private setMeaningMinorCode(market: IMarket, event: ISportEvent): void {
    const sortedOutcomes = market.outcomes;
    sortedOutcomes.sort((a, b) => a.displayOrder - b.displayOrder);

    if (sortedOutcomes.length > 1) {
      sortedOutcomes[0].correctedOutcomeMeaningMinorCode = this.getMinorCode(sortedOutcomes[0], event, 1, false);
      sortedOutcomes[1].correctedOutcomeMeaningMinorCode = this.getMinorCode(sortedOutcomes[1], event, 2, false);
      sortedOutcomes[sortedOutcomes.length - 1].correctedOutcomeMeaningMinorCode =
        this.getMinorCode(sortedOutcomes[sortedOutcomes.length - 1], event, 3, false);
    } else {
      sortedOutcomes[0].correctedOutcomeMeaningMinorCode = this.getMinorCode(sortedOutcomes[0], event, 1, true);
    }
  }
}
