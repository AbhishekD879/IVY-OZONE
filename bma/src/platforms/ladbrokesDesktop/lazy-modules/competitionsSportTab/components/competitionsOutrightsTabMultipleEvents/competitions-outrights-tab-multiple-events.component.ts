import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
  selector: 'competitions-outrights-tab-multiple-events',
  templateUrl: './competitions-outrights-tab-multiple-events.component.html'
})
export class CompetitionsOutrightsTabMultipleEventsComponent implements OnChanges {
  @Input() outrights: ISportEvent[];
  @Input() openedItems: boolean[];
  openMarketTabs: number = 1;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  constructor(
    private sportEventHelperService: SportEventHelperService,
    private templateService: TemplateService,
    private filtersService: FiltersService,
    private sbFiltersService: SbFiltersService,
    private cmsService: CmsService
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

  isLuckyDipMarketAvailable(event: ISportEvent){
    let sysConfig;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      sysConfig = config && config.LuckyDip && config.LuckyDip.enabled;
    });
    let isLD: boolean | IMarket[] = false;
    const obConfig: IMarket = event?.markets.find(market => market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1);
    const isLuckyDipConfig = sysConfig && obConfig && event?.eventSortCode === LUCKY_DIP_CONSTANTS.TNMT;
    event?.markets.forEach(market => {
      market.isLuckyDip = market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1;
    });
    isLD = (isLuckyDipConfig) ? true : (!sysConfig && obConfig) ? event.markets = event?.markets.filter(market => !market.isLuckyDip) : false;
    return isLD;
  }
}
