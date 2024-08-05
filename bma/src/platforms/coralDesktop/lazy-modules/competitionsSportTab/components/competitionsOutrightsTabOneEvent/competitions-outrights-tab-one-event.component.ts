import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';

import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'competitions-outrights-tab-one-event',
  templateUrl: './competitions-outrights-tab-one-event.component.html'
})
export class CompetitionsOutrightsTabOneEventComponent implements OnChanges {
  @Input() outrights: ISportEvent[];
  @Input() openedItems: boolean[] = [];

  event: ISportEvent;
  markets: IMarket[];

  constructor(
    private sbFiltersService: SbFiltersService,
    private sportsEventHelperService: SportEventHelperService,
    private templateService: TemplateService,
    private filtersService: FiltersService
  ) {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if ('outrights' in changes) {
      this.event = this.outrights[0];

      const markets = this.event.markets;
      markets.sort((a, b) => a.displayOrder - b.displayOrder);
      markets.forEach(market => {
        this.sbFiltersService.orderOutcomeEntities(market.outcomes, market.isLpAvailable, true);
      });

      this.markets = markets;
    }
  }

  isLive(event: ISportEvent): boolean {
    return this.sportsEventHelperService.isLive(event);
  }

  isCashoutAvailable(event: ISportEvent): boolean {
    return this.sportsEventHelperService.isCashoutAvailable(event);
  }

  isEachWayTermsAvailable(market: IMarket): boolean {
    return this.sportsEventHelperService.isEachWayTermsAvailable(market);
  }

  genTerms(market: IMarket): string {
    return this.templateService.genTerms(market);
  }

  getStartTime(event: ISportEvent): string {
    return this.filtersService.date(event.startTime, 'EEEE, d-MMM-yy hh:mm');
  }

  trackMarket(index: number, market: IMarket): any {
    return market.id;
  }

  trackOutcome(index: number, outcome: IOutcome): any {
    return outcome.id;
  }
}
