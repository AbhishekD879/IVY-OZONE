import {
  from as observableFrom,
  empty as observableEmpty,
  of as observableOf,
  throwError,
  Subscription,
  Observable,
  forkJoin as observableForkJoin
} from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';
import { Component, OnChanges, Input, OnDestroy, OnInit, ChangeDetectorRef, SimpleChanges, ElementRef, ViewChild,
   ViewContainerRef } from '@angular/core';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { IConstant } from '@core/services/models/constant.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';
import { IGroupedSportEvent, ISportEvent } from '@core/models/sport-event.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { ISystemConfig } from '@core/services/cms/models';
import { IPoolModel } from '@shared/models/pool.model';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { IStreamControl } from '@app/tote/models/stream-control.model';
import { UK_TOTE_CONFIG } from '@uktote/constants/uk-tote-config.contant';
import { IBreadcrumb } from '@app/shared/models/breadcrumbs.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FORECAST_CONFIG } from '@lazy-modules/forecastTricast/constants/forecast-tricast-config.contant';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import {
  IPerformGroupConfig,
  IQuantumLeapTimeRangeConfig
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { IRacingHeader } from '@app/shared/models/racing-header.model';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import { RacingGaService } from '@racing/services/racing-ga.service';
import environment from '@environment/oxygenEnvConfig';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { IRacingEdpMarket } from '@core/services/cms/models/racing-edp-market.model';
import { HRTabs } from '@app/lazy-modules/racingFeatured/components/racingFeatured/constant';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';
import { IDelta } from '@app/core/models/delta-object.model';
import { ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';

/**
 * @class Racing event controller'responseCreationTime'
 */
@Component({
  templateUrl: 'racing-event.component.html',
  styleUrls: ['./racing-event.component.scss'],
  selector: 'racing-event'
})
export class RacingEventComponent implements OnInit, OnDestroy, OnChanges {
  @Input() eventId: number;
  @Input() sportName: string;
  @Input() origin: string;
  @Input() selectedTypeName: string;
  @Input() selectedMarketPath: string;
  @Input() selectedMarketTypePath: string;
  @Input() racingsMap: any;
  @Input() racingTypeNames: string[];
  @Input() racingInMeeting: ISportEvent[];
  @Input() eventEntity: ISportEvent;
  @Input() loadFloatingMsgComp: boolean;
  @Input() presimStopTrackInterval: number;
  @Input() filter: string;
  @Input() images: string;
  @Input() onExpand: Function;
  @Input() streamControl?: IStreamControl;
  @Input() meetingsTitle: any;
  @Input() quickNavigationItems: IGroupedSportEvent[];
  @Input() sportEventsData?: ISportEvent[] = [];
  @ViewChild('nativeVideoPlayerPlaceholder', {static: true}) nativeVideoPlayerPlaceholderRef: ElementRef;

  spinner = {
    isActive: false
  };
  racingPostSummary;
  showLess: boolean = true;
  allowFlexTabs: number;
  showMeetings: boolean;
  pools: IPoolModel[];
  poolEventEntity: ISportEvent;
  poolEventIds: string[];
  expandedSummary: boolean[][];
  outcomeInfo: boolean;
  selectedMarket: string;
  selectedMarketType: string;
  closeWatchFreeDialog: Function;
  preloadStream: boolean;
  toteLabel: string;
  winOrEWLabel: string = 'Win or E/W';
  forecastLabel: string = 'Forecast';
  tricastLabel: string = 'Tricast';
  sortBy: string = 'Price';
  sortOptionsEnabled: boolean = false;
  ewLabel: string;
  breadcrumbsItems: IBreadcrumb[];
  racingSpecialsDate: string = '';
  isNotAntepostOrSpecials: boolean;
  isRacingSpecialsCondition: boolean;
  isGreyhoundEdp: boolean = false;
  hideSilk: boolean;
  bellActive: boolean;
  alertsVisible: boolean = false;
  isRibbonEventName: boolean = false;
  isForecastTricast: boolean;
  forecastTricastMarket: IMarket;
  isWrapper: boolean = false;
  liveCommentary: { [key: string]: string };
  termsBeforeMarketAvailable: { [key: string]: boolean | string } = {};
  marketsTabs: ISwitcherConfig[] = [];
  specialsLoaded: boolean = false;
  performConfig: IPerformGroupConfig;
  shouldShowCSBIframe: boolean;
  isMediaAvailable: boolean = false;
  isRacingPostVerdictAvailable: boolean;
  showVerdict: boolean = false;
  racingPostVerdictData: IRacingPostVerdict;
  isActiveRangeForQuantumLeap: boolean = true;
  isMarketAntepost: boolean;
  showQuantumLeap: boolean;
  isMarketDescriptionAvailable: boolean = false;
  RACING_EDP_MARKETS: IRacingEdpMarket[] = [];
  isToteForecastTricast: boolean = false;
  hasSortedMarketsFromCms: boolean = false;
  isDescriptionAvailable: boolean = false;
  delta: IDelta;

  isInfoHidden: {'info': boolean};
  isSpOnly: boolean;
  toolTipArgs: { [key: string]: string; };
  showToolTip: boolean;
  secondaryMarketsTooltip: string;
  marketContainer: HTMLElement;
  showFullscreen: boolean = false;
  isFullScreenConfig: boolean = false;
  eachWayMarket: IMarket;
  spotlightedOutcome: IOutcome;

  readonly MARKETS_CONTAINER: string = '.markets-container';

  readonly HR_TABS = HRTabs;
  activeUserTab = this.HR_TABS.MARKETS;
  protected label: string;
  public readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  protected readonly VIEW_ACTION: string = 'view';
  private config;
  private document;
  private detectListener: number;
  protected isHR: boolean;
  private routeEventsListener: Subscription;
  private ukToteDataSubscription: Subscription;
  private secondaryMarketsSubscription: Subscription;
  private readonly SECONDARY_MARKETS = 'SecondaryMarketsTooltip';
  private hasMarketType: boolean = false;
  private isVideoHandled: boolean =  false;
  protected BIRMarketsEnabled: string[] = [];
  fullScreenDrillDownTags: string[] = [''];
  insightsDrillDownTags: string[] = [''];
  isRaceCard: boolean = false;
  isFutureMeetingsOverlay: boolean;
  eventsOrder: Array<string>;
  protected isWebStreamBet: boolean; 

  @ViewChild('marketsContainer', {read: ViewContainerRef, static: false}) set marketDescriptionContainer(container: ViewContainerRef) {
    if (!container) {
      return;
    }
    this.marketContainer = this.elementRef.nativeElement.querySelector(this.MARKETS_CONTAINER);
  }

  constructor(
    protected windowRef: WindowRefService,
    protected timeService: TimeService,
    protected pubSubService: PubSubService,
    protected nativeBridgeService: NativeBridgeService,
    protected ukToteService: UkToteService,
    protected lpAvailabilityService: LpAvailabilityService,
    protected deviceService: DeviceService,
    protected gtmService: GtmService,
    protected streamTrackingService: StreamTrackingService,
    protected dialogService: DialogService,
    protected filterService: FiltersService,
    protected localeService: LocaleService,
    protected horseracing: HorseracingService,
    protected routingHelperService: RoutingHelperService,
    protected cmsService: CmsService,
    protected tools: CoreToolsService,
    protected sbFilters: SbFiltersService,
    protected router: Router,
    protected location: Location,
    protected changeDetectorRef: ChangeDetectorRef,
    protected sortByOptionsService: SortByOptionsService,
    protected route: ActivatedRoute,
    protected watchRulesService: WatchRulesService,
    protected seoDataService: SeoDataService,
    protected elementRef: ElementRef,
    protected racingGaService: RacingGaService
  ) {
    /**
     * Max amount of markets tabs to use flex-tabs style
     * @member {number}
     */
    this.allowFlexTabs = horseracingConfig.MARKET_FLEX_TABS;
    this.config = horseracingConfig;
    this.document = this.windowRef.nativeWindow.document;

    this.handleAlerts = this.handleAlerts.bind(this);

    this.sortOptionsEnabledFn = this.sortOptionsEnabledFn.bind(this);

    if(this.router && this.router.url) {
      this.isRaceCard = this.router.url.includes('horse-racing/build-your-own-race-card');
    }
  }

  ngOnInit(): void {
    if (this.eventEntity) {
      this.eventsOrder = this.config.order.EVENTS_ORDER;
      this.racingInMeeting = this.racingInMeeting && this.racingInMeeting.filter(race => race.categoryId !== '39');
      const currentEvent = this.racingInMeeting && this.racingInMeeting.find((eventEntity: ISportEvent) => eventEntity.id.toString() === this.eventId.toString());
      if (currentEvent) {
        this.eventEntity.rawIsOffCode = currentEvent.rawIsOffCode;
      }
      this.goToSeo(this.eventEntity);
      this.racingPostVerdictData = this.eventEntity.racingPostVerdict;
      this.setMarketsTooltip();
      this.hasMarketType = !!this.route.snapshot.params['market'];

      this.isWrapper = this.deviceService.isWrapper;
      const order = ['customOrder', 'displayOrder', 'name'],
        isTotepoolMarket = this.selectedMarketPath === UK_TOTE_CONFIG.marketPath,
        isTricastMarket = this.selectedMarketPath === FORECAST_CONFIG.tricastMarketPath,
        isForecastMarket = this.selectedMarketPath === FORECAST_CONFIG.forecastMarketPath,
        sortedMarkets = this.eventEntity.sortedMarkets;
      this.isHR = this.eventEntity.categoryCode === 'HORSE_RACING';
      this.isGreyhoundEdp = this.eventEntity.categoryCode !== 'HORSE_RACING';
      this.isSpOnly = this.isSp(this.eventEntity);

      this.changeDetectorRef.detach();
      this.detectListener = this.windowRef.nativeWindow.setInterval(() => {
        this.changeDetectorRef.detectChanges();
      }, 100);

      this.nativeBridgeService.eventPageLoaded(this.eventId.toString(), this.sportName);
      this.checkAlerts();
      this.document.addEventListener('eventAlertsEnabled', this.handleAlerts);
      
      this.sortByOptionsService.isGreyHound = this.isGreyhoundEdp;
      this.sortBy = this.sortByOptionsService.get();
      this.ewLabel = this.localeService.getString('sb.winOrEachWay');

      // Totepool tab should be activated only after Tote data is initialized
      const marketByPath = !isTotepoolMarket && this.selectedMarketPath && this.getMarketByPath(sortedMarkets, this.selectedMarketPath);

      // If not specified explicitly, either the Win or E/W tab, or the first tab in the list is activated by default
      const marketToSelect = !isTotepoolMarket && !isForecastMarket && !isTricastMarket && marketByPath ||
        this.getMarketByLabel(sortedMarkets, this.ewLabel);

      // For non-Totepool markets set the selectedMarket property and adjust location for wrong or incomplete URLs
      !isTotepoolMarket && !isTricastMarket && !isForecastMarket && this.selectFallbackMarket(marketToSelect);

      this.racingTypeNames = _.sortBy(this.racingTypeNames);

      this.eventEntity.markets = this.filterService.orderBy(this.eventEntity.markets, order);

      this.eventEntity.filteredTime = this.filterDate(this.eventEntity.startTime);
      this.expandedSummary = [];

      this.outcomeInfo = _.some(this.eventEntity.markets, (marketEntity: IMarket) => {
        return _.some(marketEntity.outcomes, (outcomeEntity: IOutcome) => !!outcomeEntity.racingFormOutcome);
      });

      this.getBIRMarkets();

      if (_.has(this.eventEntity.racingFormEvent, 'overview')) {
        // Set init summary text (by def show less)
        this.eventEntity.racingFormEvent.overview = `${this.eventEntity.racingFormEvent.overview}`;
        this.racingPostSummary = `${this.eventEntity.racingFormEvent.overview.substring(0, 100)} ... `;
      }

      // UKTOTE
      this.ukToteDataSubscription = this.cmsService.getSystemConfig().pipe(
        switchMap((config: ISystemConfig) => {
          this.sortOptionsEnabled = config.SortOptions && config.SortOptions.enabled && (this.isHR || this.isGreyhoundEdp) && !this.isAntepostMarket();
          this.performConfig = config.performGroup;
          const quantumLeapTimeRangeConfig: IQuantumLeapTimeRangeConfig = config.quantumLeapTimeRange;

          this.isActiveRangeForQuantumLeap = this.sportName !== 'greyhound' && this.eventEntity.isUKorIRE &&
            quantumLeapTimeRangeConfig && quantumLeapTimeRangeConfig.startTime &&
            quantumLeapTimeRangeConfig.endTime ?
            this.timeService.isActiveRangeForCustomTime(
              quantumLeapTimeRangeConfig.startTime,
              quantumLeapTimeRangeConfig.endTime
            ) : true;

          // Live Sim is not available for events from groups other than UK or IE and not available for greyhounds
          this.showQuantumLeap = this.eventEntity && this.eventEntity.isUKorIRE && this.sportName !== 'greyhound';
          this.isMarketAntepost = this.isAntepostMarket();

          this.syncToApplySorting();

          // Forecast-Tricast
          this.addForecastTricastTabs(config);
          // Check for default tab should be made after forecast/tricast tabs were added
          this.checkDefaultTab(isTotepoolMarket);

          this.liveCommentary = config.LiveCommentary;
          this.isMarketDescriptionAvailable = config.RacingEDPMarketsDescription &&
           config.RacingEDPMarketsDescription.enabled;
          const $racingEDPMarkets = this.setRacingEDPMarkets();

          return observableForkJoin([observableOf(config),
            $racingEDPMarkets]);
        }),
        switchMap(([config, racingEDPMarkets]: [ISystemConfig, IRacingEdpMarket[]]) => {
          this.RACING_EDP_MARKETS = racingEDPMarkets;
          this.setMarketTabs();
          const isUkToteEnabled = config.TotePools && config.TotePools.Enable_UK_Totepools;
          const isInternationalToteEnabled = config.InternationalTotePool && config.InternationalTotePool.Enable_International_Totepools
            && config.InternationalTotePool.Enable_International_Totepools_On_RaceCard;
          // Show totepool tab only if event is UK or IRE and there are mapped pool events
          return (isUkToteEnabled && this.eventEntity.isUKorIRE) || (isInternationalToteEnabled && !this.eventEntity.isUKorIRE)
            ? observableOf(null)
            : (isTotepoolMarket ? throwError(null) : observableEmpty());
        }),
        switchMap(() => {
          this.poolEventIds = this.ukToteService.getTotePoolEventIds(this.eventEntity);
          this.toteLabel = this.localeService.getString('uktote.totepool');
          // Show totepool tab only if event is UK or IRE and there are mapped pool events
          return this.poolEventIds && this.poolEventIds.length
            ? this.ukToteService.getPoolsForEvent({ eventsIds: this.poolEventIds })
            : (isTotepoolMarket ? throwError(null) : observableEmpty());
        }),
        switchMap((pools: IPoolModel[]) => {
          if (!pools || !pools.length || !this.isAllowedPool(pools)) {
            return isTotepoolMarket ? throwError(null) : observableEmpty();
          }
          this.pools = pools;
          return observableFrom(this.horseracing.getEvent(this.poolEventIds[0]));
        }))
        .subscribe((poolEventEntities: ISportEvent[]) => {
          this.poolEventEntity = poolEventEntities[0];
          this.addTotePoolTab();

          if (isTotepoolMarket) {
            this.selectedMarket = this.getMarketByPath(this.eventEntity.sortedMarkets, UK_TOTE_CONFIG.marketPath).label;
            this.selectedMarketType = this.getTotePoolTypeByPath(UK_TOTE_CONFIG.poolTypesMap, this.selectedMarketTypePath);
          }
          this.setMarketTabs();
        }, () => this.selectFallbackMarket(this.getMarketByLabel(sortedMarkets, this.ewLabel)));

      this.shouldShowCSBIframe = this.watchRulesService.shouldShowCSBIframe(this.eventEntity, this.performConfig);

      if (this.eventEntity.racingFormEvent && this.isHR
        && this.eventEntity.racingFormEvent.distance) {
        this.eventEntity.racingFormEvent.distance = this.filterService.distance(this.eventEntity.racingFormEvent.distance);
      }

      this.filter = 'hideStream';

      this.showRibbonEventName();

      this.initializeBreadcrumbs();

      this.isNotAntepostOrSpecials = !this.isAntepostMarket() && !this.horseracing.isRacingSpecials(this.eventEntity);
      this.isRacingSpecialsCondition = this.horseracing.isRacingSpecials(this.eventEntity);
      this.hideSilk = this.isRacingSpecialsCondition && this.isGreyhoundEdp;
      this.isMediaAvailable = this.isShowMedia;

      this.setRacingSpecialsDate();

      this.checkIsForecastTricast(this.selectedMarketPath);

      this.addDeleteMarketListener();
      this.isRacingPostVerdictAvailable =  this.RacingPostVerdictAvailable();
      this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT, (updateEventId: string, delta: IDelta) => {
        if (delta.originalName === 'Win or Each Way') {
          this.delta = delta;
          this.delta.updateEventId = updateEventId;
        }
      });
      if (this.isWrapper) {
        this.nativePlayerSticky();
      }
      this.handleEvent();      
      this.cmsService.getFeatureConfig('NativeConfig').subscribe(data => {
        if (data && data.showFullScreen && data.fullScreenDrillDownTags) {
          this.isFullScreenConfig = true;
          this.fullScreenDrillDownTags = data.fullScreenDrillDownTags;
        }
        if(data && data.insightsDrillDownTags) {
          this.insightsDrillDownTags = data.insightsDrillDownTags;
        }
      });
      this.isFutureMeetingsOverlay = this.eventEntity.categoryId == '19' && !['sb.today', 'sb.tomorrow'].includes(this.eventEntity.correctedDay);
      this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.IS_WEB_VIDEO_STICKED, (containerHeight: string) => {
        this.updateFloatingMsgTop(containerHeight);
        this.isWebStreamBet = true;
      });
      this.spotlightedOutcome = this.getSpotlightedSelection();
    }
  }

  protected isWebStreamAndBet(): boolean {
    return this.isWebStreamBet && this.filter === 'showVideoStream' && this.deviceService.isWrapper;
  }

  /**
   * Setting rawIsOffCode based on pre-play and in-play events
   */
   handleEvent(): void {
    this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.EXTRA_PLACE_RACE_OFF, (updateEventId: string) => {
      if(updateEventId && this.eventEntity.id.toString() === updateEventId.toString()) {
        this.eventEntity.rawIsOffCode = 'Y';
      }
    });
  }

  childComponentLoaded() {
    this.changeDetectorRef.detectChanges();
  }

  /**
 * Returns Spotlighted selection
 * @returns IOutcome
 */
  getSpotlightedSelection(): IOutcome {
    let spotlightedSelection = null;
    if (this.eventEntity && this.eventEntity.markets) {
      this.eachWayMarket = this.eventEntity.markets.find((market) => market.name === 'Win or Each Way');
      if (!this.eachWayMarket) {
        this.eachWayMarket = this.eventEntity.markets.find((market) => market.name === 'Win Only');
      }
      if (this.racingPostVerdictData && this.racingPostVerdictData.tips && this.eachWayMarket && this.eachWayMarket
        .outcomes) {
        this.racingPostVerdictData.tips.forEach((tip) => {
          tip.outcome = this.eachWayMarket
            .outcomes.find((outcome) => tip.saddleNo === outcome.runnerNumber);
        });
        const getSpotlightTip = this.racingPostVerdictData.tips.find(tip => tip.name === 'SPOTLIGHT');
        if (getSpotlightTip) {
          spotlightedSelection = this.eachWayMarket.outcomes.find(item => item.runnerNumber == getSpotlightTip.saddleNo);
        }
      }
    }
    return spotlightedSelection;
  }

  /**
   * get BIR markets enabled and modify markets
   */
  protected getBIRMarkets(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.BIRMarketsEnabled = config?.HorseRacingBIR?.marketsEnabled;
      this.modifyMarkets(this.eventEntity, this.sportName);
    });
  }

  addDeleteMarketListener(): void {
    this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.DELETE_MARKET_FROM_CACHE, (marketId: string) => {
      const index: number = this.eventEntity.sortedMarkets.findIndex((el: IMarket) => {
        const isId: boolean = el.id === marketId;
        if (!isId && el.markets) {
          const i = el.markets.findIndex(mkt => mkt.id === marketId);
          if (i === -1) {
            return false;
          }
          el.markets.splice(i, 1);
          return !el.markets.length;
        } else {
          return isId;
        }
      });

      if (index < 0) {
        return;
      }

      this.removeTab(undefined, index);
    });
  }

  removeTab(label: string, index?: number): void {
    if (typeof label !== 'string') {
      if (!Number.isInteger(index) || index < 0) {
        return;
      }
      label = this.eventEntity.sortedMarkets[index].label;
    }

    if (!Number.isInteger(index)) {
      index = this.eventEntity.sortedMarkets.findIndex(el => el.label === label);
    }

    if (index < 0) {
      return;
    }

    this.eventEntity.sortedMarkets.splice(index, 1);
    this.marketsTabs.splice(index, 1);

    let isWinOrEWCase;
    if (label === this.winOrEWLabel) {
      this.eventEntity.sortedMarkets = this.eventEntity.sortedMarkets
        .filter((el: IMarket) => el.label !== this.tricastLabel && el.label !== this.forecastLabel);
      this.marketsTabs = this.marketsTabs
        .filter((el: ISwitcherConfig) => el.name !== this.tricastLabel && el.name !== this.forecastLabel);

      isWinOrEWCase = [this.winOrEWLabel, this.tricastLabel, this.forecastLabel]
        .some((lbl: string) => this.selectedMarket === lbl);
      if (isWinOrEWCase) {
        index = 0;
      }
    }

    if (this.selectedMarket === label || isWinOrEWCase) {
      const sortedMarketsLength: number = this.eventEntity.sortedMarkets.length;
      if (!sortedMarketsLength) {
        return;
      }
      if (index > sortedMarketsLength - 1) {
        index = sortedMarketsLength - 1;
      }
      this.change(this.eventEntity.sortedMarkets[index]);
    }
  }
  private set isShowMedia(value:boolean){}
  private get isShowMedia(): boolean {
    return !this.isAntepostMarket() && !this.isRacingSpecialsCondition && (this.eventEntity.liveStreamAvailable ||
      this.sportName !== 'greyhound' && this.eventEntity.isUKorIRE);
  }

  showRibbonEventName(): void {
    if (this.racingInMeeting.length) {
      const firstEventName: string = this.racingInMeeting[0].name;
      this.isRibbonEventName = _.some(this.racingInMeeting, event => event.name !== firstEventName);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.racingInMeeting && changes.racingInMeeting.currentValue) {
      this.showRibbonEventName();
    }
  }
  
  updateFloatingMsgTop(nativePlayerHeight: string = '0') {
    const floatingMsgPlaceholder = this.elementRef.nativeElement.querySelector('.floating-ihr-msg-sticky');
    if (floatingMsgPlaceholder) {
      floatingMsgPlaceholder.style?.removeProperty('top');
      const { top } = this.windowRef.nativeWindow.getComputedStyle(floatingMsgPlaceholder);
      const playerHeight = +nativePlayerHeight.replace('px', '');
      if (playerHeight === 0) {
        floatingMsgPlaceholder.style?.removeProperty('top');
        return;
      }
      const messageHeight = +top?.replace('px', '');
      floatingMsgPlaceholder.style.top = `${playerHeight + messageHeight}px`;
    }
  }
  ngOnDestroy(): void {
    this.routeEventsListener && this.routeEventsListener.unsubscribe();
    this.ukToteDataSubscription && this.ukToteDataSubscription.unsubscribe();
    this.secondaryMarketsSubscription && this.secondaryMarketsSubscription.unsubscribe();

    this.pubSubService.unsubscribe('RacingEventComponent');
    this.document.removeEventListener('eventAlertsEnabled', this.handleAlerts);
    this.pubSubService.unsubscribe('racingEvent');
    this.windowRef.nativeWindow.clearInterval(this.detectListener);
  }

  stopPropagation(event): void {
    event.stopPropagation();
  }

  onBellClick(): void {
    this.nativeBridgeService.onEventAlertsClick(
      this.eventId.toString(),
      this.sportName,
      this.eventEntity.categoryId,
      this.eventEntity.drilldownTagNames,
      ALERTS_GTM.EVENT_SCREEN);
      this.sendGTMMatchAlertClick();
  }

  /**
  * click match alerts - GA tracking
  */
  private sendGTMMatchAlertClick(): void {
    const gtmData = {
      'component.ActionEvent': ALERTS_GTM.CLICK,
      'component.PositionEvent': ALERTS_GTM.EVENT_SCREEN,
      'component.EventDetails': ALERTS_GTM.MATCH_ALERT_ICON,
      'component.CategoryEvent': ALERTS_GTM.SPORT_ALERT,
      'component.LabelEvent': ALERTS_GTM.MATCH_ALERT,
      'component.LocationEvent': ALERTS_GTM.EVENT_SCREEN,
      'component.URLClicked': ALERTS_GTM.NA,
      'sportID': this.eventEntity.categoryId,
    };
    this.gtmService.push(ALERTS_GTM.EVENT_TRACKING, gtmData);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {object} value
   * @return {number}
   */
  trackById(index: number, value: { id: number }): number | any {
    return value.id;
  }

  isResultedOrRaceOff(event: ISportEvent): boolean {
    return event.isResulted || !event.isResulted && event.isStarted && !event.isLiveNowEvent;
  }

  /**
   * Handles selection of new racing event by redirecting to event's page.
   */
  selectEvent(selectedTypeName: string): void {
    const activeEvents = _.filter(this.racingsMap[selectedTypeName], (value: ISportEvent) => !this.isResultedOrRaceOff(value)),
      activeEventsByTime = this.filterService.orderBy(activeEvents, ['startTime']),
      eventEntity = activeEvents.length ? activeEventsByTime[0] : this.racingsMap[selectedTypeName][0],
      url = this.routingHelperService.formEdpUrl(eventEntity);

    this.router.navigateByUrl(url);
  }

  /**
   * Show more/less summary text
   */
  summaryMoreLess(): void {
    this.showLess = !this.showLess;
    this.racingPostSummary = this.showLess
      ? `${this.eventEntity.racingFormEvent.overview.substring(0, 100)}... `
      : this.eventEntity.racingFormEvent.overview;
  }

  /**
   * Display market panel
   * @param {Object} marketEntity
   * @return {Boolean}
   */
  displayMarketPanel(marketEntity: IMarket): boolean {
    const isSelected: boolean = this.selectedMarket === marketEntity.label,
      isTopFinishSelected = this.isTopFinishSelected(marketEntity),
      isToFinishSelected = this.selectedMarket === this.localeService.getString('sb.toFinishMarkets') &&
        marketEntity.isToFinish && !marketEntity.collapseMarket,
      insuranceSelected = this.selectedMarket === this.localeService.getString('sb.insuranceMarkets') &&
        marketEntity.insuranceMarkets && !marketEntity.collapseMarket,
      isOtherSelected = this.selectedMarket === this.localeService.getString('sb.otherMarkets') &&
        marketEntity.isOther && !marketEntity.collapseMarket,
      isWOSelected = this.selectedMarket === this.localeService.getString('sb.bettingWithout') &&
        marketEntity.isWO && !marketEntity.collapseMarket;
    const isDisplayedPanel = this.isRacingSpecialsCondition || isSelected || isTopFinishSelected ||
      isToFinishSelected || insuranceSelected || isOtherSelected || isWOSelected;

    return isDisplayedPanel && !!marketEntity.outcomes && !this.isGroupedMarket() ||
      isDisplayedPanel && !!marketEntity.outcomes && this.isRacingSpecialsCondition;
  }

  /**
   * Display Market Header
   * @param marketEntity
   * @returns {string}
   */
  displayMarketHeader(marketEntity: IMarket): string {
    const isTopFinishSelected = this.selectedMarket === this.localeService.getString('sb.topFinishMarkets') && marketEntity.isTopFinish,
      isToFinishSelected = this.selectedMarket === this.localeService.getString('sb.toFinishMarkets') && marketEntity.isToFinish,
      insuranceMarkets = this.selectedMarket === this.localeService.getString('sb.insuranceMarkets') && marketEntity.insuranceMarkets,
      isOtherSelected = this.selectedMarket === this.localeService.getString('sb.otherMarkets') && marketEntity.isOther,
      isWOSelected = this.selectedMarket === this.localeService.getString('sb.bettingWithout') && marketEntity.isWO,
      isWinOrEW = this.selectedMarket === this.localeService.getString('sb.winOrEachWay')
        && marketEntity.templateMarketName === 'Win or Each Way',
      isAntepost = marketEntity.isAntepost === 'true';

    if (this.horseracing.isRacingSpecials(this.eventEntity) && !isWinOrEW) {
      return marketEntity.name;
    }

    if (isOtherSelected || isWOSelected || isTopFinishSelected || isToFinishSelected || insuranceMarkets || isAntepost) {
      return marketEntity.name;
    }
    return '';
  }

  /**
   * Change the selected tab.
   *
   * selectedMarket - selected market, defines which market tab is selected.
   *
   */
  change(marketEntity: IMarket): void {
    this.selectedMarket = marketEntity.label;
    this.selectedMarketType = null;
    this.isDescriptionAvailable = false;
    this.isToteForecastTricast = false;
    this.pubSubService.publish(this.pubSubService.API.CLOSE_SORT_BY);
    this.pubSubService.publish(this.pubSubService.API.CHANGE_MARKET, marketEntity.path);

    _.each(this.eventEntity.markets, (market: IMarket) => {
      market.collapseMarket = false;
    });
    if (!this.isRaceCard) {
      this.updateLocation(marketEntity.path);
    }
    this.checkIsForecastTricast(marketEntity.path);
    this.track(marketEntity.label);
    this.isToteForecastTricast = this.horseracing.isToteForecastTricasMarket(this.selectedMarket);
  }

  /**
   * Click on the Video Stream button.
   * Toggle Video Stream Area.
   * param {object} event object.
   */
  playStream(e: MouseEvent): void {
    e.preventDefault();
    if(this.filter !== 'showVideoStream' && this.showWatchAndInsights()) {
      if(this.eventEntity.rawIsOffCode !== 'Y') {
        this.setGtmData('watch & insights'); 
      } else {
        this.setGtmData('watch');
      }
    }
    if (!this.isVideoHandled) {
      this.handleNativeVideoPlayer();
      this.isVideoHandled = true;
    }
    this.filter = this.filter === 'showVideoStream' ? 'hideStream' : 'showVideoStream';
    this.preloadStream = true;
    this.streamControl.playLiveSim(false);

    this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED, () => {
      this.filter = 'hideStream';
    });

    if (this.filter === 'hideStream' && this.isWrapper) {
      this.nativeBridgeService.hideVideoStream();
      this.pubSubService.publish(this.pubSubService.API.IS_NATIVE_VIDEO_STICKED, false);
    }
  }

  /**
   * Click on the Live Simulation button.
   * Toggle Live Simulation Area.
   * param {object} event object.
   *
   */
  playLiveSim(e: MouseEvent): void {
    const event = this.eventEntity,
      isDuplication = this.streamTrackingService.checkIdForDuplicates(event.id, 'preSim'),
      now = this.timeService.getCurrentTime();
    e.preventDefault();
    this.filter = this.filter === 'showLiveSim' ? 'hideStream' : 'showLiveSim';

    // track pre sim to GTM
    if (this.filter === 'showLiveSim' && event.isActive && !isDuplication) {
      // stop tracking pre sim 5 min before event will start
      const timeDiff = Number(event.startTime) - now;

      if (timeDiff <= this.presimStopTrackInterval) {
        return;
      }

      this.gtmService.push('trackEvent', {
        eventCategory: 'streaming',
        eventAction: 'click',
        eventLabel: 'watch pre sim',
        sportID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      });
      this.streamTrackingService.addIdToTrackedList(event.id, 'preSim');
    }

    this.streamControl.hideStream();
    this.streamControl.playLiveSim(this.filter === 'showLiveSim');
  }

  /**
   * Google analytics. Track uk tote main tab
   */
  track(label: string): void {
    const toteType = this.eventEntity.isUKorIRE ? 'uk tote' : 'international tote';
    const toteTabName = this.localeService.getString('uktote.totepool');
    if (label === toteTabName) {
      this.gtmService.push('trackEvent', {
        eventCategory: toteType,
        eventAction: 'entry',
        eventLabel: 'main tab'
      });
    }
  }

  /**
   * Checks if at least one event of group has inplay signpost available
   * @param {ISportEvent[]} races
   * @returns {boolean}
   */
  private isBIRSignpostAvailable(event: ISportEvent): boolean {
    return this.isHR && event.drilldownTagNames?.split(',').includes(DRILLDOWNTAGNAMES.HR_BIR);
  }

  /**
   * Checks if market is enabled in CMS for BIR
   * @param {string} marketName
   * @returns {boolean}
   */
  private isBirMarketEnabled(marketName: string = ''): boolean {
    return this.BIRMarketsEnabled?.some((market: string) => marketName.toLocaleLowerCase() === market.toLocaleLowerCase());
  }

  /**
   * @description
   * remove ',' in the and of weight value
   * Ex: Pounds,132, => Pounds,132
   * @return {undefined}
   */
  modifyMarkets(event: ISportEvent, sportName: string): void {
    const isBIRSignPostAvailable = this.isBIRSignpostAvailable(event);
    _.each(event.markets, (marketEntity: IMarket) => {
      _.each(marketEntity.outcomes, (outcomeEntity: IOutcome) => {
        this.termsBeforeMarketAvailable[marketEntity.id] = (isBIRSignPostAvailable && this.isBirMarketEnabled(marketEntity.name)) || marketEntity.isEachWayAvailable || marketEntity.isGpAvailable
          || marketEntity.drilldownTagNames || marketEntity.cashoutAvail === 'Y' || marketEntity.viewType === 'handicaps' || event.uiClass;

        if (outcomeEntity.racingFormOutcome && outcomeEntity.racingFormOutcome.weight) {
          // eslint-disable-next-line no-useless-escape
          outcomeEntity.racingFormOutcome.weight = outcomeEntity.racingFormOutcome.weight.replace(/\,$/, '');
        }
        outcomeEntity.isValidRunnerNumber = this.isValidRunnerNumber(outcomeEntity.runnerNumber);
        if (outcomeEntity.isValidRunnerNumber && sportName === 'greyhound') {
          event.silksAvailable = true;
        }
      });
    });
  }

  /**
   * Check for market with antepost flag
   * @returns {boolean}
   */
  isAntepostMarket(): boolean {
    return this.eventEntity &&
      this.eventEntity.markets &&
      this.eventEntity.markets[0] &&
      this.eventEntity.markets[0].isAntepost === 'true';
  }

  /**
   * Forms event details page or sport results page based on event's "isResulted" property.
   * @param {Object} eventEntity
   * @return {string}
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formResultedEdpUrl(eventEntity, this.isNextRaceEvent() ? `?origin=${this.origin}` : '');
  }

  /**
   * Redirect user to page
   * @param eventEntity
   */
  goToEdpUrl(eventEntity: ISportEvent | Event | any): void {
    this.router.navigateByUrl(this.formEdpUrl(eventEntity));
  }

  goToSeo(eventEntity: ISportEvent): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(eventEntity);
    this.seoDataService.eventPageSeo(eventEntity, edpUrl);
  }

  /**
   * @param {object} event
   */
  isLpAvailable(event: ISportEvent): boolean {
    return this.lpAvailabilityService.check(event);
  }

  /**
   * Set outcome isFavourite property
   * @param outcomeEntity
   */
  setOutcomeFavourite(outcomeEntity: IOutcome): void {
    outcomeEntity.isFavourite = +outcomeEntity.outcomeMeaningMinorCode > 0 ||
      outcomeEntity.name.toLowerCase() === 'unnamed favourite' ||
      outcomeEntity.name.toLowerCase() === 'unnamed 2nd favourite';
  }

  // Function for open/close dropdown
  showMeetingsList(): void {
    this.showMeetings = !this.showMeetings;
    this.windowRef.nativeWindow.scrollTo(0, 0);
    if (this.showMeetings) {
      this.gtmService.push('trackEvent', {
        eventCategory: this.sportName === 'horseracing' ? 'horse racing' : 'greyhounds',
        eventAction: 'meetings',
        eventLabel: 'open'
      });
    }
  }

  /**
   * Find if market is grouped
   * @params {object} market
   * @return {object}
   */
  isGroupedRaceMarket(market: IMarket): string {
    return _.find(this.config.GROUPED_MARKETS_NAME, (marketName: string) => marketName === market.name);
  }

  /**
   * Get event stage
   * @returns {*|string}
   */
  get going(): string {
    const KEY_NOT_FOUND = 'KEY_NOT_FOUND';
    let stage = this.localeService.getString(`racing.racingFormEventGoing.${this.eventEntity.racingFormEvent.going}`);

    if (stage === KEY_NOT_FOUND) {
      stage = '';
    }

    return stage;
  }
  set going(value:string){}

  /**
   * Get race type
   * @returns {*|string}
   */
  get raceType(): string {
    const KEY_NOT_FOUND = 'KEY_NOT_FOUND';
    let stage = this.localeService.getString(`racing.raceType.${this.eventEntity.racingFormEvent.raceType}`);

    if (stage === KEY_NOT_FOUND) {
      stage = '';
    }
    return stage;
  }
  set raceType(value:string){}

  isGroupedMarket(): boolean {
    return (this.selectedMarket === 'To Finish') || (this.selectedMarket === 'Top Finish') || (this.selectedMarket === 'Place Insurance');
  }

  formatAntepostTerms(str: string): string {
    const newStr = str
      .replace(/(odds)/ig, 'Odds')
      .replace(/(places)/ig, 'Places')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `<strong>${match}</strong>`;
      });

    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `<strong>${match}</strong>`);
  }

  showTab(racing: ISportEvent, event: ISportEvent): boolean {
    if (event && event.drilldownTagNames && event.drilldownTagNames.split(',').indexOf('EVFLAG_AP') > -1) {
      return racing && racing.drilldownTagNames && racing.drilldownTagNames.split(',').indexOf('EVFLAG_AP') > -1;
    }
    return true;
  }

  onPlayLiveStreamError($event: { value: string}): void {
    if (this.isWrapper && !this.watchRulesService.isInactiveUser($event.value)) {
      this.filter = 'hideStream';
    }
  }

  /**
   * Sort markets by selected option.
   * @param {string} option 'price'/'racecard'
   */
  applySortBy(option: string): void {
    const noRunnerNumbers = this.eventEntity.markets.every(
      (market: IMarket) =>  market.outcomes.every((outcome: IOutcome) => !Number(outcome.runnerNumber) )
    );

    const byPrice = option.toLowerCase() === 'price' || noRunnerNumbers;
    this.sortBy = option;
    this.eventEntity.markets.forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFilters.orderOutcomeEntities(market.outcomes,
        market.isLpAvailable && byPrice, true, true, false, false,
        !this.isHR && !this.eventEntity.isResulted);
      this.setMarketsInfo(market, mindex);
    });
  }

  /**
   * Set correct date format.
   * @param {string} date
   * @return {string}
   */
  filterDate(date: string, withYear?: boolean): string {
    let filtered = this.timeService.formatByPattern(date, 'd', null, true);
    const daySuffix = this.tools.getDaySuffix(filtered.replace(/[^0-9]/g, ''));

    filtered = `${this.timeService.formatByPattern(date, 'EEEE', null, true)} ${filtered + daySuffix} ${
      this.timeService.formatByPattern(date, 'MMMM', null, true)}`;
    if (withYear) {
      filtered += ` ${new Date(date).getFullYear()}`;
    }
    return filtered;
  }

  /**
   * Check if sort options are shown
   * @param {boolean} isEW
   * @param {boolean} checkMarket
   * @param {object} market
   * @return {boolean}
   */
  sortOptionsEnabledFn(isEW: boolean, checkMarket?: boolean, market?: IMarket): boolean {
    const checks = isEW && this.sortOptionsEnabled && this.selectedMarket !== this.toteLabel;
    const selectedMarket = this.selectedMarket &&
      _.find(this.eventEntity.sortedMarkets, sortedMarket => sortedMarket.name === this.selectedMarket);

    if (!market && selectedMarket && checkMarket) {
      if (selectedMarket.markets) {
        market = selectedMarket.markets[0];
      } else if (selectedMarket.outcomes) {
        market = selectedMarket;
      }
    }
    const isLP = market && market.isLpAvailable;

    return checks && (!market || isLP && _.some(market.outcomes, (o: IOutcome) => o.prices && o.prices.length > 0));
  }

  updateLocation(marketPath: string | null, replace: boolean = false): void {
    const edpUrl = this.routingHelperService.formEdpUrl(this.eventEntity),
      subPath = marketPath ? `/${marketPath}` : '',
      fullUrl = `${edpUrl}${subPath}`;
    const origin = this.route.snapshot.queryParams.origin;
    const queryParamOrigin = origin ? `origin=${origin}` : '';

    replace ? this.location.replaceState(fullUrl, queryParamOrigin) : this.location.go(fullUrl, queryParamOrigin);
  }

  /**
   * Handle child Spectial component data loaded
   */
  handleSpecialsLoaded(): void {
    this.specialsLoaded = true;
  }
  /**
   * toggle Racing Post Verdict
   */
  toggleRacingPostVerdict(): void {
    this.showVerdict = !this.showVerdict;
    this.spotlightedOutcome = this.getSpotlightedSelection();

    this.gtmService.push('trackEvent', {
      eventCategory: 'horse racing',
      eventAction: 'race card',
      eventLabel: 'racing post verdict'
    });
  }

  /**
   * Click on Horse Block.
   *
   * Toggle Horse Information Area.
   *
   * param {array} summary of expanded and collapsed areas.
   * param {number} market index.
   * param {number} outcome index.
   *
   */
  onExpandSection(expandedSummary: Array<Array<boolean>>, mIndex: number, oIndex: number): void {
    expandedSummary[mIndex][oIndex] = !expandedSummary[mIndex][oIndex];
    const hideInfoChecker: boolean = expandedSummary[mIndex].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info':!hideInfoChecker };
    const gtmData = {
      event: "trackEvent",
      eventAction: "race card",
      eventCategory: this.isGreyhoundEdp?'greyhounds':'horse racing',
      eventLabel: expandedSummary[mIndex][oIndex] ? 'show more':'show less',
      categoryID:this.eventEntity.categoryId,
      typeID:this.eventEntity.typeId,
      eventID:  this.eventEntity.id
    }
    this.gtmService.push(gtmData.event,gtmData);
  }

  toggleShowOptions(expandedSummary: Array<Array<boolean>>, mIndex: number, showOption: boolean): void {
    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex][i] = showOption;
    }
  }

  protected selectFallbackMarket(marketToSelect: IMarket): void {
    this.selectedMarket = marketToSelect.label;
    this.selectedMarketPath = marketToSelect.path;
    this.selectedMarketTypePath = null;
    this.setMarketTabs();
    if (!this.isRaceCard) {
      this.updateLocation(this.selectedMarketPath, true);
    }
  }

  /**
   * Applying sorting in cases:
   * - sort switcher change
   * - new selection was added
   * - init
   */
  protected syncToApplySorting(): void {
    if (this.sortOptionsEnabled) {
      this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.SORT_BY_OPTION, (option: string) => {
        this.applySortBy(option);
        this.racingGaService.updateGATracking(this.eventEntity, option, this.isGreyhoundEdp);
      });
    }

    this.pubSubService.subscribe('racingEvent', this.pubSubService.API.LIVE_MARKET_FOR_EDP, (market: IMarket) => {
      this.applySortBy(this.sortBy);
    });

    const sortByName = this.eventEntity.markets.every((market: IMarket) => {
      const runners = market.outcomes.filter(item => item.name.search(/N\/R$/) === -1 && !item.name.includes('Unnamed'));

      return runners.some((outcome: IOutcome) => !Number(outcome.runnerNumber) && !outcome.prices.length);
    });

    if (sortByName && this.sortBy !== 'Price') {
      this.applySortByName();
    } else {
      this.applySortBy(this.sortBy);
    }
  }

  /**
   * Check if set of pools consist at least one allowed pool type
   */
  protected isAllowedPool(pools: IPoolModel[]): boolean {
    return pools.some((pool: IPoolModel) => {
      return pool && UK_TOTE_CONFIG.allowedPools.indexOf(pool.type) >= 0;
    });
  }

  protected getMarketByPath<T extends { path?: string }>(marketsList: T[], marketPath: string): T | null {
    return marketsList.reduce((selectedMarket: T, market: T): T | null =>
      selectedMarket || (market.path === marketPath ? market : selectedMarket), null);
  }

  protected getMarketByLabel<T extends { label?: string }>(marketsList: T[], defaultLabel: string): T {
    return marketsList.reduce((defaultMarket: T, market: T): T =>
      market.label === defaultLabel ? market : defaultMarket);
  }

  protected getTotePoolTypeByPath(poolTypesMap: { [key: string]: { name: string; path: string } }, poolTypePath: string): string {
    const poolTypes = Object.keys(poolTypesMap).map(type => ({ type, path: poolTypesMap[type].path }));
    // Tote pooltype switch should be retrieved from URL subpath, if provided
    const poolTypeByPath = poolTypePath && this.getMarketByPath(poolTypes, poolTypePath);
    // If pooltype URL subpath is not provided, or is not a valid/existing one, then first pooltype switcher is selected
    return poolTypeByPath && this.pools.some(pool => pool.type === poolTypeByPath.type)
      && UK_TOTE_CONFIG.displayOrder.some(poolType => poolType === poolTypeByPath.type) ? poolTypeByPath.type : null;
  }

  protected setMarketTabs(): void {
    this.marketsTabs = [];
    this.hasSortedMarketsFromCms = false;
    this.marketContainer = this.elementRef.nativeElement.querySelector(this.MARKETS_CONTAINER);
    if (this.isMarketDescriptionAvailable) {
      this.eventEntity.sortedMarkets = this.horseracing.getSortingFromCms(this.eventEntity.sortedMarkets,
        this.RACING_EDP_MARKETS, this.isGreyhoundEdp);
      if (!this.hasMarketType) {
        this.selectedMarket = this.eventEntity.sortedMarkets[0].label;
        this.selectedMarketPath = this.eventEntity.sortedMarkets[0].path;
        if (!this.isRaceCard) {
          this.updateLocation(this.selectedMarketPath, true);
        }
      }
      this.hasSortedMarketsFromCms = true;
      this.isToteForecastTricast = this.horseracing.isToteForecastTricasMarket(this.selectedMarket);
    }
    this.eventEntity.sortedMarkets.forEach((market: IMarket) => {
      this.marketsTabs.push({
        onClick: () => this.change(market),
        name: market.label,
        viewByFilters: market.label
      });
    });
  }

  protected addForecastTricastTabs(config: ISystemConfig): void {
    const sortedMarkets = this.eventEntity.sortedMarkets;
    const winOrEWMarket = Object.assign({},
      this.eventEntity.markets.find(market => market.templateMarketName === 'Win or Each Way'));

    if (config.forecastTricastRacing && config.forecastTricastRacing.enabled === true
      && winOrEWMarket.ncastTypeCodes && sortedMarkets.length > 0) {

      const isForecastAvailable = winOrEWMarket.ncastTypeCodes.indexOf('CF') >= 0;
      const isTricastAvailable = winOrEWMarket.ncastTypeCodes.indexOf('CT') >= 0;
      this.forecastTricastMarket = winOrEWMarket;
      this.forecastTricastMarket.outcomes = this.forecastTricastMarket.outcomes
        .filter((outcome: IOutcome) => !outcome.isFavourite && !outcome.nonRunner)
        .sort((firstOutcome: IOutcome, secondOutcome: IOutcome) => firstOutcome.displayOrder - secondOutcome.displayOrder);

      if (isTricastAvailable && this.forecastTricastMarket.outcomes.length >= 3) {
        const tricastTab = {
          label: this.tricastLabel,
          path: 'tricast'
        };
        // @ts-ignore
        sortedMarkets.splice(1, 0, tricastTab);
        if (this.selectedMarketPath === FORECAST_CONFIG.tricastMarketPath) {
          this.selectedMarket = this.tricastLabel;
        }
      }
      if (isForecastAvailable && this.forecastTricastMarket.outcomes.length >= 2) {
        const forecastTab = {
          label: this.forecastLabel,
          path: 'forecast'
        };
        // @ts-ignore
        sortedMarkets.splice(1, 0, forecastTab);
        if (this.selectedMarketPath === FORECAST_CONFIG.forecastMarketPath) {
          this.selectedMarket = this.forecastLabel;
        }
      }
    }
  }

  protected addTotePoolTab(): void {
    const sortedMarkets = this.eventEntity.sortedMarkets,
      poolTab = {
        label: this.toteLabel,
        path: UK_TOTE_CONFIG.marketPath
      };

    if (sortedMarkets.find((market: IMarket) => market.label === this.toteLabel)) {
      return;
    }

    if (sortedMarkets.length > 0) {
      // @ts-ignore
      sortedMarkets.push(poolTab);
    }
  }

  protected checkDefaultTab(isTotepoolMarket: boolean): void {
    this.selectedMarket = this.eventEntity.sortedMarkets
      .find((market: IMarket) => market.label === this.label) ? this.label : this.eventEntity.sortedMarkets[0].label;

    // Totepool tab should be activated only after Tote data is initialized
    const marketByPath = !isTotepoolMarket && this.selectedMarketPath && this.getMarketByPath(this.eventEntity.sortedMarkets,
      this.selectedMarketPath);

    // If not specified explicitly, either the Win or E/W tab, or the first tab in the list is activated by default
    const marketToSelect = !isTotepoolMarket && marketByPath || this.getMarketByLabel(this.eventEntity.sortedMarkets,
      this.ewLabel);

    // For non-Totepool markets set the selectedMarket property and adjust location for wrong or incomplete URLs
    if (!isTotepoolMarket) {
      this.selectFallbackMarket(marketToSelect);
    }
  }

  /**
   * Sets market tooltip based on configuration
   */
  protected setMarketsTooltip(): void {
    this.secondaryMarketsSubscription = this.cmsService.getFeatureConfig(this.SECONDARY_MARKETS).subscribe(
      (config: ISystemConfig) => {
        if (config && config.enabled) {
          this.secondaryMarketsTooltip = config.title;
          this.secondaryMarketsTooltip = this.secondaryMarketsTooltip.length > 100 ?
          `${this.secondaryMarketsTooltip.substring(0, 100)}...` : this.secondaryMarketsTooltip;
          this.toolTipArgs = {
            moreMarketTooltip: this.secondaryMarketsTooltip
          };
        }
      });
    }

  /*
   * Fetch Racing EDP Markets from CMS
   */
  protected setRacingEDPMarkets(): Observable<IRacingEdpMarket[]> {
    this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.HAS_MARKET_DESCRIPTION, (state: boolean) => {
      this.isDescriptionAvailable = state;
    });
    return this.isMarketDescriptionAvailable ?
          this.cmsService.getRacingEDPMarkets() : observableOf([]);
  }

  /**
   * Sort outcomes in market by name
   */
  private applySortByName(): void {
    this.eventEntity.markets.forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFilters.orderOutcomesByName(market.outcomes);
      this.setMarketsInfo(market, mindex);
    });
  }

  private setMarketsInfo(market: IMarket, mindex: number): void {
    this.expandedSummary[mindex] = [];
    market.outcomes.forEach((outcome: IOutcome) => {
      this.setOutcomeFavourite(outcome);
      if (!outcome.isFavourite && !outcome.nonRunner) {
        this.expandedSummary[mindex].push(false);
      }
    });
  }

  /**
   * As we have only 8 images for runners and backend may return
   * the runner number more than 8, we should check range of this number.
   * @param  {[String|Number]}  value Racer number
   * @return {Boolean}
   */
  private isValidRunnerNumber(value: string | number): boolean {
    return Number(value) >= 1 && Number(value) <= 8;
  }

  private handleAlerts(data: IConstant): void {
    this.bellActive = data.detail.isEnabled;
  }

  /**
   * Is notifications allowed by cms
   */
  private checkAlerts(): void {
    const sportConfigsDictionary = {
      horseracing: 'visibleNotificationIconsHorseracing',
      greyhound: 'visibleNotificationIconsGreyhounds',
    };

    const currentConfig = sportConfigsDictionary[this.sportName];

    if (this.nativeBridgeService.hasOnEventAlertsClick()) {
      this.cmsService.getFeatureConfig('NativeConfig').subscribe(data => {
        if (data && data[currentConfig]) {
          const { multiselectValue = '', value = '' } = data[currentConfig] || {};
          const isOSPermitted = _.contains(multiselectValue, this.nativeBridgeService.getMobileOperatingSystem());
          const allowedLeaguesList = _.isString(value) ? value.split(/\s*,\s*/) : [];

          this.alertsVisible = isOSPermitted && _.contains(allowedLeaguesList, this.eventEntity.typeName);
        }
      });
    } else {
      this.alertsVisible = false;
    }
  }

  private initializeBreadcrumbs(): void {
    const targetUri = this.sportName === 'horseracing' ? '/horse-racing/featured' : '/greyhound-racing/today';
    this.breadcrumbsItems = [{
      name: this.localeService.getString(`sb.${this.sportName}`),
      targetUri
    }, {
      name: this.isNextRaceEvent() ? this.isOriginOffersnFeatured() :
        this.eventEntity && this.eventEntity.typeName,
    }];
    const headerData: IRacingHeader = {
      breadCrumbs: this.breadcrumbsItems,
      eventEntity: this.eventEntity,
      meetingsTitle: this.meetingsTitle,
      quickNavigationItems: this.quickNavigationItems,
      sportEventsData: this.sportEventsData,
      isMarketAntepost: this.isMarketAntepost
    };
    this.pubSubService.publish('TOP_BAR_DATA', headerData);
  }

  private isOriginOffersnFeatured() {
   return this.origin.includes('offer') ? 'Offers and Featured' : this.localeService.getString(`racing.${this.origin}`);
  }

  private isNextRaceEvent(): boolean {
    return (this.origin && this.eventEntity.isStarted === undefined);
  }

  private checkIsForecastTricast(marketPath: string): void {
    this.isForecastTricast = ['tricast', 'forecast'].includes(marketPath);
  }

  private isTopFinishSelected(marketEntity: IMarket): boolean {
    return this.selectedMarket === this.localeService.getString('sb.topFinishMarkets') &&
      marketEntity.isTopFinish && !marketEntity.collapseMarket;
  }

  private setRacingSpecialsDate(): void {
    if (this.horseracing.isRacingSpecials(this.eventEntity) || this.isAntepostMarket()) {
      this.racingSpecialsDate = this.filterDate(this.eventEntity.startTime, true);
    }
  }

  private handleNativeVideoPlayer(): void {
    if (this.nativeBridgeService.isWrapper) {
      const placeholder = this.nativeVideoPlayerPlaceholderRef && this.nativeVideoPlayerPlaceholderRef.nativeElement;
      this.windowRef.nativeWindow.requestAnimationFrame(() => this.nativeBridgeService.handleNativeVideoPlayer(placeholder));
    }
  }
  /**
   * Subscriber to check if video sticked to top in EDP
   * Removes/adds the streaming section based on state value from IS_NATIVE_VIDEO_STICKED
   */
  private nativePlayerSticky(): void {
    const placeholder = this.nativeVideoPlayerPlaceholderRef && this.nativeVideoPlayerPlaceholderRef.nativeElement;
    this.pubSubService.subscribe('RacingEventComponent', this.pubSubService.API.IS_NATIVE_VIDEO_STICKED, (state: boolean) => {
      if(state) {
        this.filter = 'showVideoStream';
      }
      this.showFullscreen = state;
      this.nativeBridgeService.handleNativeVideoPlaceholder(state, placeholder);
      this.updateFloatingMsgTop(placeholder?.style?.height);
      this.pubSubService.publish(this.pubSubService.API.PIN_TOP_BAR, state);
    });
  }
  /**
   * process the updates from racing mybets
   * @param {any} event 
   */
  private handleRacingMybetsUpdates(event: ILazyComponentOutput): void {
    if(event.output === 'tabUpdated') {
      this.activeUserTab = event.value;
    }
  }

  /*
   * Checks if isSp or not
   * @param {ISportEvent} eventEntity
   * @returns {boolean}
   */
  private isSp(eventEntity: ISportEvent): boolean {
    return eventEntity.markets.map(
      (market) => market.priceTypeCodes).every(
        (el) => el.includes('SP') && !el.includes('LP'));
  }
  /**
   * checks if RacingPostVerdictAvailable or not
   * @returns {boolean}
   */
  private RacingPostVerdictAvailable(): boolean {
    return (this.eventEntity && this.eventEntity.categoryId === environment.HORSE_RACING_CATEGORY_ID &&
      this.racingPostVerdictData && this.racingPostVerdictData.isFilled);
  }


