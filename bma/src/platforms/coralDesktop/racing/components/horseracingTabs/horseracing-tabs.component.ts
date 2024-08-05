import { Component, OnInit } from '@angular/core';
import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { Router } from '@angular/router';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { CmsService } from '@core/services/cms/cms.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'horseracing-tabs',
  templateUrl: 'horseracing-tabs.component.html'
})
export class DesktopHorseracingTabsComponent extends HorseracingTabsComponent implements OnInit {

  cardIdObj: { id: string };
  isTotePoolsAvailable: boolean = false;
  isEnabledCardState: boolean;
  isLimitReached: boolean;
  isClearBuildCardState: boolean;

  constructor(
    router: Router,
    routingHelperService: RoutingHelperService,
    eventService: EventService,
    public cmsService: CmsService,
    protected vEPService: VirtualEntryPointsService
  ) {
    super(router,
      routingHelperService,
      eventService,
      cmsService, vEPService);
  }

  fetchCardId(cardIdObj: { id: string}): void {
    this.cardIdObj = Object.assign({}, cardIdObj);
  }

  onFeaturedEvents(event: {output: string, value: any}): void {
    switch (event.output) {
      case 'fetchCardId':
        this.fetchCardId(event.value);
        break;
      case 'featuredLoaded':
        this.handleFeaturedLoaded(event.value);
        break;
      default:
        break;
    }
  }
}
