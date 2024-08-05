import { Component, OnInit, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import {
  LadbrokesGreyhoundsTabsComponent
} from '@ladbrokesMobile/racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { EventService } from '@sb/services/event/event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { DeviceService } from '@core/services/device/device.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'greyhounds-tabs',
  templateUrl: 'greyhounds-tabs.component.html'
})
export class DesktopGreyhoundsTabsComponent extends LadbrokesGreyhoundsTabsComponent implements OnInit {

  sysConfig: ISystemConfig;
  limit: number;
  itemLoad: boolean;
  isPanelExpanded: boolean;
  loadAccordion: boolean;

  constructor(
    public router: Router,
    public filterService: FiltersService,
    public racingGaService: RacingGaService,
    public routingHelperService: RoutingHelperService,
    public eventService: EventService,
    public pubSubService: PubSubService,
    public cmsService: CmsService,
    protected gtm: GtmService,
    protected sessionStorageService: SessionStorageService,
    protected deviceService: DeviceService,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(router,
      filterService,
      racingGaService,
      routingHelperService,
      eventService,
      pubSubService,
      cmsService, gtm, vEPService);

    this.cmsService.getSystemConfig().subscribe(
      (data: ISystemConfig) => {
        this.sysConfig = data;
      });
  }

  ngOnInit(): void {
    super.ngOnInit();
    if (this.filteredTypeNames) {
      this.toggleByMeetingAccordion(0);
      this.filteredTypeNames[0]['isExpanded'] = true;
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if(!this.isEventOverlay && changes.filter && changes.filter.currentValue && this.filteredTypeNames && this.filteredTypeNames.length) {
      this.filteredTypeNames[0]['isExpanded'] = true;
      this.isExpanded = true;
    }
    if (!this.isEventOverlay && changes.viewByFilters && this.display === 'future') {
      this.filterInitData();
      this.filteredTypeNames && this.toggleByMeetingAccordion(0);
      this.filteredTypeNames[0]['isExpanded'] = true;
    }
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

  toggleByMeetingAccordion(index: number, moduleName?: string): void {
    if(moduleName === 'Events') {
      this.isExpanded = !this.isExpanded;
    }
    else{
      this.filteredTypeNames.forEach((filterType, ind) => {
        filterType['isExpanded'] = (index === ind) ? !filterType['isExpanded'] : this.isEventOverlay && this.deviceService.isDesktop ? false : filterType['isExpanded'];
      });
    }
    this.loadAccordion = true;
    moduleName && this.trackModule(index, moduleName);
  }

  trackModule(index: number, module: string): void{
    const accordionStatus = ( module === 'Events' ) ? this.isExpanded : this.filteredTypeNames[index]['isExpanded'];
    const gtmData = {
      'event': 'trackEvent',
      'eventAction': 'meetings',
      'eventCategory': 'greyhounds',
      'eventLabel': accordionStatus ? 'expand': 'collapse',
      'eventDetails': module
    }
    this.gtm.push(gtmData.event, gtmData);
  }

  overlayContentHandler(eventEntity: ISportEvent): void {
    this.sessionStorageService.set('gh-overlay-filterBy', this.filter);
    this.pubSubService.publish('MEETING_OVERLAY_FLAG', { id: eventEntity.id, flag: false });
    this.gtm.push('trackEvent', {
      eventID: eventEntity.id,
      eventAction: 'meetings',
      typeID: eventEntity.typeId,
      eventCategory: 'greyhounds',
      categoryID: eventEntity.categoryId,
      eventLabel: `navigation – ${this.filter.split('-').join(" ")}`,
    });
  }
}
