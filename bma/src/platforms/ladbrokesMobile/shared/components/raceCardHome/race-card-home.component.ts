import { Component, Input, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { NextRacesHomeService } from '@ladbrokesMobile/lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router } from '@angular/router';
import { EventService } from '@sb/services/event/event.service';
import {
  RaceCardHomeComponent as AppRaceCardHomeComponent
} from '@lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { DatePipe } from '@angular/common';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { RacingGaService } from '@racing/services/racing-ga.service';

@Component({
  selector: 'race-card-home',
  templateUrl: './race-card-home.component.html',
  styleUrls: [
    '../../../../../app/lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component.scss',
    './race-card-home.component.scss'
  ]
})
export class RaceCardHomeComponent extends AppRaceCardHomeComponent implements OnInit, OnDestroy {
  @Input() moduleType?: string;
  @Input() trackFunction?: Function;
  @Input() carouselView?: boolean;
  @Input() showBriefHeader?: boolean;
  @Input() showHeader?: boolean=true;
  @Input() isNextRacesModule?: boolean;
  constructor(
    public raceOutcomeData: RaceOutcomeDetailsService,
    public routingHelperService: RoutingHelperService,
    public nextRacesHomeService: NextRacesHomeService,
    public locale: LocaleService,
    public sbFiltersService: SbFiltersService,
    public filtersService: FiltersService,
    public pubSubService: PubSubService,
    public router: Router,
    public eventService: EventService,
    public virtualSharedService: VirtualSharedService,
    public datePipe: DatePipe,
    public changeDetectorRef: ChangeDetectorRef,
    public cmsService: CmsService,
    public sortByOptionsService: SortByOptionsService,
    public horseracing: HorseracingService,
    public racingGaService: RacingGaService
  ) {
    super(raceOutcomeData,
      routingHelperService,
      nextRacesHomeService,
      locale,
      sbFiltersService,
      filtersService,
      pubSubService,
      router,
      eventService,
      virtualSharedService,
      datePipe,
      changeDetectorRef,
      cmsService,
      sortByOptionsService,
      horseracing,
      racingGaService
    );
  }

  trackEvent(entity: ISportEvent): void {
   if (this.trackFunction) {
      this.trackFunction(entity);
      return;
    }

    this.nextRacesHomeService.trackNextRace(entity, this.moduleType);
    const link = this.isVirtual && entity.categoryId === '39' ? this.virtualSharedService.formVirtualEventUrl(entity) : this.formEdpUrl(entity);
    this.router.navigateByUrl(link);
  }
}
