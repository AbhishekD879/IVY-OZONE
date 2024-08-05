import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';
import { EventService } from '@sb/services/event/event.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IFutureEvent, IFilterType } from '@racing/models/racing-ga.model';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'greyhound-future-tab',
  styleUrls: ['greyhound-future-tab.scss'],
  templateUrl: 'greyhound-future-tab.component.html'
})

export class GreyhoundFutureTabComponent implements OnInit {
  @Input() filter: string;
  @Input() orderedEvents: ISportEvent[];
  @Input() orderedEventsByTypeNames: ISportEvent[];
  @Input() filteredTypeNames: IFilterType[];
  @Input() racingEvents: ISportEvent[];
  @Input() isExpanded: boolean;
  @Input() isEventOverlay: boolean;

  limit: number;
  loadAccordion: boolean;

  constructor(
    public filterService: FiltersService,
    public eventService: EventService,
    public routingHelperService: RoutingHelperService,
    protected sessionStorageService: SessionStorageService,
    protected pubSubService: PubSubService,
    protected gtmService: GtmService,
    protected deviceService: DeviceService
  ) {}

  ngOnInit(): void {
    this.isEventOverlay && this.toggleByMeetingAccordion(0);
    this.orderedEvents.forEach((event: IFutureEvent) => {
      event.link = this.formEdpUrl(event);
      event.date = this.filteredTime(event);
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if(!this.isEventOverlay && changes.filter && changes.filter.currentValue) {
      this.toggleByMeetingAccordion(0); 
    }
  }
  checkCacheOut(events: ISportEvent[], typeName: string): boolean {
    const filteredEvents = _.filter(events, (event: ISportEvent) => event.typeName === typeName);

    return this.eventService.isAnyCashoutAvailable(filteredEvents, [{ cashoutAvail: 'Y' }]);
  }

  trackById(index, value): number {
    return value.id ? value.id : value.groupFlag;
  }

  /**
   * Forms event details page.
   * @param {Object} event
   * @return {string}
   */
  formEdpUrl(event: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(event);
  }

  private filteredTime(event: ISportEvent): string {
    return this.filterService.date(event.startTime, 'dd-MM-yyyy');
  }

  /**
   * Accordion toggle handler 
   * @param index 
   * @param moduleName 
   */
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

  /**
   * track accordion handler GA Tracking
   * @param index 
   * @param moduleName 
   */
  trackModule(index: number, moduleName: string): void {
    const tab = (moduleName === 'Events') ? this.isExpanded : this.filteredTypeNames[index]['isExpanded'];
    const accordionStatus =  tab ? 'expand': 'collapse';
    const gtmData = {
      'event': 'trackEvent',
      'eventAction': 'meetings',
      'eventCategory': 'greyhounds',
      'eventLabel': accordionStatus,
      'eventDetails': moduleName
    }

    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * overlay data switcher default tab save, 
   * GA tracking
   * @param data 
   * @param event 
   */
  overlayContentHandler(data, event) {
    this.sessionStorageService.set('gh-overlay-filterBy', data.filter);
    this.pubSubService.publish('MEETING_OVERLAY_FLAG', { id: data.eventId, flag: false });
    this.gtmService.push('trackEvent', {
      eventID: event.id,
      eventAction: 'meetings',
      typeID: event.typeId,
      eventCategory: 'greyhounds',
      categoryID: event.categoryId,
      eventLabel: `navigation – ${this.filter.split('-').join(" ")}`,
    });
  }
}
