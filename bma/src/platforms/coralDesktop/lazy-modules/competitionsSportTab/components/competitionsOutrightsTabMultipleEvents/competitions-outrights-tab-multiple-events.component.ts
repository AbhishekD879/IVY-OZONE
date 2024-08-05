import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'competitions-outrights-tab-multiple-events',
  templateUrl: './competitions-outrights-tab-multiple-events.component.html'
})
export class CompetitionsOutrightsTabMultipleEventsComponent implements OnChanges {
  @Input() outrights: ISportEvent[];
  @Input() openedItems: boolean[];

  constructor(
    private sportEventHelperService: SportEventHelperService,
    private templateService: TemplateService,
    private filtersService: FiltersService,
    private sbFiltersService: SbFiltersService
  ) {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if ('outrights' in changes) {
      // Sort outrights
      this.outrights.sort((a, b) => a.displayOrder - b.displayOrder);

      this.outrights.forEach(event => {
        // Sort markets
        event.markets.sort((a, b) => a.displayOrder - b.displayOrder);

        event.markets.forEach(market => {
          // Sort outcomes
          this.sbFiltersService.orderOutcomeEntities(market.outcomes, market.isLpAvailable);
        });
      });
    }
  }

  isLive(event: ISportEvent): boolean {
    return this.sportEventHelperService.isLive(event);
  }

  isCashoutAvailable(event: ISportEvent): boolean {
    return this.sportEventHelperService.isCashoutAvailable(event);
  }

  isEachWayTermsAvailable(market: IMarket): boolean {
    return this.sportEventHelperService.isEachWayTermsAvailable(market);
  }

  genTerms(market: IMarket): string {
    return this.templateService.genTerms(market);
  }

  getStartTime(event: ISportEvent): string {
    return this.filtersService.date(event.startTime, 'EEEE, d-MMM-yy h:mm a');
  }

  trackEvent(index: number, event: ISportEvent): any {
    return event.id;
  }

  trackMarket(index: number, market: IMarket): any {
    return market.id;
  }

  trackOutcome(index: number, outcome: IOutcome): any {
    return outcome.id;
  }
}
