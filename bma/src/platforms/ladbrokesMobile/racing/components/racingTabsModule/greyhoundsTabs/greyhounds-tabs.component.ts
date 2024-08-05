import { Component, ViewEncapsulation, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ISystemConfig } from '@core/services/cms/models';
import {
  GreyhoundsTabsComponent as CoralGreyhoundsTabsComponent
} from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { Router } from '@angular/router';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'greyhounds-tabs',
  templateUrl: 'greyhounds-tabs.component.html',
  styleUrls: ['greyhounds-tabs.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class LadbrokesGreyhoundsTabsComponent extends CoralGreyhoundsTabsComponent implements OnInit, OnDestroy {
  nextRacesComponentEnabled: boolean = false;

  private cmsDataSubscription: Subscription;

  constructor(
    public router: Router,
    public filterService: FiltersService,
    public racingGaService: RacingGaService,
    public routingHelperService: RoutingHelperService,
    public eventService: EventService,
    public pubSubService: PubSubService,
    public cmsService: CmsService,
    protected gtm: GtmService,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(router,
      filterService,
      racingGaService,
      routingHelperService,
      eventService,
      pubSubService,
      cmsService, gtm, vEPService);
  }

  /**
   * Check if next races component should be shown
   */
  get displayNextRaces(): boolean {
    return !this.responseError && this.display === 'today' && this.nextRacesComponentEnabled;
  }
  set displayNextRaces(value:boolean){}

  ngOnInit(): void {
    this.cmsDataSubscription = this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        this.nextRacesComponentEnabled = config && config.GreyhoundNextRacesToggle
          && config.GreyhoundNextRacesToggle.nextRacesComponentEnabled === true;
        super.ngOnInit();
      });
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();

    if (this.cmsDataSubscription) {
      this.cmsDataSubscription.unsubscribe();
    }
  }
}
