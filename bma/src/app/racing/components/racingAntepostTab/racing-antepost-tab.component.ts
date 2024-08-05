import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IRacingMap, IFutureEvent, ITypeNamesEvent } from '@racing/models/racing-ga.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { DeviceService } from '@app/core/services/device/device.service';

@Component({
  selector: 'racing-antepost-tab',
  styleUrls: ['racing-antepost-tab.component.scss'],
  templateUrl: 'racing-antepost-tab.component.html'
})
export class RacingAntepostTabComponent implements OnInit {
  @Input() racing: {events: ISportEvent[]};
  @Input() defaultAntepostTab?: string;
  @Input() responseError?;
  @Input() isFromOverlay?: boolean;
  events: ISportEvent[];
  eventsMap: {[key: string]: IRacingMap};
  switchers: ISwitcherConfig[] = [];
  sortSwitchers: ISwitcherConfig[];
  filter: string | null;
  isExpanded: boolean[];
  gtmInitialData: { event: string; eventAction: string; eventCategory: string; };

  constructor(
    public filterService: FiltersService,
    public locale: LocaleService,
    public racingService: RacingService,
    public routingHelperService: RoutingHelperService,
    public sessionStorageService: SessionStorageService,
    public pubSubService: PubSubService,
    public gtm: GtmService,
    public deviceService: DeviceService
    ) {}

  ngOnInit(): void {
    this.events = this.racing.events;
    if (this.events.length) {
      this.getAntepostEventsFlags(this.events);
      this.sortSwitchers = _.sortBy(this.switchers, 'order');
      this.isExpanded = [true];
      this.setDefaultTab();
    }

    if (this.isFromOverlay) {
      this.pubSubService.subscribe('futureTab', this.pubSubService.API.ACTIVE_FUTURE_TAB, () => {
        this.filter = this.sessionStorageService.get('selectedFutureTab');
      });
    }
  }

  trackById(index: number, value: any): number {
    return value.id ? value.id : (value.typeNameEvents && value.typeNameEvents[0] && value.typeNameEvents[0].id);
  }

  /**
   * Select events by switcher
   * @param {string} key
   */
  selectEventList(key: string, clicked?: boolean): void {
    this.filter = key;
    this.sessionStorageService.set('selectedFutureTab', key);
    if (this.isFromOverlay) {
      for (let i = 0; i < this.eventsMap[key].typeNames.length; i++) {
        this.isExpanded[i] = false;
      }
    }
    this.isExpanded[0] = true;

    if(this.isFromOverlay && clicked) {
      const gtmData = {
        'event': 'trackEvent',
        'eventAction': 'meetings',
        'eventCategory': 'horse racing',
        'eventLabel': `${this.switchers.find((sw) => sw.viewByFilters === this.filter).name.toLowerCase()}`,
      }
  
      this.gtm.push(gtmData.event, gtmData);
    }
  }

  /**
   * Accordion toggle handler 
   * @param {index} number 
   * @param {type} ITypeNamesEvent
   */
  accordionHandler(index: number, type?: ITypeNamesEvent): void {
    if (!this.isFromOverlay) {
      return;
    }

    this.deviceService.isDesktop && this.isExpanded.forEach((expand, idx) => {
      this.isExpanded[idx] = (idx === index) ? !this.isExpanded[idx] : false;
    });

    const accordionStatus = this.isExpanded[index] ? 'expand': 'collapse';
    const gtmData = {
      'event': 'trackEvent',
      'eventAction': 'meetings',
      'eventCategory': 'horse racing',
      'eventLabel': accordionStatus,
      'eventDetails': type.typeName
    }

    this.gtm.push(gtmData.event, gtmData);
  }

