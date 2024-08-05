import { catchError, map, switchMap } from 'rxjs/operators';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import {
  Subscription,
  from,
  Observable,
  of as observableOf,
  throwError,
  forkJoin
} from 'rxjs';
import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ChangeDetectorRef,
  AfterViewInit,
  ViewEncapsulation
} from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { CouponsDetailsService } from '@sb/components/couponsDetails/coupons-details.service';
import { MarketSortService } from '@sb/services/marketSort/market-sort.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';

import { SHOWSTATSENABLEDAYSLIMIT, COUPON_STAT_AVAILABLE_IDS, COUPON_NAMES_CONFIG, MAX_COUPON_WIDGETS, GA_COUPON_STATS_WIDGET, COUPONS_WIDGET } from '@sb/components/couponsDetails/coupons-details.constant';

import { ISportEvent } from '@core/models/sport-event.model';
import { ICouponMarketSelector } from '@shared/components/marketSelector/market-selector.model';
import { ITypeSegment, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';
import { ICoupon } from '@core/models/coupon.model';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GamingService } from '@app/core/services/sport/gaming.service';
import { RoutingState } from '@shared/services/routingState/routing-state.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { CouponsListService } from '../couponsList/coupons-list.service';
import { ICouponSegment } from '../couponsList/coupons-list.model';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { OptaScoreboardLoaderService } from '@edp/services/optaScoreboard/opta-scoreboard-loader.service';
import { OptaScoreboardOverlayService } from '@edp/services/optaScoreboard/opta-scoreboard-overlay.service';
import { ISystemConfig } from '@core/services/cms/models';
import { ILeagueLink } from '@core/services/cms/models/league-links.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { SafeResourceUrl } from '@angular/platform-browser';
import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { IOnboardingOverlay } from './onboarding-coupon-stat-overlay.model';
import { TimeService } from '@core/services/time/time.service';
interface ILeagueLinksMap {
  [obId: string]: { leagueId: string; leagueName: string; };
}

@Component({
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  selector: 'coupons-details',
  templateUrl: './coupons-details.component.html',
  styleUrls: ['./coupons-details.component.scss'],
  providers: [CouponsDetailsService]
})
export class CouponsDetailsComponent extends AbstractOutletComponent implements OnInit, OnDestroy, AfterViewInit {
  couponsList: ICoupon[];
  marketOptions: ICouponMarketSelector[] = [];
  couponNamesConfig;
  couponEvents = [];
  savedCouponEvents = [];
  applyingParams = true;
  applyingList = true;
  isEmptyEvents = false;
  isExpanded = [true, true, true];
  showCoupons = false;
  couponName: string;
  coupons: { name: string }[] = [];
  isBetFilterEnable: boolean = false;
  isEventsUnavailable: boolean = false;
  oddsHeader: string[];
  couponId: string;
  marketFilter: string = '';
  couponFilter: string = '';
  footballService: GamingService;
  eventIdFromEDP: number;
  pageRenderTime: number = 1000;
  couponSegments:  ICouponSegment[];
  leagueLinksMap: ILeagueLinksMap = {};
  couponStatOpenedEvents:any=[];
  isFootball:boolean;
  availableIds:any[];
  maxCouponWidgets:number=MAX_COUPON_WIDGETS;
  includedLeagues:any[];
  hideCoupons: boolean = true;
  public welcomeUrl: SafeResourceUrl | any;
  isShowDiv: boolean = false;
  homeBody: Element;
  isCSWOverlayEnabled : boolean = true;
  widgetType: any;
  isDisplayed: boolean = false;
  isLoading: boolean = true;
  selectedMarketSwitcher: string;
  twoUpMarkets = {'2Up - Instant Win':'2Up - Instant Win','2Up&Win Early Payout':'2Up&Win - Early Payout'}

