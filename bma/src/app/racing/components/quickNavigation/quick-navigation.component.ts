import { Component, ElementRef, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { ICombinedSportEvents, IGroupedSportEvent, ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SortByOptionsService } from '@racing/services/sortByOptions/sort-by-options.service';
import { NavigationStart, Router } from '@angular/router';
import { RendererService } from '@shared/services/renderer/renderer.service';

import { StorageService } from '@core/services/storage/storage.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { IRaceGridMeeting } from '@app/core/models/race-grid-meeting.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { CommandService } from '@coreModule/services/communication/command/command.service';
import { EventService } from '@sb/services/event/event.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Subscription } from 'rxjs';
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { SessionStorageService } from '@core/services/storage/session-storage.service';

@Component({
  templateUrl: './quick-navigation.component.html',
  selector: 'quick-navigation',
  styleUrls: ['./quick-navigation.component.scss']
})
export class QuickNavigationComponent implements OnChanges, OnInit, OnDestroy {
  @Input() items: IGroupedSportEvent[];
  @Input() showMenu: boolean;
  @Output() readonly showMeetingsListFn: EventEmitter<void> = new EventEmitter();
  @Input() meetingsTitle: any;
  @Input() eventEntity: ISportEvent;

  @Input() sportEventsData?: ISportEvent[];
  @Input() isExtraPlaceAvailable?: boolean;
  @Input() nextRacesComponentEnabled?: boolean;
  @Input() sectionTitle?: any;
  @Input() eventsOrder?:string[];
  @Input() sportName?: string;
  @Input() filter?: string;
  @Input() display?: string;
  @Input() races?:{[key: string]: Partial<IRaceGridMeeting> & {racingType?: string}};
  @Input() categoryId?:number;
  @Input() sportModule?: string;
  @Input() offersAndFeaturedRacesTitle?: string;
  @Input() isMarketAntepost?: boolean;
  private flagsMap: {[key: string]: string} = {
    'UK': 'UIR' ,
    'INT': 'IR',
    'VR': 'LVR'
  };

  public titlesMap: {[key: string]: string} = {};
  hrCategoryId:string = "21";
  isHR: boolean;
  isEntityChanged: boolean = false;
  overlayContentData:ISportEvent[] = [];
  currentUrl: string = '';
  overlayId: any;
  routerState: Subscription;
  isEventAntePost: boolean = false;
  isBrandLadbrokes: boolean;
  loading: boolean = true;

  constructor(
    protected filterService: FiltersService,
    private routingHelperService: RoutingHelperService,
    private sortByOptionsService: SortByOptionsService,
    private router: Router,
    private rendererService: RendererService,
    private storage: StorageService,
    private locale: LocaleService,
    private pubSubService:PubSubService,
    private horseRacingService: HorseracingService,
    private greyhoundService: GreyhoundService,
    private command: CommandService,
    protected eventService: EventService,
    protected windowRef: WindowRefService,
    protected elementRef: ElementRef,
    protected deviceService: DeviceService,
    protected sessionStorageService: SessionStorageService
  ) {}

  ngOnInit() {
    this.isHR = this.eventEntity.categoryId == this.hrCategoryId;
    const titles: {[key: string]: string} = this.storage.get('racingFeatured');
    this.isEventAntePost = this.isAntePostEvent();
    this.filterNavItems(titles);
    this.setNavTitles(titles);
    this.getOverlayHeight();
    this.pubSubService.subscribe('closeOverlay', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      const selector = this.windowRef.document.querySelector('.menu-navigation-opened');
      if(selector) {
        this.closeMenu();
      }
    });

    this.routerState = this.router.events.subscribe((event: NavigationStart) => {
      if(event.navigationTrigger === 'popstate') {
        this.showMenu && this.closeMenu();
        // resetting the default activeTab to By Meeting in EDP overlay switcher on back/forward button click
        if(this.isEventAntePost && this.eventEntity.categoryId == '19') {
          this.sessionStorageService.set('gh-overlay-filterBy', 'by-meeting');
        }
      }
    });
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  /**
   * Handles selection of new racing event by redirecting to event's page.
   */
  selectEvent(event: ISportEvent): void {
    if (event.isExtraPlaceOffer && event.id === this.eventEntity.id
      || !event.isExtraPlaceOffer && this.eventEntity.name === event.name) {
      this.closeMenu();
      return;
    }

    const url = this.routingHelperService.formEdpUrl(event);
    this.sortByOptionsService.set('Price');

    this.router.navigateByUrl(url);
    this.closeMenu();
  }

  getLink(event: ISportEvent): string {
    if (!this.items) {
      return '';
    }
    return this.routingHelperService.formEdpUrl(event);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {object} value
   * @return {number}
   */
  trackById(index: number, value: { id: number }): number {
    return value.id;
  }

  isActiveLink(event: ISportEvent): boolean {
    return event.name === this.eventEntity.name && !event.isExtraPlaceOffer;
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.isHR = this.eventEntity.categoryId == this.hrCategoryId;
    if(!this.deviceService.isDesktop){
    if (changes.showMenu && changes.showMenu.currentValue) {
      this.rendererService.renderer.addClass(document.body, 'menu-opened');
      this.rendererService.renderer.addClass(document.body, 'menu-navigation-opened');
      this.getOverlayHeight();
      this.currentUrl = this.windowRef.nativeWindow.location.href;
      this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', true);
    } else {
      setTimeout(() => { // set timeout duration the same as animation duration in css
        this.rendererService.renderer.removeClass(document.body, 'menu-opened');
        this.rendererService.renderer.removeClass(document.body, 'menu-navigation-opened');
      }, 300);
      this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', false);
    }
    }
    if (changes.eventEntity && changes.eventEntity.currentValue) {
      this.isEntityChanged = true;
      this.isEventAntePost = this.isAntePostEvent();
      this.getOverlayContentData();
    }

    this.pubSubService.subscribe('closeOverlay', this.pubSubService.API.MEETING_OVERLAY_FLAG, (data) => {
      if (!data.flag) {
        this.closeMenu();
        if (this.currentUrl.indexOf(data.id) > -1) {
          this.eventService.hrEventSubscription.next(true);
        }
      }
    });
  }

  getOverlayContentData() {
    const args = {
      selectedTab: this.isHR ? 'featured' : 'todayAndTomorrow',
      filterByDate:'',
      additionalEventsFromModules : this.isHR ? [this.command.API.HR_ENHANCED_MULTIPLES_EVENTS] : []
    }
    const activeService = this.isHR ? this.horseRacingService : this.greyhoundService;
    activeService.getTypeNamesEvents(args).then((events: ICombinedSportEvents) => {
      this.overlayContentData = events.sportEventsData;
      this.loading = false;
    });
  }

  closeMenu() {
    this.isEntityChanged = false;
    this.showMeetingsListFn.emit(); 
  }

  private setNavTitles(titles: {[key: string]: string}): void {
    Object.keys(this.meetingsTitle).forEach((flag) => {
      if (titles && titles[this.flagsMap[flag]]) {
        this.titlesMap[flag] = titles[this.flagsMap[flag]];
      } else {
        this.titlesMap[flag] = this.locale.getString(this.meetingsTitle[flag]);
      }
    });
  }

  private filterNavItems(titles: {[key: string]: string}): void {
    if (titles) {
      if (!Object.keys(titles).includes('IR')) {
        this.items = this.items.filter(this.filterInternational);
      } else if (!Object.keys(titles).includes('UIR')) {
        this.items = this.items.filter(item => item.flag !== 'UK');
      } else if (!Object.keys(titles).includes('LVR')) {
        this.items = this.items.filter(item => item.flag !== 'VR');
      }
    }
  }

  private filterInternational(races: IGroupedSportEvent): boolean {
    return races.flag === 'UK' || races.flag === 'VR' || races.flag === 'ENHRCS';
  }

  getOverlayHeight() {
    if(!this.deviceService.isDesktop){
    this.overlayId = this.windowRef.nativeWindow.setInterval(() => {
      const element = this.windowRef.document.querySelector('.racing-tabs-panel');
      if(element) {
        this.windowRef.nativeWindow.clearInterval(this.overlayId);
        const elHeight = this.windowRef.nativeWindow.innerHeight - Number(element.getBoundingClientRect().bottom.toFixed()) - 40 + 'px';
        const navFrameElement = this.elementRef.nativeElement.querySelector('#nav-frame');
        this.rendererService.renderer.setStyle(navFrameElement, 'max-height', elHeight);
        this.rendererService.renderer.setStyle(navFrameElement, 'min-height', elHeight);
      }
    }, 10);
    }
  }

  isAntePostEvent() {
   return this.eventEntity &&
    this.eventEntity.markets &&
    this.eventEntity.markets[0] &&
    ( this.eventEntity.markets[0].isAntepost === 'true' ||
      this.eventEntity.markets[0].label == 'Ante Post' ||
      (this.eventEntity.categoryId == "19" && !["sb.today", "sb.tomorrow"].includes(this.eventEntity.correctedDay)));
  }

  ngOnDestroy() {
    this.routerState && this.routerState.unsubscribe();
  }
}