  /**
   * Get antepost events and sort them by typeNames
   * @param {array} events
   */
  getAntepostEventsFlags(events: ISportEvent[]): void {
    const regexp = /EVFLAG_FT|EVFLAG_IT|EVFLAG_NH/g;
    const sortEvents: ISportEvent[] = _.sortBy(events, 'startTime');

    _.each(sortEvents, (object: IFutureEvent) => {
      const key = object.drilldownTagNames.match(regexp);
      object.link = this.formEdpUrl(object);
      object.date = this.getDate(object);
      if (key && _.contains(this.racingService.ANTEPOST_SWITCHER_KEYS, key[0])) {
        this.groupBySwitcherKeys(key[0], object);
      }
    });

    _.each(this.eventsMap, (value: IRacingMap) => {
      value.typeNames = _.chain(value.events)
        .groupBy('typeName')
        .reduce((list, typeNameEvents, typeName) => {
          const displayOrder = typeNameEvents[0].typeDisplayOrder;
          const cashoutAvail = typeNameEvents[0].cashoutAvail;
          list.push({ typeName, typeNameEvents, displayOrder, cashoutAvail });
          return list;
        }, [])
        .value();
      value.typeNames =  _.sortBy(value.typeNames, 'displayOrder');

    });
  }

  /**
   * GA Tracking on closeOverlay, reload Components
   * @param { event } ISportEvent
   */
  closeOverlay(event: ISportEvent): void {
    if (!this.isFromOverlay) {
      return;
    }

    const gtmData = {
      'event': 'trackEvent',
      'eventAction': 'meetings',
      'eventCategory': 'horse racing',
      'eventLabel': `navigation - ${this.switchers.find((sw) => sw.viewByFilters === this.filter).name.toLowerCase()}`,
      'categoryID': event.categoryId,
      'typeID': event.typeId,
      'eventID':  event.id
    }

    this.gtm.push(gtmData.event, gtmData);
    this.pubSubService.publish(this.pubSubService.API.RELOAD_COMPONENTS);
  }

  protected getDate(event: ISportEvent): string {
    return `${this.filterService.date(event.startTime, 'dd-MM-yyyy | HH:mm')}`;
  }

  /**
   * Forms event details page or sport results page based on event's "isResulted" property.
   * @param {Object} eventEntity
   * @return {string}
   */
  private formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }
  /**
   * Set tab recived by CMS or forst available tab
   */
  private setDefaultTab(): void {
    let defaultTab: ISwitcherConfig;
    let filter: string;
    if (this.isFromOverlay) {
      filter = this.sessionStorageService.get('selectedFutureTab');
    } else if (this.defaultAntepostTab) {
      defaultTab = this.sortSwitchers.find((swicher) => swicher.name.toLowerCase() === this.defaultAntepostTab.toLocaleLowerCase());
      filter = defaultTab && defaultTab.viewByFilters;
    }
    
    this.filter = filter || this.sortSwitchers[0].viewByFilters;
    this.selectEventList(this.filter);
  }

  /**
   * Group events by switchers keys
   * @param {string} key
   * @param {object} event
   */
  private groupBySwitcherKeys(key: string, event: ISportEvent): void {
    if (!this.eventsMap || (this.eventsMap && !this.eventsMap[key])) {
      this.sortSwitchersKeys(key);
      if (this.eventsMap) {
        this.eventsMap[key] = {
          events: [event]
        };
      } else {
        this.eventsMap = {
          [key]: {
            events: [event]
          }
        };
      }
    } else {
      this.eventsMap[key].events.push(event);
    }
  }

  /**
   * Sort switchers keys
   */
  private sortSwitchersKeys(key: string): void {
    _.each(this.racingService.ANTEPOST_SWITCHER_KEYS, (value, index) => {
      if (key === value) {
        this.createSwitchers(key, index);
      }
    });
  }

  /**
   * Create switcher keys for antepost events
   * @param {string} key
   * @param {number} sortOrder
   */
  private createSwitchers(key: string, sortOrder: number): void {
    this.switchers.push({
      name: this.locale.getString(`racing.${key}`),
      onClick: () => this.selectEventList(key, true),
      viewByFilters: key,
      order: sortOrder
    });
  }
}
