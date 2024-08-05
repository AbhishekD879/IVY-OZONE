import * as _ from 'underscore';
import { Router } from '@angular/router';
import { Component, Input, OnDestroy, OnInit, OnChanges, SimpleChanges } from '@angular/core';

import environment from '@environment/oxygenEnvConfig';
import { IToteEvent } from '@app/tote/models/tote-event.model';
import { ToteService } from '@app/tote/services/mainTote/main-tote.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { TempStorageService } from '@core/services/storage/temp-storage.service';

import { Subscription } from 'rxjs';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'tote-slider',
  templateUrl: 'tote-slider.component.html',
  styleUrls: [ 'tote-slider.component.scss' ]
})
export class ToteSliderComponent implements OnInit, OnDestroy, OnChanges {

  @Input() sport: string;
  @Input() moduleTitle: string;
  @Input() eventsData: IToteEvent[];
  @Input() sportName?: string;
  isExpanded: boolean;
  bannerBeforeAccorditionHeader: string= '';
  targetTab: ISportConfigTab | null = null;

  protected SECTION_FLAG = 'ITC';

  private loadDataSubscription: Subscription;
  private loadEventSubscription: Subscription;

  constructor(
    protected toteService: ToteService,
    protected gtmService: GtmService,
    protected router: Router,
    protected locale: LocaleService,
    protected storage: TempStorageService,
    protected buildUtilityService: BuildUtilityService,
    protected vEPService : VirtualEntryPointsService
  ) {}

  ngOnInit(): void {
    const expandedState = this.storage.get(this.SECTION_FLAG);
    this.isExpanded = expandedState !== undefined ? this.storage.get(this.SECTION_FLAG) : true;

    if(!this.storage.get('totes') || this.checkStoredTime(this.storage.get('totes').time, new Date().getTime())) {
      // if featured is down and no tote, get data from ss-request
      if (this.eventsData[0].name === this.SECTION_FLAG && !this.eventsData[0].id) {
        this.loadDataSubscription = this.toteService.getRawToteEvents(environment.TOTE_CLASSES[this.sport])
          .subscribe((data: IToteEvent[]) => {
            this.eventsData = this.prepareData(data, true);
            this.storage.set('totes', { data: this.eventsData, time: new Date().getTime() });
          });
      } else {
        this.eventsData = this.prepareData(this.eventsData);
        this.storage.set('totes', { data: this.eventsData, time: new Date().getTime() });
      }
    } else {
      this.eventsData = this.storage.get('totes').data;
      this.filterEventsData(this.eventsData);
    }
    this.moduleTitle = this.moduleTitle || this.locale.getString('tt.toteEvents');

    this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });
  
    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });
  }

  ngOnChanges(changes: SimpleChanges): void  {
    const eventsData: IToteEvent[] = changes.eventsData && changes.eventsData.currentValue;
    if (eventsData) {
      this.eventsData = this.prepareData(eventsData);
    }
  }

  ngOnDestroy(): void {
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }

    if (this.loadEventSubscription) {
      this.loadEventSubscription.unsubscribe();
    }
  }

  trackEvent(event: IToteEvent): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'tote carousel',
      eventLabel: `${event.typeName} ${event.localTime}`
    });
  }

  trackById(index: number, event: IToteEvent): number {
    return event.id;
  }

  sortEvents(data: IToteEvent[]): IToteEvent[] {
    return _.sortBy(data, (event) => {
      const resulted = event.isResulted ? '0' : '1';
      return `${resulted}-${event.startTime}-${event.typeName}`;
    });
  }

  prepareData(data: IToteEvent[], toSort: boolean = false): IToteEvent[] {
    let linkedToteEvents = this.filterLinkedToteEvents(data);
    if (toSort) {
      linkedToteEvents = this.sortEvents(linkedToteEvents);
    }
    linkedToteEvents.forEach( (event) => {
      event.displayName = this.parseTypeName(event.typeName);
      if (!event.localTime) {
        event.localTime = this.buildUtilityService.getLocalTime(event);
      }
    });
    this.filterEventsData(linkedToteEvents);
    return this.eventsData;
  }

  /**
   * Handle click on int tote event
   * @param {IToteEvent} event
   */
  clickEvent(event: IToteEvent | ISportEvent | any): void {
    this.trackEvent(event);

    if (this.loadEventSubscription) {
      this.loadEventSubscription.unsubscribe();
    }

    this.loadEventSubscription = this.toteService.getToteLink(
      event.externalKeys && event.externalKeys.OBEvLinkNonTote,
      event.id,
      false // in use for international tote only
    ).subscribe((eventUrl: string) => {
      eventUrl && this.router.navigate([eventUrl]);
    });
  }

  parseTypeName(name: string): string {
    const parts = name.replace(/\(.*\)|\sTH\s?$/g, '').trim().split(' ');
    if (parts.length === 1 || parts[0].length >= 5) {
      return parts[0].substr(0, 5);
    }
    return parts[0] + parts[1].substr(0, 5 - parts[0].length);
  }

  filterLinkedToteEvents(toteEvents: IToteEvent[]) {
    return (toteEvents || []).filter((event: IToteEvent) => event.externalKeys && event.externalKeys.OBEvLinkNonTote);
  }

  // Check stored totes time, if it is greater than 3 min,
  // data needs to be re-fetched and re-stored
  private checkStoredTime(time1: number, time2: number): boolean {
    const MINUTES_TO_STORE: number = 5;
    return Math.abs(time2 - time1)/1000 > 60 * MINUTES_TO_STORE;
  }

  /**
   * To filter events data
   * @param {IToteEvent[]} eventsData
   * @returns {void}
   */
  private filterEventsData(eventsData: IToteEvent[]): void {
    this.eventsData = this.toteService.filterToteGroup(eventsData);
  }


  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

}
