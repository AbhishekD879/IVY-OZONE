import { Component, Input, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef,
OnChanges,
SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { from, Subscription } from 'rxjs';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ExtraPlaceService } from '@core/services/racing/extraPlace/extra-place.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOffersRacingEvent, IOffersRacingGroup } from './offers-and-featured-races.model';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'offers-and-featured-races',
  templateUrl: 'offers-and-featured-races.component.html',
  styleUrls: ['./offers-and-featured-races.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OffersAndFeaturedRacesComponent implements OnInit, OnDestroy, OnChanges {
  @Input() sectionTitle: string;
  @Input() events: ISportEvent[];
  @Input() isEventOverlay?: boolean;

  @Input() isRacingFeatured?:boolean;
  @Input() sportName?: string;
  bannerBeforeAccorditionHeader: string= '';
  targetTab: ISportConfigTab | null = null;

  slidesOnPage: number = 1;
  groupedEvents: IOffersRacingGroup = {};
  allEvents: ISportEvent[] = [];
  subscribedChannelsId: string = '';
  readonly raceKeys: string[] = ['itv', 'epr'];
  private readonly tagName: string = 'offers-and-featured-races';
  private loadDataSubscription: Subscription;
  private isFirstTimeCollapsed: boolean = false;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  constructor(
    protected extraPlaceService: ExtraPlaceService,
    protected gtmService: GtmService,
    protected routingHelperService: RoutingHelperService,
    protected router: Router,
    protected localeService: LocaleService,
    protected pubSubService: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected seoDataService:SeoDataService,
    protected vEPService : VirtualEntryPointsService) { }

  ngOnInit(): void {
    if (this.events && this.events.length) {
      this.allEvents = this.filterEvents(this.events);
      this.allEvents = [...this.allEvents].sort((a: ISportEvent, b: ISportEvent) => (Number(a.startTime) - Number(b.startTime)));
      this.setGroupedEvents(this.allEvents);
    } else {
      this.loadDataSubscription = from(this.extraPlaceService.getEvents()).subscribe((events: ISportEvent[]) => {
        this.allEvents = events;
        this.allEvents = [...this.allEvents].sort((a: ISportEvent, b: ISportEvent) => (Number(a.startTime) - Number(b.startTime)));
        this.setGroupedEvents(this.allEvents);
      }, () => {
        this.allEvents = [];
        this.groupedEvents = {};
        this.changeDetectorRef.markForCheck();
      });
    }

    this.pubSubService.subscribe(this.tagName,
      [
        this.pubSubService.API.DELETE_EVENT_FROM_CACHE,
        this.pubSubService.API.EXTRA_PLACE_RACE_OFF
      ], (eventId: number) => {
        this.updateEvents(eventId);
      });

     this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });
  
    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.events) {
      if (this.events &&
        this.events.length) {
        this.allEvents = this.filterEvents(this.events);
        this.allEvents = [...this.allEvents].sort((a: ISportEvent, b: ISportEvent) => (Number(a.startTime) - Number(b.startTime)));
        this.setGroupedEvents(this.allEvents);
      }
    }
  }

  ngOnDestroy(): void {
    this.loadDataSubscription && this.loadDataSubscription.unsubscribe();
    this.extraPlaceService.unSubscribeForUpdates(this.subscribedChannelsId);
    this.pubSubService.unsubscribe(this.tagName);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ISportEvent} event
   * @return {string}
   */
  trackById(index: number, event: ISportEvent): string {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  /**
   * Send GA on first collapse
   */
  sendCollapseGTM(): void {
    if (!this.isFirstTimeCollapsed) {
      this.gtmService.push('trackEvent', this.extraPlaceService.gtmObject);
      this.isFirstTimeCollapsed = true;
    }
  }

  /**
   * Go to the sport event
   */
  goToEvent(event: ISportEvent): void {
    const url = this.formEdpUrl(event);
    this.extraPlaceService.sendGTM(event.originalName);
    this.router.navigateByUrl(url);
    this.seoDataService.eventPageSeo(event, url);
    if(this.isEventOverlay){
      this.offersAndFeaturesGATracking(event);
      this.pubSubService.publish('MEETING_OVERLAY_FLAG',{id:event.id,flag: false});
    }
  }

  offersAndFeaturesGATracking(event: ISportEvent) {
    this.gtmService.push('trackEvent', {    
        eventAction: 'meetings',
        eventCategory: 'horse racing',
        eventLabel: `navigation – ${this.sectionTitle.toLowerCase()}`,
        categoryID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      });
  }

  /**
   * Set Grouped Racing Events
   */
  private setGroupedEvents(events: ISportEvent[]): void {
    this.groupedEvents = this.getRacingEvents(events);
    this.subscribedChannelsId = this.extraPlaceService.subscribeForUpdates(events);
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Filter needed events
   * @param events
   */
  private filterEvents(events: ISportEvent[]): ISportEvent[] {
    return events.filter((event: ISportEvent) => {
      // Event is Open (not finished or resulted, not live event and does not have raceStage)
      const isOpen = event.raceStage !== 'O' && event.rawIsOffCode !== 'Y' && !event.isFinished && !event.isResulted;
      return event.markets.length && isOpen && (this.isEPR(event) || this.isITV(event));
    });
  }

  /**
   * Get Grouped Racing Events by drilldownTagNames
   * @param events
   */
   private getRacingEvents(events: ISportEvent[]): IOffersRacingGroup {
    events.forEach((event: IOffersRacingEvent) => {
        event.link = this.formEdpUrl(event);
        if (this.isOddsAvailable(event)) {
          event.odds = this.getOdds(event);
        }
    });
    return {
      itv: {
        title: this.localeService.getString('racing.itv'),
        name: this.localeService.getString('racing.itv'),
        svgId: '#itv',
        events: events.filter(event => this.isITV(event))
      },
      epr: {
        title: this.localeService.getString('racing.extraPlaceTitle'),
        name: this.localeService.getString('racing.extraPlace'),
        svgId: '#extra-place',
        events: events.filter(event => this.isEPR(event))
      }
    };
  }

  /**
   * Extra Place Event (Market Level)
   * @param event
   */
  private isEPR(event: ISportEvent): boolean {
    return event.markets[0].drilldownTagNames && event.markets[0].drilldownTagNames.includes('MKTFLAG_EPR');
  }

  /**
   * ITV Event (Event Level)
   * @param event
   */
  private isITV(event: ISportEvent): boolean {
    return event.drilldownTagNames && event.drilldownTagNames.includes('EVFLAG_FRT');
  }

  /**
   * @param {object} event
   * Get odds for extra place event
   * @returns {string}
   */
  private getOdds(event: ISportEvent): string {
    return `${event.markets[0].eachWayFactorNum}/${event.markets[0].eachWayFactorDen} the Odds ` +
      `${this.getPlaces(event.markets[0].eachWayPlaces)}` +
      `<b>${event.markets[0].eachWayPlaces}</b>`;
  }

  /**
   * @param {string} places
   * Get race places for extra place event
   * @returns string
   */
  private getPlaces(places: string): string {
    const length = +places || 0;
    let str = '';
    for (let i = 1; i < length; i++) {
      str += `${i}-`;
    }
    return str;
  }

  /**
   * @param {object} event
   * Checking valid odds for event
   * @returns boolean
   */
  private isOddsAvailable(event: ISportEvent): boolean {
    return !!(event.markets[0].isEachWayAvailable && event.markets[0].eachWayFactorNum && event.markets[0].eachWayFactorDen);
  }

  /**
   * Forms event details page.
   * @param {Object} event
   * @return {string}
   */
  private formEdpUrl(event: ISportEvent): string {

      origin = '?origin=offers-and-features';
      return `${this.routingHelperService.formEdpUrl(event)}${origin}`;

    // return this.routingHelperService.formEdpUrl(event);
  }

  /**
   * Update Events
   * @param eventId
   */
  private updateEvents(eventId: number): void {
    this.raceKeys.forEach((key: string) => {
      if (this.groupedEvents[key]) {
        this.groupedEvents[key].events = this.groupedEvents[key].events.filter(item => item.id !== eventId);
      }
    });
    this.allEvents = this.allEvents.filter(item => item.id !== eventId);
    this.changeDetectorRef.markForCheck();
  }

  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

}