/**
  * Updates GTMservice with greyhound data
  * @param showOption:  option
  */
 public toggleShowOptionsGATracking(showOption: boolean): void {
  this.racingGaService.toggleShowOptionsGATracking(this.eventEntity, showOption, this.isGreyhoundEdp);
}


  /**
    * Show Watch & Insights button for RMG streams
  */
  public showWatchAndInsights(): boolean {
    const tagList = this.insightsDrillDownTags.find((tag: string)=>(this.eventEntity && this.eventEntity.drilldownTagNames && this.eventEntity.drilldownTagNames.includes(tag)));
    if(tagList) {
      return this.eventEntity.isUKorIRE && this.eventEntity.categoryId === environment.HORSE_RACING_CATEGORY_ID;
    }
    return false;
  }

  /**
    * Show full screen option for RMG streams
  */
  showFullScreen(): boolean { 
    const tagList = this.fullScreenDrillDownTags.find((tag: string)=>(this.eventEntity && this.eventEntity.drilldownTagNames && this.eventEntity.drilldownTagNames.includes(tag)));    
    return tagList
        && this.eventEntity.isUKorIRE 
        && this.eventEntity.categoryId === environment.HORSE_RACING_CATEGORY_ID
        && this.eventEntity.rawIsOffCode === 'Y' 
        && this.showFullscreen 
        && this.isWrapper
        && typeof this.windowRef.nativeWindow.NativeBridge?.displayInLandscapeMode === 'function'
        && this.isFullScreenConfig;
  }

  /**
    * Full screen available to turn video to Landscape mode
  */
   watchInFullScreen(): void {
    this.nativeBridgeService.displayInLandscapeMode();
    this.setGtmData('full video mode');
  }

  /**
   * set GA tracking object
   * @param gtmEventLabel string value
   */
   setGtmData(gaEventDetails: string): void {    
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'horse racing',
      'component.LabelEvent': 'event details page',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': this.eventEntity.typeName,
      'component.EventDetails': gaEventDetails,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

    /**
   * displays the BOG signposting if Gp start time is greaterthan or equal to current time
   * @param isBOGAvailable ISportEvent value
   */
    isBOGAvailable(raceData: ISportEvent, isGpAvailable: boolean): boolean{
      return  !!raceData.effectiveGpStartTime && new Date().getTime() >= new Date(raceData.effectiveGpStartTime).getTime() && !!isGpAvailable;
    }  
  
}
