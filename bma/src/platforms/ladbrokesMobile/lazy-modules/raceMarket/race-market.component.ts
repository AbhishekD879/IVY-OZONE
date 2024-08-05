/**
 * @class Race market controller To Finish, Top Finish, Place Insurance
 */

import { Component, Input } from '@angular/core';

import { RaceMarketComponent } from '@app/lazy-modules/raceMarket/race-market.component';
import { IOutcome } from '@core/models/outcome.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RacingGaService } from '@racing/services/racing-ga.service';

@Component({
  selector: 'race-market-component',
  templateUrl: 'race-market.component.html',
  styleUrls: ['race-market.scss'],
})
export class LadbrokesRaceMarketComponent extends RaceMarketComponent {
  @Input() isGreyhoundEdp?: boolean;
  @Input() sortOptionsEnabled: boolean;
  @Input() mIndex: number;
  @Input() sortOptionsEnabledFn: Function;

  constructor(
    protected raceOutcomeData: RaceOutcomeDetailsService,
    protected filterService: FiltersService,
    protected locale: LocaleService,
    protected pubsubService: PubSubService,
    protected sbFiltersService: SbFiltersService,
    protected racingService: RacingService,
    protected gtmService: GtmService,
    protected racingGaService: RacingGaService
  ) {
    super(raceOutcomeData, filterService, locale, pubsubService, sbFiltersService, racingService,gtmService, racingGaService);
  }

  isShowMore(outcomeEntity: IOutcome): boolean {
    return (outcomeEntity.racingFormOutcome && !outcomeEntity.isFavourite &&
      (!this.isGreyhoundEdp || outcomeEntity.racingFormOutcome.overview)) || outcomeEntity.timeformData;
  }

  toggleShowOptions(expandedSummary: Array<Array<boolean>>, showOption: boolean): void {
    if (expandedSummary && expandedSummary[0]) {
      for (let i = 0; i < expandedSummary[0].length; i++) {
        expandedSummary[0][i] = showOption;}
      }
  }

  onExpand(expandedSummary: boolean[][], oIndex: number): void {
    expandedSummary[0][oIndex] = !expandedSummary[0][oIndex];
    const hideInfoChecker: boolean = expandedSummary[0].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info': !hideInfoChecker };
    const gtmData = {
      event: "trackEvent",
      eventAction: "race card",
      eventCategory: this.isGreyhoundEdp?'greyhounds':'horse racing',
      eventLabel: expandedSummary[0][oIndex] ? 'show more':'show less',
      categoryID:this.eventEntity.categoryId,
      typeID:this.eventEntity.typeId,
      eventID:  this.eventEntity.id
    }
    this.gtmService.push(gtmData.event,gtmData);
  }
}