  private detectListener: number;
  private routeChangeSuccessHandler: Subscription;
  private couponsDetailsSubscription: Subscription;
  private couponsListSubscription: Subscription;
  private sportsConfigSubscription: Subscription;
  public onboardingCoupon: IOnboardingOverlay;
  public showOnboardingOverlay: boolean = false;
  private contentOverlayClassName: string = 'coupon-content-overlay'
  private readonly COUPON_NAMES_CONFIG = COUPON_NAMES_CONFIG;
  CMS_ENDPOINT: string;
  CWS_ONBOARDING : string = 'OnBoardingCSW';
  public readonly COUPON_STAT_AVAILABLE_IDS=COUPON_STAT_AVAILABLE_IDS;
  public readonly SHOWSTATSENABLEDAYSLIMIT=SHOWSTATSENABLEDAYSLIMIT;
  constructor(
    private activatedRoute: ActivatedRoute,
    private sportConfigService: SportsConfigService,
    private deviceService: DeviceService,
    private pubSubService: PubSubService,
    private marketSortService: MarketSortService,
    protected elementRef: ElementRef,
    private router: Router,
    protected domToolsService: DomToolsService,
    protected windowRefService: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    public couponsDetailsService: CouponsDetailsService,
    private cacheEventsService: CacheEventsService,
    private routingState: RoutingState,
    private couponsListService: CouponsListService,
    private routingHelperService: RoutingHelperService,
    private cmsService: CmsService,
    private optaScoreboardLoaderService: OptaScoreboardLoaderService,
    private optaScoreboardOverlayService: OptaScoreboardOverlayService,
    // eslint-disable-next-line
    private updateEventService: UpdateEventService, // DO NOT REMOVE: needed for events subscription on init of this dependency
    private gtmService: GtmService,
    private userService: UserService,
    private storageService: StorageService,
    private rendererService: RendererService,
    private timeService:TimeService
  ) {
    super()/* istanbul ignore next */;
    this.couponNamesConfig = this.COUPON_NAMES_CONFIG;
  }

