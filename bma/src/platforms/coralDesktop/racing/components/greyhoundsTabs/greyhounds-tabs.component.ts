import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'greyhounds-tabs',
  templateUrl: 'greyhounds-tabs.component.html'
})
export class DesktopGreyhoundsTabsComponent extends GreyhoundsTabsComponent implements OnInit {

  sysConfig: ISystemConfig;
  limit: number;

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
      cmsService, gtm,  vEPService);

    this.cmsService.getSystemConfig().subscribe(
      (data: ISystemConfig) => {
        this.sysConfig = data;
      });
  }

  filteredTime(time: string, format: string): string {
    return this.filterService.date(time, format);
  }

  checkCacheOut(events: ISportEvent[], typeName: string): boolean {
    const filteredEvents = _.filter(events, (event: ISportEvent) => event.typeName === typeName);

    return this.eventService.isAnyCashoutAvailable(filteredEvents, [{ cashoutAvail: 'Y' }]);
  }

  /**
   * Forms event details page.
   * @param {Object} eventEntity
   * @return {string}
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  get showTodayTomorrowNoEvents(): boolean {
    const noMeetingEvents = this.filter === 'by-meeting' && !this.racing.groupedRacing.length;
    const noTimeEvents = this.filter === 'by-time' && !this.racing.events.length;
    return !this.responseError && (noMeetingEvents || noTimeEvents);
  }
  set showTodayTomorrowNoEvents(value:boolean){}
}