  ngOnInit() {
    this.changeDetectorRef.detach();
    this.CMS_ENDPOINT = environment.CMS_ENDPOINT.split('/api')[0];
    this.detectListener = this.windowRefService.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
      this.eventIdFromEDP && this.scrollToPreviousState();
    }, 500);

    const couponName: string = this.activatedRoute.snapshot.paramMap.get('couponName');
    this.couponId = this.activatedRoute.snapshot.paramMap.get('couponId');
    this.sportsConfigSubscription = this.sportConfigService.getSport('football').subscribe((sportService: GamingService) => {
      this.footballService = sportService;
      this.footballService.extendRequestConfig('coupons');
      this.setCouponsData(couponName);
    });

    if (this.deviceService.isTablet || this.deviceService.isTabletLandscape) {
      this.setTabletTopTitleWidth();

      this.pubSubService.subscribe(
        'CouponsDetailsCtrl',
        this.pubSubService.API.SHOW_HIDE_WIDGETS,
        () => this.setTabletTopTitleWidth()
      );
    }

    this.routeChangeSuccessHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        const currentCouponId: string = this.activatedRoute.snapshot.paramMap.get('couponId');
        const currentCouponName: string = this.activatedRoute.snapshot.paramMap.get('couponName');
        const isRouteSegment: boolean = this.activatedRoute.snapshot.data['segment'] === 'couponsDetails';

        if (this.couponId !== currentCouponId && isRouteSegment) {
          this.marketFilter = '';
          this.couponId = currentCouponId;
          this.applyingParams = true;
          this.setCouponsData(currentCouponName);
        }
      }
    });

    // Block quick bet on coupon details page if configured in CMS
    this.couponsDetailsService.isQuickBetBlocked().subscribe((isQuickBetBlocked: boolean) => {
      if (!isQuickBetBlocked) { return; }

      this.pubSubService.subscribe('CouponsDetailsCtrl', this.pubSubService.API.BETSLIP_LOADED, () => {
        this.blockQuickBet();
      });
      this.blockQuickBet();
    });

    this.pubSubService.subscribe('CouponsDetailsCtrl', this.pubSubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.deleteEvent(eventId);
    });
    const sdmTag=document.createElement('div');
    sdmTag.id='sdm-scoreboards-modal';
    document.body.appendChild(sdmTag);
    this.getShowStatsIncludedLeagues();
  }

  private getShowStatsIncludedLeagues()
  {
    this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
      if (sysConfig && sysConfig.CouponStatsWidget && sysConfig.CouponStatsWidget) {
        const keys = Object.keys(sysConfig.CouponStatsWidget);
        this.includedLeagues = keys.filter(key=>sysConfig.CouponStatsWidget[key]);
       }
    });
  }

  closeFirstOpenedBoard() {
    const removeEvent = this.couponStatOpenedEvents.shift();
    if(removeEvent.couponStatId){
    this.availableIds.push(removeEvent.couponStatId);
    }
    removeEvent.isCouponScoreboardOpened = undefined;
    this.removeTagFromDom(removeEvent);
    this.sendGTMData(removeEvent);
  }

  private removeTagFromDom(removeEvent: ISportEvent) {
    if(document.getElementById(removeEvent.couponStatId)){
    document.getElementById(removeEvent.couponStatId).remove();
    removeEvent.couponStatId = undefined;
    const spinner=document.getElementById('spin' + (removeEvent.id));
    if(spinner)
    {
      spinner.remove();
    }
    }
  }

  closeCurrentBoard(currentEvent: ISportEvent) {
    if(currentEvent.couponStatId){
    this.availableIds.push(currentEvent.couponStatId);
    }
    const currentEventIndex = this.couponStatOpenedEvents.findIndex((event) => event.id === currentEvent.id);
    this.couponStatOpenedEvents.splice(currentEventIndex, 1);
    currentEvent.isCouponScoreboardOpened = undefined;
    this.removeTagFromDom(currentEvent);
  }

  private initElements(): void {
    this.homeBody = this.deviceService.isWrapper ?
                          this.windowRefService.document.querySelector('body') : this.windowRefService.document.querySelector('html, body');
  }

   sendGTMData(removeEvent: ISportEvent){
    const gtmData = {
      "event": "trackEvent",
      "eventAction": "click",
      "eventCategory": "coupon stats widget",
      "eventLabel": 'hide stats',
      "categoryID": removeEvent.categoryId,
      "typeID": removeEvent.typeId,
      "eventID": removeEvent.id
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  public setGtmData(data, label?, buttonText?): void {
         const gtmData = {
             event: data.event,
             'component.CategoryEvent': data.categoryEvent,
             'component.LabelEvent': label? label: data.labelEvent,
             'component.ActionEvent': data.actionEvent,
             'component.PositionEvent': data.positionEvent,
             'component.LocationEvent': data.locationEvent,
             'component.EventDetails': buttonText? buttonText: data.eventDetails,
             'component.URLClicked': data.URLClicked
        };
        this.gtmService.push(gtmData.event, gtmData);
      }

  onExpand(currentEvent: ISportEvent) {

    currentEvent.isCouponScoreboardOpened = !currentEvent.isCouponScoreboardOpened;
    if (currentEvent.isCouponScoreboardOpened) {
      if(this.isCSWOverlayEnabled && this.userService.username && this.deviceService.requestPlatform === 'mobile'
          && this.storageService.get(this.CWS_ONBOARDING) && (this.userService.username === this.storageService.get(this.CWS_ONBOARDING).user &&
          this.storageService.get(this.CWS_ONBOARDING).widget === 'couponAndMarketSwitcherWidget')) {
            this.getOnboardingOverlayCMS('coupon-stats-widget');
          }
      this.couponStatOpenedEvents.push(currentEvent);
      if (this.couponStatOpenedEvents.length > this.maxCouponWidgets) {
        this.closeFirstOpenedBoard();
      }
      const newId: any = this.availableIds.shift();
      currentEvent.couponStatId = newId;
    }
    else {
      this.closeCurrentBoard(currentEvent);
    }
  }

  ngAfterViewInit(): void {
    this.changeDetectorRef.detectChanges();
  }

  ngOnDestroy() {
    this.hideCoupons = true;
    this.marketFilter = '';
    this.applyingParams = true;
    this.cacheEventsService.clearByName('coupons');
    this.windowRefService.nativeWindow.clearInterval(this.detectListener);
    // unSubscribe LS Updates via liveServe PUSH updates (iFrame)!
    this.footballService.unSubscribeCouponsForUpdates('football-coupons');
    this.pubSubService.unsubscribe('CouponsDetailsCtrl');
    this.routeChangeSuccessHandler && this.routeChangeSuccessHandler.unsubscribe();
    this.couponsDetailsSubscription && this.couponsDetailsSubscription.unsubscribe();
    this.couponsListSubscription && this.couponsListSubscription.unsubscribe();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.blockQuickBet(false);
    this.optaScoreboardOverlayService.destroyOverlay();
    if(this.homeBody) {
      this.rendererService.renderer.removeClass(this.homeBody, this.contentOverlayClassName);
    }
  }

  trackById(index: number, element: ISportEvent): string {
    return element.id ? `${index}${element.id}` : index.toString();
  }

  trackByTypeId(index: number, element: ITypeSegment): string {
    return `${index}${element.typeId}${element.deactivated}`;
  }

  changeAccordionState(i: number, value: boolean): void {
    this.isExpanded[i] = value;
  }

  isDisplay() {
    this.isDisplayed = true;
  }
  /**
   * filterEvents()
   * @param {string} marketFilter
   */
  filterEvents(marketFilter: string): void {
    this.selectedMarketSwitcher = '';
    this.changeDetectorRef.detectChanges();
    this.hideCoupons = false;
    this.marketFilter = marketFilter;
    this.selectedMarketSwitcher = this.twoUpMarkets[marketFilter];
    this.marketSortService.setMarketFilterForMultipleSections(this.savedCouponEvents, marketFilter);
    this.isEventsUnavailable = this.getEventsIsUnavailable;
    this.oddsHeader = this.couponsDetailsService.setOddsHeader(this.marketOptions, marketFilter);

    // filter events and keep reference to the array
    this.couponEvents.length = 0;
    this.couponEvents.push(...this.filteredEvents());
    this.removeAllWidgetsFromDom();

  }

  /**
 *
 * @param selectedCoupon {string[]}
 */
  filterCoupons(selectedCoupon: string[]): void {
    this.selectedMarketSwitcher = '';
    this.couponFilter = selectedCoupon[0];
    let coupon;
    this.couponSegments.every(segment => {
      if (!coupon) {
        coupon = segment.coupons.find((coup) => coup.name === this.couponFilter);
        return !coupon ? true : false;
      }
    });
    const couponName = this.routingHelperService.encodeUrlPart(coupon.name);
    this.router.navigate([`/coupons/football/${couponName}/${coupon.id}`]);
  }

  /**
   * showCouponsList()
   */
  showCouponsList(): void {
    this.showCoupons = !this.showCoupons;
    this.scrollToTop();
  }

  /**
   * goToPage()
   * @param {string} path
   * @returns {void|boolean}
   */
  goToPage(path: string): Promise<boolean>| boolean {
    return path ? this.router.navigateByUrl(path) : false;
  }

  filteredEvents(): ITypeSegment[] {
    return this.savedCouponEvents.filter(event => !event.deactivated);
  }

  handleMatchesMarketSelectorEvent(event: ILazyComponentOutput): void {
    if (event.output === 'filterChange') {
      this.filterEvents(event.value);
    }
  }

  openLeagueTable(events: ITypeSegment): void {
    this.optaScoreboardOverlayService.setOverlayData({
      overlayKey: 'leagueTable',
      data: this.leagueLinksMap[events.typeId]
    });
    this.sendGTM(events.events[0]);
    this.optaScoreboardOverlayService.showOverlay();
  }

  protected getStickyElementsHeight(): number {
    const couponsContainer = this.windowRefService.document.querySelector('.coupons-container-js');
    return !couponsContainer ? 0 : this.domToolsService.getOffset(couponsContainer).top;
  }

  private sendGTM(event: ISportEvent): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'in-line stats',
      eventAction: 'league table',
      eventLabel: event.typeName,
      categoryID: event.categoryId,
      typeID: `${event.typeId}`
    }]);
  }

  private updatePreviousStateInfo(): void {
    const previousSegment = this.routingState.getPreviousSegment();
    if (previousSegment !== 'eventMain') {
      return;
    }
    const regexpResult = /\/([0-9]*)\//.exec(this.routingState.getPreviousUrl()),
      eventIdFromEDP = regexpResult && +regexpResult[1];
    if (!eventIdFromEDP) {
      return;
    }
    const allEvents = this.couponEvents.map(coupon => coupon.events)
      .reduce((firstArray, secondArray) => firstArray.concat(secondArray), []);
    const eventIndex = allEvents.findIndex(event => event.id === eventIdFromEDP);
    if (eventIndex === -1) {
      return;
    }
     const typeID = allEvents[eventIndex].typeId;
     const typeIndex = this.couponEvents.findIndex(type => type.typeId === typeID);
    this.isExpanded[typeIndex] = true;
    this.eventIdFromEDP = eventIdFromEDP;
  }

  /**
   * If redirecting back from coupons EDP, scroll to previous position on coupons page
   */
  private scrollToPreviousState(): void {
    const document: HTMLDocument = this.windowRefService.document,
      eventElement = document.querySelector(`.coupon-event-${this.eventIdFromEDP}`);
      // eventElement = document.querySelector(`#acc-${this.typeID}`);
    if (!eventElement) {
      return;
    }
    const eventElementOffset = this.domToolsService.getOffset(eventElement).top;
    setTimeout(() => {
      this.windowRefService.nativeWindow.scroll(0, eventElementOffset - this.getStickyElementsHeight());
      this.eventIdFromEDP = 0;
    });
  }

  private setCouponsData(couponName: string): void {
    const couponTitle = this.getCouponName(couponName);
    this.selectedMarketSwitcher = '';
    this.marketOptions = [];
    this.couponsDetailsService.isGoalscorerCoupon = couponTitle.toLowerCase() ===
      this.couponNamesConfig.goalscorerCouponName.toLowerCase();
    this.footballService.unSubscribeCouponsForUpdates('football-coupons');
    this.getCouponsData(couponTitle);
    this.getCouponsListData();
  }

  /**
   * eventsIsUnavailable()
   * @returns {boolean}
   */
  private get getEventsIsUnavailable(): boolean {
    if (this.isEmptyEvents) {
      return true;
    }

    return this.couponsDetailsService.isCustomCoupon ? false : !_.some(this.couponEvents, (couponEvent: ITypeSegment) => {
      return _.some(couponEvent.groupedByDate, (group: IGroupedByDateItem) => {
        return group.deactivated === false || group.deactivated === undefined;
      });
    });
  }
  private set getEventsIsUnavailable(value:boolean){}

  /**
   * getCouponsListData()
   */
  private getCouponsListData(): void {
    this.couponsListSubscription = from(this.footballService.coupons())
      .pipe(switchMap((data: ICoupon[]) => {
        this.applyingList = false;
        this.couponsList = data;
        this.couponFilter = this.couponsList.find((coupon) => coupon.id === this.couponId).name;
        if (this.couponsList && this.couponsList.length) {
          this.couponsListService.getCouponSegment().subscribe((segments: ICouponSegment[]) => {
            this.couponSegments = this.couponsListService.groupCouponBySegment(this.couponsList as any, segments);
            this.groupCoupons();
          });
        }
        const currentCoupon = this.couponsList.find((coupon: ICoupon) => coupon.id === this.couponId);
        this.couponName = this.getCouponName(currentCoupon.name);
        return this.couponsDetailsService.isBetFilterEnable(currentCoupon);
      })).subscribe((isEnable: boolean) => {
      this.isBetFilterEnable = isEnable;
      this.hideSpinner();
    }, (error) => {
        this.applyingList = false;
        this.isBetFilterEnable = false;
        this.couponsList = [];
        this.coupons = [];
        console.warn('Error:', error);
        this.showError();
    });
  }

  private groupCoupons(): void {
    if(this.couponSegments && this.couponSegments.length){
        this.coupons = [];
        this.couponSegments.forEach((couponSegment) => {
        couponSegment.coupons.forEach((coupon) => {
          this.coupons.push({ name: coupon.name });
        })
      });
    }
  }

  /**
   * getCouponsData()
   * @param {string} couponName
   */
  private getCouponsData(couponName: string): void {
    this.couponsDetailsSubscription = forkJoin(
      this.couponsDetailsService.getCouponEvents(this.couponId, couponName, this.footballService),
      this.initCouponLeagueLinks(this.couponId),
    ).subscribe(([{ coupons, options }, leagueLinks]: [{ coupons: ISportEvent[], options: ICouponMarketSelector[]}, ILeagueLink[]]) => {
      this.loadCouponEvents(coupons, options, leagueLinks);
    }, () => this.showError());
  }

  /**
   * Load Coupons Events
   * @param {ISportEvent[]} coupons
   * @param {ICouponMarketSelector[]} options
   * @param {ILeagueLink[]} leagueLinks
   */
  private loadCouponEvents(coupons: ISportEvent[], options: ICouponMarketSelector[], leagueLinks: ILeagueLink[]): void {
    this.savedCouponEvents = this.couponsDetailsService.groupCouponEvents(coupons, this.footballService);
    this.couponEvents = this.savedCouponEvents.slice();
    this.isEmptyEvents = _.isEmpty(this.couponEvents);
    this.isEventsUnavailable = this.getEventsIsUnavailable;
    this.applyingParams = false;
    this.leagueLinksMap = this.buildLeagueLinksMap(leagueLinks);

    if (!this.isEmptyEvents) {
      this.footballService.subscribeCouponsForUpdates(coupons, 'football-coupons');
      this.marketOptions = options;
      this.hideCoupons = this.marketOptions && this.marketOptions.length > 0;
    }
    if(!this.applyingParams && this.hideCoupons && !this.couponsDetailsService.isCustomCoupon && !this.isEventsUnavailable) {
      const CWS_ONBOARDING = this.storageService.get(this.CWS_ONBOARDING);
      const username = CWS_ONBOARDING ? CWS_ONBOARDING.user : '';
      const widget = CWS_ONBOARDING ? CWS_ONBOARDING.widget : '';
      const status =(this.userService.username === username && (widget === 'couponAndMarketSwitcherWidget' || widget === 'coupon-stats-widget'));
      if((this.isCSWOverlayEnabled && this.userService.username && this.deviceService.requestPlatform === 'mobile')
      && !status) {
        this.getOnboardingOverlayCMS('couponAndMarketSwitcherWidget');
      }
    }
    this.checkIsShowStatsEnabled();
    this.updatePreviousStateInfo();
  }

  private checkIsShowStatsEnabled() {
    this.availableIds = _.clone(this.COUPON_STAT_AVAILABLE_IDS);
    this.couponStatOpenedEvents = [];
    if (this.footballService.isFootball) {
      this.isFootball = true;
      this.couponEvents.forEach(e => {
        if (this.includedLeagues.includes(e.typeId.toString())) {
          e.events.forEach((event: ISportEvent) => {
            if (this.getdaysToEventStart(event) <= this.SHOWSTATSENABLEDAYSLIMIT) {
              event.isShowStatsEnabled = true;
            }
          })
        }
      });
    }
  }

  removeAllWidgetsFromDom() {
    this.couponStatOpenedEvents.forEach((event) => {
      if (event.couponStatId) {
        this.availableIds.push(event.couponStatId);
      }
      event.isCouponScoreboardOpened = undefined;
      this.removeTagFromDom(event);
    });
    this.couponStatOpenedEvents = [];
  }

  private getdaysToEventStart(e:ISportEvent):number{
   return  Math.ceil(-1 * (this.timeService.daysDifference(e.startTime)));
  }

  private initCouponLeagueLinks(couponId: string): Observable<ILeagueLink[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig): boolean => config && config.StatisticsLinks && config.StatisticsLinks.leagues),
      switchMap((enabled: boolean): Observable<[ILeagueLink[], HTMLElement]> =>
        enabled ? forkJoin(this.cmsService.getCouponLeagueLinks(couponId), this.initScoreboardOverlay())
          : throwError('Coupon League Links are disabled in CMS')),
      switchMap(([links, scoreboardOverlay]: [ILeagueLink[], HTMLElement]) => {
        switch (true) {
          case !links:
          case !links.length: return throwError(`Coupon League Links are not available in CMS for the '${couponId}' couponId`);
          case !scoreboardOverlay: return throwError(`Could not initialize Scoreboard Overlay`);
          default: return observableOf(links);
        }
      }),
      catchError(error => {
        console.warn(error);
        return observableOf([]);
      })
    );
  }

  private buildLeagueLinksMap(leagueLinks: ILeagueLink[]): ILeagueLinksMap {
    return leagueLinks.reduce((linksMap, link) =>
      Object.assign(linksMap, { [link.obLeagueId]: { leagueId: link.dhLeagueId, leagueName: link.linkName } }), {});
  }

  private initScoreboardOverlay(): Observable<HTMLElement> {
    return this.optaScoreboardLoaderService.loadBundle().pipe(
      map(() => this.optaScoreboardOverlayService.initOverlay()));
  }

  private scrollToTop(): void {
    const couponsListElem = this.elementRef.nativeElement.querySelector('.coupons-list');
    if (this.showCoupons && couponsListElem) {
      this.windowRefService.document.body.scrollTop = 0; // For Safari
      this.windowRefService.document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
      couponsListElem.scrollTop = 0; // Element scrollTop
    }
  }

  /**
   * setTabletTopTitleWidth()
   */
  private setTabletTopTitleWidth(): void {
    const couponsTopTitle = this.elementRef.nativeElement.querySelector('.coupons-top-title');
    if (!couponsTopTitle) {
      return;
    }

    const pageContent = this.windowRefService.document.getElementById('content');

    const elmWidth = this.domToolsService.getWidth(pageContent);

    this.domToolsService.css(couponsTopTitle, 'width', `${elmWidth}px`);
    this.domToolsService.css(couponsTopTitle, 'transition', 'initial');
  }

  /**
   * deleteEvent()
   * @param {number} eventId
   */
  private deleteEvent(eventId: number): void {
    this.savedCouponEvents.forEach((section: ITypeSegment, i: number) => {
      if (section) {
        this.deleteIndex(section, eventId, i);
        section.groupedByDate.forEach((groupedSection: IGroupedByDateItem, j: number) => {
          this.deleteIndex(groupedSection, eventId, j);
        });
      }
    });
  }

  private deleteIndex(section: ITypeSegment | IGroupedByDateItem, eventId: number, index: number): void {
    const eventIndex = section.events.findIndex((event: ISportEvent) => Number(event.id) === Number(eventId));
    if (eventIndex !== -1) {
      section.events.splice(eventIndex, 1);
      if (!section.events.length) {
        section.events.splice(index, 1);
      }
    }
  }

  /**
   * getCouponName()
   * @param {string} couponName
   * @returns {string}
   */
  private getCouponName(couponName: string): string {
    const couponTitle = couponName.replace(/-/g, ' ');
    const overUnderCoupon = this.couponNamesConfig.overUnderOriginalName.toLowerCase() === couponTitle.toLowerCase()
      && this.couponNamesConfig.overUnderOriginalName;
    const ukCoupon = this.couponNamesConfig.ukCoupon.toLowerCase() === couponTitle.toLowerCase()
      && this.couponNamesConfig.ukCoupon;

    return overUnderCoupon || ukCoupon || couponTitle;
  }

  private blockQuickBet(block: boolean = true): void {
    this.pubSubService.publish(this.pubSubService.API.BLOCK_QUICK_BET, block);
  }

  private getOnboardingOverlayCMS(requestParam): void {
    this.cmsService.getOnboardingOverlay(requestParam).subscribe((onboardingOverlay: IOnboardingOverlay) => {
      this.isCSWOverlayEnabled = onboardingOverlay.isEnable;
      if (onboardingOverlay.isEnable) {
        this.initElements();
        this.rendererService.renderer.addClass(this.homeBody, this.contentOverlayClassName);
        this.storageService.set(this.CWS_ONBOARDING, { user: this.userService.username, displayed: true, widget: requestParam });
        if(requestParam === 'couponAndMarketSwitcherWidget') {
          this.setGtmData(COUPONS_WIDGET);
          this.widgetType = COUPONS_WIDGET;
        } else if (requestParam === 'coupon-stats-widget') {
          this.isShowDiv = false;
          this.setGtmData(GA_COUPON_STATS_WIDGET);
          this.widgetType = GA_COUPON_STATS_WIDGET;
        }
       }
        this.showOnboardingOverlay = true;
        this.welcomeUrl = `${this.CMS_ENDPOINT}${onboardingOverlay.imageUrl}`;
        this.onboardingCoupon = onboardingOverlay;
        this.isLoading = false;
    }, (error) => {
      console.warn(error);
    });
  }

  imageclose(location:string) {
    location === 'close' ? this.setGtmData(this.widgetType, location) : this.setGtmData(this.widgetType, `${this.onboardingCoupon.buttonText}`, `${this.onboardingCoupon.buttonText} cta`);
    this.isShowDiv = true;
    this.showOnboardingOverlay = false;
  }
}
