import { EMPTY, forkJoin, from, Observable, of as observableOf, Subscription } from 'rxjs';
import { catchError, defaultIfEmpty, finalize, map, mergeMap, switchMap, concatMap, delay, filter } from 'rxjs/operators';
import {
  ChangeDetectorRef, OnDestroy, OnInit, AfterViewInit,
  Component, ComponentRef, ElementRef, ViewChildren, QueryList, Input, OnChanges, SimpleChanges, Output, EventEmitter
} from '@angular/core';

import * as _ from 'underscore';
import { DeviceService } from '@core/services/device/device.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { VisDataHandlerService } from '@core/services/visDataHandler/vis-data-handler.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { ActivatedRoute } from '@angular/router';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IMarketCollection } from '@core/models/market-collection.model';
import { IEdpMarket, ISportCategory, ISystemConfig, ISportInstance } from '@core/services/cms/models';
import { IScoreboardConfig } from '@core/models/scoreboard-config.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { SportEventPageProviderService } from '@app/edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@app/edp/components/sportEventMain/sport-event-main-provider.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import IConfig from '@app/edp/models/config';
import { IEventData, ISportEvent, ISportByMapping } from '@core/models/sport-event.model';
import { IConstant } from '@core/services/models/constant.model';
import { TimeService } from '@app/core/services/time/time.service';
import { RegularBetBase } from '@app/betHistory/betModels/regularBetBase/regular-bet-base.class';
import { IScoreType } from '@core/services/scoreParser/models/score-data.model';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { SCOREBOARDS_LOAD_ORDER } from '@edp/components/sportEventMain/sport-event-main.constant';
import { ICashoutMapItem } from '@app/betHistory/models/cashout-map-item.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';
import { IBetDetail } from '@bpp/services/bppProviders/bpp-providers.model';
import { IAutoSeoData } from '@app/core/services/cms/models/seo/seo-page.model';
import { MYBETS_AREAS, ALERTS_GTM } from '@app/betHistory/constants/bet-leg-item.constant';
import { IMarket } from '@app/core/models/market.model';
import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import environment from '@environment/oxygenEnvConfig';
import { StorageService } from '@app/core/services/storage/storage.service';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { IStreamBetWeb } from '@core/services/cms/models/system-config';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { SportEventHelperService } from '@app/core/services/sportEventHelper/sport-event-helper.service';

@Component({
  selector: 'sport-event-main',
  templateUrl: './sport-event-main.component.html'
})
export class SportEventMainComponent extends AbstractOutletComponent implements OnInit, AfterViewInit, OnDestroy, OnChanges {
  @ViewChildren('nativeVideoPlayerPlaceholder') nativeVideoPlayerPlaceholderRef: QueryList<ElementRef>;

  @Input() isQuickSwitchPanelActive: boolean = false;
  @Output() quickSwitchHandler: EventEmitter<boolean> = new EventEmitter();
  @Output() typeId: EventEmitter<string> = new EventEmitter();
  public sport: ISportInstance;
  public streamShown: boolean = false;
  public activeUserTab: string;
  public scoreboardUrl: string;
  public myBetsCounter: number;
  public sportName: string = '';
  public eventId: string = '';
  public eventEntity: ISportEvent;
  public isEnhanceMultiples: boolean = false;
  public isOutRight: boolean = false;
  public isSpecialEvent: boolean = false;
  public isScoreboardVis: boolean = true;
  public showMatchLive: boolean = true;
  public showScoreboard: boolean = false;
  public optaScoreboardAvailable: boolean = false;
  public isOptaProviderPresent: boolean = false;
  public isScoreLoaded: boolean;
  public cssClass: string;
  public myBets: string;
  public myBetsAvailable: boolean;
  public gpScoreboardAvailable: boolean;
  public showSignPosting: boolean;
  public isQuickSwitchEnabled: boolean;
  public bgScoreboardConfig: IConfig = {
    available: false
  };
  public brScoreboardConfig: IConfig = {
    available: false
  };
  public eventsWithVisualizationParams: Array<any> = [];
  public sportsConfig: IConstant;
  public preMatchWidgetAvailable: boolean;
  public marketsByCollection: IMarketCollection[];
  public eventTabs: IMarketCollection[];
  public EDP_MARKETS: IEdpMarket[];
  public sysConfig: ISystemConfig = {};
  public cashoutBets: RegularBetBase[];
  public placedBets: RegularBetBase[];
  public tempBets = [];
  public DS_GAME: any;
  public cashoutIds: ICashoutMapItem[];
  public isLoggedIn: boolean;
  public marketName: string;
  public eventStartDate: string;
  public footballAlertsVisible: boolean = false;
  public footballBellActive: boolean = false;
  public favouritesVisible: boolean = undefined;
  public showNewUserTabs: boolean;
  public fallbackScoreboardType: IScoreType;
  public isFallbackScoreboards: boolean;
  public isEnhancedMultiplesEnabled: boolean = false;
  public betRadarMatchId: number;
  public imgEventDetails: string;
  public imgFrontRowArena: IConfig = {
    available: false
  };
  private combineEventIds: number[] = [];
  public dataDisclaimer = {enabled: false, dataDisclaimer: ''};
  protected eventStartDatePattern: string = 'EEEE, d-MMM-yy. HH:mm';
  protected scoreboardsLoadOrder = SCOREBOARDS_LOAD_ORDER;
  protected eventData: IEventData;
  protected catId: string;
  protected scoreSports: string[] = ['BADMINTON'];
  protected myTabsSport = [16,34,21,18,6,1,10,9,30,31,24];
  private scoreboardsLoaders: { [key: string]: (config: IScoreboardConfig) => Observable<IScoreboardConfig | never> } = {
    PM: config => this.preMatchLoader(config),
    OPTA: config => this.optaLoader(config),
    IMG: config => this.imgLoader(config),
    IMG_ARENA: config => this.imgArenaLoader(config),
    FS: config => this.fallbackScoreboardLoader(config),
    BG: config => this.betGeniusLoader(config),
    BR: config => this.betRadarLoader(config),
    GP: config => this.grandParadeLoader(config)
  };

  private nativeVideoPlayerPlaceholder: HTMLElement;
  private myBetsRef: ComponentRef<any>;
  private messageListener: any;
  private isIMGScoreboardAvailable: boolean = false;
  private isOptaScoreboardChecked: boolean = false;
  private betsStreamOpened: boolean = false;
  public isFootball: boolean;
  public isMobileOnly: boolean = false;
  private eventVideoStreamSubscriber: Subscription;
  private initDataSubscription: Subscription;
  private cashoutDataSubscription: Subscription;
  private editMyAccaUnsavedOnEdp: boolean;
  private readonly tagName: string = 'sportEventMain';
  private autoSeoData: IAutoSeoData = {};
  readonly MYBETS_EDP: MYBETS_AREAS = MYBETS_AREAS.EDP
  isStreambetAvailable: boolean;
  private streamBetCmsConfig: IStreamBetWeb;
  public changeMatch: boolean = false;
  private quickSwitchEnabledSports = ['football'];
  constructor(
    public deviceService: DeviceService,
    private activatedRoute: ActivatedRoute,
    private visEventService: VisEventService,
    private visDataHandler: VisDataHandlerService,
    private pubSubService: PubSubService,
    protected cmsService: CmsService,
    private gtmService: GtmService,
    private localeService: LocaleService,
    protected commandService: CommandService,
    private nativeBridgeService: NativeBridgeService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,
    private coreTools: CoreToolsService,
    private userService: UserService,
    private windowRef: WindowRefService,
    private sportEventPageProviderService: SportEventPageProviderService,
    private sportEventMainProviderService: SportEventMainProviderService,
    private rendererService: RendererService,
    private timeService: TimeService,
    private changeDetectorRef: ChangeDetectorRef,
    private scoreParserService: ScoreParserService,
    private sportsConfigService: SportsConfigService,
    // eslint-disable-next-line
    private updateEventService: UpdateEventService, // for events subscription (done in service init)
    private cashOutMapService: CashOutMapService,
    public cashoutWsConnectorService: CashoutWsConnectorService,
    public storageService: StorageService,
    public sportEventHelperService: SportEventHelperService
  ) {
    super()/* istanbul ignore next */;
    this.isLoggedIn = this.userService.status;
    this.setStreamShowFlag = this.setStreamShowFlag.bind(this);
    // Binded function handleFootballAlerts
    this.handleFootballAlerts = this.handleFootballAlerts.bind(this);
    this.isMobileOnly = this.deviceService.isMobileOnly;
  }

  ngAfterViewInit(): void {
    if (this.nativeBridgeService.isWrapper) {
      this.nativeVideoPlayerPlaceholderRef.changes.pipe(
        map((refs: QueryList<ElementRef>) => refs && refs.first && refs.first.nativeElement),
        filter((newEl: HTMLElement) => newEl && newEl !== this.nativeVideoPlayerPlaceholder),
        delay(0) // though already hidden by (state.loading === false), now spinner is still in DOM affecting the placeholder offset
      ).subscribe((newEl: HTMLElement) => {
        this.nativeVideoPlayerPlaceholder = newEl;
        this.nativeBridgeService.handleNativeVideoPlayer(newEl);
      });
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.isQuickSwitchPanelActive) {
      this.isQuickSwitchPanelActive = changes.isQuickSwitchPanelActive.currentValue;
    }
  }

  ngOnDestroy(): void {
    // unSubscription from liveServe PUSH updates
    if (this.eventEntity) {
      this.sport.unSubscribeEDPForUpdates();
    }

    if (this.initDataSubscription) {
      this.initDataSubscription.unsubscribe();
    }

    this.pubSubService.publish(this.pubSubService.API.SPORT_EDP_CLOSED);
    this.pubSubService.publish(this.pubSubService.API.UNSUBSCRIBE_LS_UPDATES_MS);
    this.pubSubService.publish(this.pubSubService.API.CASHOUT_CTRL_STATUS, { ctrlName: 'eventCashoutAndPlacedBets', isDestroyed: true });

    this.pubSubService.unsubscribe(this.tagName);

    this.messageListener && this.messageListener();
    this.windowRef.document.removeEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.setStreamShowFlag);
    this.sportEventPageProviderService.sportData.next(null);
    this.myBetsRef && this.myBetsRef.destroy();

    this.windowRef.document.removeEventListener('eventAlertsEnabled', this.handleFootballAlerts);

    // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
    this.windowRef.nativeWindow.removeEventListener('CURRENT_FOOTBALL_ALERTS_STATE_CHANGED', this.handleFootballAlerts);
    // TODO END

    this.closeCashoutStream();
    this.eventVideoStreamSubscriber && this.eventVideoStreamSubscriber.unsubscribe();
  }

  ngOnInit(): void {
    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
    this.eventId = this.activatedRoute.snapshot.paramMap.get('id');
    this.showMatchLive = this.activatedRoute.snapshot.paramMap.get('live') !== 'watch-live';
    this.isFootball = this.sportName === 'football';

    this.getIsEnhancedMultiplesEnabled().subscribe((isEnhancedMultiplesEnabled: boolean) => {
      this.isEnhancedMultiplesEnabled = isEnhancedMultiplesEnabled;
    });

    this.addListeners();

    this.initDataSubscription = this.sportsConfigService.getSport(this.sportName)
      .pipe(
        concatMap((sport: ISportInstance) => {
          this.sport = sport;
          this.catId = sport.config.request.categoryId;
          return this.init();
        })
      )
      .subscribe(() => {
        if (this.isFootball) {
          this.excludedFanzoneMarkets();
          
          this.nativeBridgeService.eventPageLoaded(this.eventId, this.sportName);
          // call nativeBridge to notify when football event detail page loading

          // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
          this.nativeBridgeService.footballEventPageLoaded(); // call nativeBridge to notify when football event detail page loading
          // TODO END
        }

      // Hide Opta scoreboard
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.HIDE_OPTA_SCOREBOARD, () => {
        if (this.optaScoreboardAvailable) {
          this.optaScoreboardAvailable = false;
          const customOrder = this.getSportScoreboardsLoadOrder().filter(id => !id.match(/^~?OPTA~?$/));
          this.prepareEventVisualization(customOrder);
        }
      });
      // listen to view type change
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
        this.streamShown = false;
        this.isLoggedIn = this.userService.status;
        this.nativeBridgeService.hideVideoStream();
        this.handleNativeorWebTutorialpopUp(); // Tennis, FB to open stream and bet pop-up on login
      });

        // Active Tab to open when user is logged in
        this.activeUserTab = 'markets';

        // Return if data is empty.
        if (this.eventData.event === undefined || (this.eventData.event && !this.eventData.event.length)) {
          this.hideSpinner();
          this.closeCashoutStream();
          return;
        }

        // Get event entity.
        this.eventEntity = this.eventData.event[0];
        this.typeId.emit(this.eventEntity.typeId);

        this.eventEntity.name = this.eventEntity.name.replace(/\*/g, ''); // removed serving sign

        this.showNewUserTabs = this.myTabsSport.includes(+this.eventEntity.categoryId) ||
          !!(this.sysConfig['ScoreboardsSports'] && this.sysConfig['ScoreboardsSports'][this.eventEntity.categoryId]);

        this.eventStartDate = this.timeService
          .formatByPattern(new Date(this.eventEntity.startTime), this.eventStartDatePattern, null, null, 'en-US');
        // Subscription for liveServe PUSH updates
        if (this.eventEntity) {
          this.sport.subscribeEDPForUpdates(this.eventEntity, _.contains(this.scoreSports, this.sportName.toUpperCase()));
        }

        this.handleNativeorWebTutorialpopUp();

        // Checks if event - Enhance Multiples.
        if (this.isFootball) {
          this.isEnhanceMultiples = this.sport.sportConfig.specialsTypeIds.includes(Number(this.eventEntity.typeId));
        }

        // Checks if event - OutRight.
        let sortCodeList;
        if (this.isOutrightSport(this.eventEntity.categoryCode)) {
          sortCodeList = OUTRIGHTS_CONFIG.outrightsSportSortCode;
        } else {
          sortCodeList = OUTRIGHTS_CONFIG.sportSortCode;
        }

        this.isOutRight = sortCodeList.indexOf(this.eventEntity.eventSortCode) !== -1;
        this.eventAutoSeoData();
        // check if event special (Enhance Multiples or OutRight).
        this.isSpecialEvent = this.isEnhanceMultiples || this.isOutRight;

        this.cssClass = `watch-${this.sportName}-live`;

      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SCOREBOARD_VISIBILITY, isVisible => {
        this.isScoreboardVis = isVisible;
        this.showWatchLiveWidget(true);
        this.showScoreboard = isVisible;
      });

      if (!this.isSpecialEvent) {
        // gets Markets By Collection.
        this.marketsByCollection = this.sport.extendMarketsCollections(this.eventData, this.DS_GAME);

        // forms tabs based on collections.
        this.eventTabs = this.sport.getCollectionsTabs(this.marketsByCollection,
          this.eventEntity,
          this.EDP_MARKETS, this.isMobileOnly);

        // LiveServe update - Market with in/out selections handler
        this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LIVE_MARKET_FOR_EDP, market => {
          const result = this.sport.updateCollectionsWithLiveMarket(market,
            this.marketsByCollection, this.eventEntity.markets, this.sportName);

          if (result) {
            this.eventTabs = this.sport.getCollectionsTabs(this.marketsByCollection, this.eventEntity, this.EDP_MARKETS, this.isMobileOnly);
            this.sportEventPageProviderService.sportData.next({
              sport: this.sport,
              eventData: this.eventData,
              eventTabs: this.eventTabs,
              marketsByCollection: this.marketsByCollection,
              sysConfig: this.sysConfig,
              isSpecialEvent: this.isSpecialEvent,
              isMTASport: this.isMTASport(),
              templateMarketName: market.templateMarketName
            });
          }
        });
        }

        this.sportEventPageProviderService.sportData.next({
          sport: this.sport,
          eventData: this.eventData,
          eventTabs: this.eventTabs,
          marketsByCollection: this.marketsByCollection,
          sysConfig: this.sysConfig,
          isSpecialEvent: this.isSpecialEvent,
          isMTASport: this.isMTASport()
        });

        this.hideSpinner();

        // Set startTime to NativeBridge.
        if (this.eventEntity.categoryName === 'Football') {
          this.nativeBridgeService.eventStartTime = this.eventEntity.startTime;
        }

        // if event has placed bets check if cash out bets are available as well
        if (!_.isEmpty(this.placedBets)) {
          this.getCashOutData(this.placedBets);
        } else {
          this.closeCashoutStream();
        }

        if (this.eventEntity.liveStreamAvailable) {
          this.setHandlers();
          // eslint-disable-next-line
          this.eventVideoStreamSubscriber = this.eventVideoStreamProviderService.playSuccessErrorListener.subscribe(streamShown => {
            this.streamShown = streamShown;
          });
        }

        this.messageListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow,
          'message', event => this.visEventService.visListener(event));

        this.subscribeForEventBetsUpdates();

        /**
         * Scoreboards and visualization entry point.
         */
        this.fallbackScoreboardType = this.scoreParserService.getScoreType(this.eventEntity.categoryId);
        this.prepareEventVisualization();

        this.subscribeForCahoutUpdates();

      this.setActiveUserTab = this.setActiveUserTab.bind(this);
      this.checkFootballAlerts();
      this.favouritesVisible = this.isFavouritesVisible();
      // This event is camelCase, because it is called from NativeBridge on Connect app.
      // It should be renamed to upper case when the same is done on native parts of Connect app.
      this.pubSubService.subscribe(this.tagName,
        this.pubSubService.API.CURRENT_FOOTBALL_ALERTS_STATE_CHANGED, this.handleFootballAlerts);
      this.windowRef.document.addEventListener('eventAlertsEnabled', this.handleFootballAlerts);

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      this.windowRef.nativeWindow.addEventListener('CURRENT_FOOTBALL_ALERTS_STATE_CHANGED', this.handleFootballAlerts);
      // TODO END
      this.quickSwitchEnabled();
    }, (error) => {
      this.showError();
      console.warn('EDP Page Load:', error.error || error);
    });
    this.checkSignPosting();
  }

  checkSignPosting() {
    //my bets signposting logic
    const spDataArray = this.storageService.get('myBetsSignPostingData');
    if (spDataArray) {
      this.showSignPosting = spDataArray.some((eventData) => Number(eventData.eventId) === Number(this.eventId) && eventData.betIds.length > 0);
    }
  }

  sendEventDetailsToNative() {
    // Set state of video play button on wrapper
    if (this.deviceService.isWrapper) {
      this.streamShown = this.nativeBridgeService.playerStatus;
      if (this.eventEntity.liveStreamAvailable) {
        this.nativeBridgeService.onEventDetailsStreamAvailable({
          categoryId: Number(this.eventEntity.categoryId),
          classId: Number(this.eventEntity.classId),
          typeId: Number(this.eventEntity.typeId),
          eventId: Number(this.eventEntity.id)
        });
      }
    }
  }

  private handleNativeorWebTutorialpopUp(): void {
    this.eventVideoStreamProviderService.getStreamBetCmsConfig().subscribe((streamBetWeb:IStreamBetWeb) => {
      this.streamBetCmsConfig = streamBetWeb;
      const streamBetConfig = {
        streamBetCmsConfig: this.streamBetCmsConfig,
        isTablet: this.deviceService.isTabletOrigin,
        isMobile: this.deviceService.isMobile,
        isDesktop: this.deviceService.isDesktop, 
        providerInfo: this.eventEntity.streamProviders,
        categoryId: this.eventEntity.categoryId
      }
      if (this.eventVideoStreamProviderService.isStreamBetAvailable(streamBetConfig,this.tagName)) {
        this.isStreambetAvailable = true;
      }
      else {
        this.sendEventDetailsToNative();
      }
    });
    
  }

  isLoadedHandler(isLoaded: boolean) {
    this.isScoreLoaded = isLoaded;
  }

  isLoading() {
    return this.optaScoreboardAvailable || this.gpScoreboardAvailable
      ? !this.isScoreLoaded && this.isOptaScoreboardChecked
      : !this.isOptaScoreboardChecked;
  }

  isFavouritesVisible(): boolean {
    return this.sportName === 'football' && !this.isSpecialEvent && !this.hasMarketSPFlag();
  }

  /**
   * Checks if event's market has "SP" flag in "drilldownTagNames".
   * @return {boolean}
   * @private
   */
  hasMarketSPFlag(): boolean {
    const SP_FLAG = 'MKTFLAG_SP';
    const market = _.isArray(this.eventEntity.markets) && this.eventEntity.markets[0];
    const drilldownTagNames = market && market.drilldownTagNames;

    return _.isString(drilldownTagNames) && drilldownTagNames.indexOf(SP_FLAG) > -1;
  }

  /**
   * Check if markets tab should be available
   */
  isMarketsTabAvailable(): boolean {
    if (this.showNewUserTabs) {
      return (this.isLoggedIn && this.myBetsAvailable);
    }
    return (this.isLoggedIn && this.myBetsAvailable) || this.eventEntity.liveStreamAvailable;
  }

  /**
   * Handler for click on football bell icon.
   */
  onFootballBellClick(): void {
    this.nativeBridgeService.onEventAlertsClick(
      this.eventId,
      this.sportName,
      this.sport.config.request.categoryId,
      this.eventData.event[0].drilldownTagNames,
      ALERTS_GTM.EVENT_SCREEN);

    // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
    this.nativeBridgeService.showFootballAlerts();
    // TODO END
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

  checkDeviceOS(osList: string[]): boolean {
    return _.contains(osList, this.nativeBridgeService.getMobileOperatingSystem());
  }

  handleFootballAlerts(data: IConstant): void {
    // TODO: Reverted changes from BMA-37049. '|| data.detail.settingValue' Will be removed after new approach implementation.
    this.footballBellActive = data.detail.isEnabled || data.detail.settingValue;
    // TODO END
  }

  /**
   * Check if event title bar is available
   */
  isEventTitleBarAvailable(): boolean {
    return (
      this.isIMGScoreboardAvailable ||
      (this.isOptaScoreboardChecked &&
        !this.optaScoreboardAvailable &&
        !this.bgScoreboardConfig.available &&
        !this.brScoreboardConfig.available)
    );
  }

  checkFootballAlerts(): void {
    // TODO: Reverted changes from BMA-37049.
    // '|| this.nativeBridgeService.hasShowFootballAlerts()' Will be removed after new approach implementation.
    const alertsEnabled = this.nativeBridgeService.hasOnEventAlertsClick() || this.nativeBridgeService.hasShowFootballAlerts();
    // TODO END
    if (alertsEnabled && this.sportName === 'football' && !this.isOutRight) {
      // Get visible notification icons from sport types (e.g. Euro 2016, Copa America)
      (this.cmsService.getFeatureConfig('NativeConfig',false)).subscribe(data => {
        // TODO: Reverted changes from BMA-37049.
        // '|| data.NativeConfig && data.NativeConfig.visibleNotificationIcons' Will be removed after new approach implementation.
        if (data && data.visibleNotificationIconsFootball ||
          data && data.visibleNotificationIcons) {
          // TODO END
          // TODO: Reverted changes from BMA-37049.
          // '|| data.NativeConfig.visibleNotificationIcons' Will be removed after new approach implementation.
          const { multiselectValue = '', value = '' } = data.visibleNotificationIconsFootball ||
            data.visibleNotificationIcons || {};
          // TODO END
          const isOSPermitted = this.checkDeviceOS(multiselectValue);
          const allowedLeaguesList = _.isString(value) ? value.split(/\s*,\s*/) : [];

          this.footballAlertsVisible = isOSPermitted && this.isFootball && _.contains(allowedLeaguesList, this.eventEntity.typeName);
        }
      });
    } else {
      this.footballAlertsVisible = false;
    }
  }

  /**
   * Click on the Video Stream button.
   * Toggle Video Stream Area.
   * param {object} event object.
   *
   */
  public playStream(event: Event): void {
    event.preventDefault();
    this.streamShown = !this.streamShown;
    this.eventVideoStreamProviderService.playListener.next();
    // hide video placeholder if stream is not shown
    if (this.deviceService.isWrapper && !this.streamShown) {
      this.nativeBridgeService.handleNativeVideoPlaceholder(false, this.nativeVideoPlayerPlaceholder);
    }
  }

  get isMatchLive(): boolean {
    const preMatch = this.preMatchWidgetAvailable;
    const betGenius = this.bgScoreboardConfig && this.bgScoreboardConfig.available;
    const betRadar = this.brScoreboardConfig && this.brScoreboardConfig.available;
    const imgArena = this.imgFrontRowArena && this.imgFrontRowArena.available;
    const visualization = this.eventsWithVisualizationParams && this.eventsWithVisualizationParams.length;
    const scoreboard = this.isScoreboardVis && this.gpScoreboardAvailable;
    const optaScoreboard = this.optaScoreboardAvailable;
    return !!(optaScoreboard || visualization || preMatch || scoreboard || betGenius || betRadar || imgArena);
  }
 set isMatchLive(value:boolean){}
  /**
   * Show Watch Live Widget
   * @returns {boolean}
   */
  public showWatchLiveWidget(isButtons: boolean): boolean {
    const isWatchLive = this.eventEntity.liveStreamAvailable;
    return isButtons ? this.isMatchLive && isWatchLive : this.isMatchLive || isWatchLive;
  }

  /**
   * Set active user tab
   * @params{string} tab name
   */
  public setActiveUserTab(tabName: string): void {
    if (this.editMyAccaUnsavedOnEdp) {
      this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
    } else {
      this.activeUserTab = tabName;
    }

    // GA track when user clicks on MyBets tab BMA-19137
    if (tabName === 'myBets') {
      this.trackMyBetsTabSwitch();
    }
  }

  /**
   * Dats disclimer text shown when scores availble only
   * @return boolean
   */
  isShownDisclaimer(): boolean {
    return this.dataDisclaimer.enabled && this.eventEntity.eventIsLive && !this.isOutRight &&
      (this.isFallbackScoreboards || this.bgScoreboardConfig.available || this.brScoreboardConfig.available
        || this.optaScoreboardAvailable);
  }

  protected init(): Observable<any> {
    const loadActions = [
      this.getEventData(),
      this.setDS(),
      this.setEDPMarkets(),
      this.setSystemConfig(),
      this.setScoreBoards()
    ];

    if (this.isLoggedIn) {
      // avoid unnecessary bet-history.js bundle lazyload for not logged-in user, when bet data is anyway resolved as null
      loadActions.push(
        this.setCashoutBets(),
        this.setPlacedBets()
      );
    }

    return forkJoin(loadActions);
  }

  protected subscribeEditAccaChanges(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EDIT_MY_ACCA, () => {
      from(Promise.all([
        this.commandService.executeAsync(this.commandService.API.GET_CASH_OUT_BETS_ASYNC, [], [])
          .then(data => this.cashoutBets = data),
        this.commandService.executeAsync(this.commandService.API.GET_PLACED_BETS_ASYNC, [this.eventId], [])
          .then(data => this.placedBets = data)
      ])).subscribe(() => {
        this.getCashOutData(this.placedBets);
        this.updateSignPosting(true);
      });
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
      this.editMyAccaUnsavedOnEdp = unsaved;
    });
  }

  protected subscribeForCahoutUpdates(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.CASH_OUT_BET_PROCESSED, (betId: string) => {
      this.cashoutIds = _.filter(this.cashoutIds, (id: ICashoutMapItem) => id.id !== betId);
      this.updateCashoutBets(this.placedBets, betId);
      this.updateCashoutBets(this.cashoutBets, betId);
      const counter = this.getFilteredBets()?.length;
      this.myBetsAvailable = counter > 0;

      // Set sign posting Flag when do cashout success
      const spData = this.storageService.get('myBetsSignPostingData');
      if(spData) {
        this.showSignPosting = spData.some((evenData) => Number(evenData.eventId) === Number(this.eventId) && evenData.betIds.length > 0);
      }

      if(this.myBetsAvailable) {
        this.myBetsCounter = counter;
        this.myBets = this.myBetsTabName(counter);
      } else {
        this.setActiveUserTab('markets');
      }
    });
  }
  
  protected subscribeForEventBetsUpdates(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.MY_BET_PLACED, (placedBet: any) => {
    let finalBets = this.placedBets;
      if(placedBet.isquickbet) {
        this.commandService.executeAsync(this.commandService.API.GET_PLACED_BETS_ASYNC, [this.eventId], [])
        .then(data => {
          this.placedBets = data;
          const qb = this.placedBets.filter(bet => bet.betId ===placedBet.id.toString());
          this.tempBets = [...this.tempBets, ...qb];
          this.showSignPosting = true;
          this.showMybetTab();
        });
      } else {
        this.tempBets = [...this.tempBets, ...placedBet.bets];
        this.extendCashoutBets(this.tempBets);
        if(!_.isEmpty(this.placedBets)) {
          finalBets = this.placedBets.filter((bet:any) => (bet.cashoutStatus != 'BET_CASHED_OUT' && bet.uniqueId !== "0"));
          this.placedBets = [...this.tempBets, ...finalBets];
        } else {
          this.placedBets = [...this.tempBets];
        }
        this.showSignPosting = true;
        this.showMybetTab();
      }    
    });
  }
  showMybetTab() {
    this.placedBets = this.getFilteredBets();
    const uniqset = [... new Set(this.placedBets.map(bet => bet.betId))];
    this.setCashoutIds(uniqset);
    const counter = uniqset.length;
    this.myBetsAvailable = counter > 0;
    if (this.activeUserTab === 'myBets') {
      this.setActiveUserTab('markets');
    }
    this.myBetsCounter = counter;
    this.myBets = this.myBetsTabName(counter);
  }
  setCashoutIds(temparr) {
    const tempCashIds = [];
    temparr.map(bet => tempCashIds.push({ id: bet, isSettled: false }));
    this.cashoutIds = [...tempCashIds];
  }
  getFilteredBets() {
    return this.placedBets
    .filter((bet: RegularBetBase) => (JSON.stringify(bet.leg).includes(this.eventId)
    && bet.settled !== 'Y'
    && bet.cashoutStatus !== 'BET_CASHED_OUT'
    && bet.type !== 'placedBetsWithoutCashoutPossibility'));
  }
  isTempBetsAvailable() {
    let farr = [];
    if(this.cashoutBets) {
      farr = this.tempBets?.filter(bet =>!JSON.stringify(this.cashoutBets).includes(bet.id || bet.betId));
    } else if(!this.cashoutBets && this.tempBets) {
      farr = this.tempBets;
    }
    return farr;
  }
  updateCashoutData() {
    this.placedBets = this.getFilteredBets();    
    
    this.updateSignPosting();
    
    if(!this.isTempBetsAvailable().length) {
      return;
    }
    if(!this.cashoutWsConnectorService.getConnection()) {
      this.openCashoutStream('onclick');
      } else  {
        this.cashoutWsConnectorService.dateChangeBet().subscribe((res: any) => {
          this.cashoutBets = res;
          if (this.cashoutBets) {
            this.cashOutMapService.createCashoutBetsMap(
              res,
              this.userService.currency,
              this.userService.currencySymbol
            );
          this.changeDetectorRef.detectChanges();
          this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
          }
        });
      }
  }

  private updateSignPosting(editAcca?: boolean) {
    //remove from local storage when my bets section Visited
    const signPostingData = this.storageService.get('myBetsSignPostingData');
    if(signPostingData){
      const index = signPostingData.findIndex(eventData => Number(eventData.eventId) === Number(this.eventId));
      if (index !== -1) {
        if(!editAcca) {
          signPostingData.splice(index, 1);
          this.showSignPosting = false;
        } else {
          this.checkSignPosting();
        }
      }
      this.storageService.set('myBetsSignPostingData', signPostingData);
    }
  }
  extendCashoutBets(bets) {
    (bets || []).forEach(bet => bet.betId = bet.betId ? bet.betId : bet.id);
  }
  /**
   * Return event and collection.
   * @return {Promise} Promise
   */
  protected getEventData(): Observable<IEventData> {
    return this.sport.getById(this.eventId, false, true, this.isMTASport()).pipe(
      map(data => {
        const event = this.getEventFromEventData(data);

        if (!event && this.eventData) {
          const oldEventData = this.getEventFromEventData(this.eventData);
          // manually set displayed = 'N' for already loaded event if no event in response
          if (oldEventData) {
            oldEventData.displayed = 'N';
          }
        } else {
          this.eventData = data;
        }

        return data;
      })
    );
  }

  /**
   * Get event object from event data, depends on structure (sport or racing)
   * @param {object} data - event data
   * @return {object} event
   */
  protected getEventFromEventData(data: IEventData): ISportEvent {
    return (data.event && data.event[0]) || data[0];
  }

  public onPlayLiveStreamError(): void {
    this.streamShown = false;
    this.changeDetectorRef.detectChanges();
  }

  protected setDS(): Observable<void> {
    return from(this.commandService.executeAsync(
      this.commandService.API.DS_GET_GAME,
      [this.eventId, this.catId], []
    )).pipe(map(data => {
      this.DS_GAME = data;
    }));
  }

  protected setEDPMarkets(): Observable<void> {
    return this.cmsService.getEDPMarkets().pipe(
      map(data => this.EDP_MARKETS = data),
      catchError(() => this.EDP_MARKETS = [])
    );
  }

  protected setSystemConfig(): Observable<void> {
    return this.cmsService.getSystemConfig().pipe(
      map((data: ISystemConfig) => {
        this.dataDisclaimer = data.ScoreboardsDataDisclaimer ? data.ScoreboardsDataDisclaimer : { enabled: false};
        return _.extend(this.sysConfig, data);
      })
    );
  }

  protected setScoreBoards(): Observable<void> {
    return this.cmsService.getFeatureConfig(
      'ScoreboardsSports',
      false,
      true).pipe(
      map((data: ISystemConfig) => _.extend(this.sysConfig, {ScoreboardsSports: data}))
    );
  }

  private setCashoutBets(): Observable<void> {
    return from(this.commandService.executeAsync(
      this.commandService.API.GET_CASH_OUT_BETS_ASYNC,
      [],
      [])).pipe(
      map((data: RegularBetBase[]) => {
        this.cashoutBets = data;
      })
    );
  }

  private setPlacedBets(): Observable<void> {
    return from(this.commandService.executeAsync(
      this.commandService.API.GET_PLACED_BETS_ASYNC,
      [this.eventId],
      [])).pipe(
      map((data: RegularBetBase[]) => {
        this.placedBets = data;
      })
    );
  }

  private getIsEnhancedMultiplesEnabled(): Observable<boolean> {
    return this.cmsService.getToggleStatus('EnhancedMultiples');
  }

  private isOutrightSport(code: string): boolean {
    return _.indexOf(OUTRIGHTS_CONFIG.outrightsSports, code) !== -1;
  }

  private setHandlers(): void {
    // add listener for native player only on wrapper
    if (this.deviceService.isWrapper) {
      this.windowRef.document.addEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.setStreamShowFlag);
    }
  }

  private setStreamShowFlag(data): void {
    this.streamShown = data.detail.settingValue;
  }

  /**
   * Google analytics myBets tab
   * Push object into dataLayer
   */
  private trackMyBetsTabSwitch(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'content',
      eventAction: 'click',
      eventLabel: `event page - my bets (${this.myBetsCounter})`,
      eventID: this.eventEntity.id,
      location: 'event page'
    });
  }

  private getCashOutData(bets: RegularBetBase[]) {
    this.cashoutDataSubscription = from(this.commandService.executeAsync(
      this.commandService.API.GET_BETS_FOR_EVENT_ASYNC,
      [
        this.eventEntity.id,
        this.cashoutBets,
        bets
      ],
      {}
    )).subscribe((betsData: { cashoutIds: ICashoutMapItem[], placedBets: RegularBetBase[] }) => {
      const placedBets: RegularBetBase[] = betsData.placedBets
        .filter((bet: RegularBetBase) => bet.settled !== 'Y' && bet.cashoutStatus !== 'BET_CASHED_OUT');

      // make my bets tab available is event has placed or cash out bets
      if (placedBets.length || betsData.cashoutIds.length) {
        this.cashoutIds = betsData.cashoutIds;
        this.placedBets = placedBets;
        this.myBetsCounter = this.placedBets.length;
        this.myBets = this.myBetsTabName(this.myBetsCounter);
        this.myBetsAvailable = true;
        this.openCashoutStream();
      } else {
        this.myBetsAvailable = false;
        this.closeCashoutStream();

        if (this.activeUserTab === 'myBets') {
          this.setActiveUserTab('markets');
        }
      }

      this.changeDetectorRef.detectChanges();
      this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
    });
  }

  private openCashoutStream(source?): void {
    this.betsStreamOpened = true;
    this.commandService.executeAsync(this.commandService.API.OPEN_CASHOUT_STREAM).then((data: IBetDetail[]) => {
      if (data) {
        this.cashOutMapService.createCashoutBetsMap(
          data,
          this.userService.currency,
          this.userService.currencySymbol
        );
        if(source){
          this.changeDetectorRef.detectChanges();
          this.pubSubService.publish(this.pubSubService.API.MY_BETS_UPDATED);
        }
      }
    });
  }

  private closeCashoutStream(): void {
    if (this.cashoutDataSubscription) {
      this.cashoutDataSubscription.unsubscribe();
    }

    if (this.betsStreamOpened) {
      this.commandService.executeAsync(this.commandService.API.CLOSE_CASHOUT_STREAM);
      this.betsStreamOpened = false;
    }
  }

  private myBetsTabName(counter: number): string {
    const name = this.localeService.getString('sb.myBets');

    return Number(counter) ? `${name} (${counter})` : name;
  }

  private updateCashoutBets(list: RegularBetBase[] = [], id: string): void {
    if (!Array.isArray(list)) {
      return;
    }

    list.forEach((bet: RegularBetBase) => {
      if (bet.betId === id) {
        bet.type = 'placedBetsWithoutCashoutPossibility';
      }
    });
  }

  // Visualization implementation
  // TODO: stuff might be encapsulated in a child component
  /**
   * Depending on event live/pre-live type defines configuration for needed visualisation/pre-match widget.
   * May utilize sport-predefined or provided custom load order.
   */
  private prepareEventVisualization(customScoreboardsLoadOrder?: string[]): void {
    const loadOrder = customScoreboardsLoadOrder || this.getSportScoreboardsLoadOrder();

    this.visualizationCmsGuard()
      .pipe(
        mergeMap(() => this.loadVisualization(loadOrder)),
        finalize(() => {
          this.isOptaScoreboardChecked = true;
        }),
      )
      .subscribe();
  }

  /**
   * Defines loading sequence of scoreboards for sport.
   */
  private getSportScoreboardsLoadOrder(): string[] {
    return this.eventEntity.eventIsLive ?
      this.scoreboardsLoadOrder[this.sportName] || this.scoreboardsLoadOrder.default :
      ['OPTA', 'PM'];
  }

  /**
   * Builds the observable-based scoreboard load chain from scoreboardsLoaders map.
   * Chain is resolved consecutively, as soon as scoreboard is found,
   * loader emits an EMPTY observable, which by default terminates the load process.
   * However, if any loaderId ends with ~ character (which means proceed further on success),
   * the defaultIfEmpty operator will be piped to the loader, which will continue the load chain.
   */
  private loadVisualization(loadOrder: string[] = []): Observable<IScoreboardConfig | never> {
    const scoreboardConfig = this.sport.getScoreboardConfig() || {};
    const loadChain = loadOrder.reduce((loadersList, rawLoaderId) => {
      const continueFlag = rawLoaderId.endsWith('~'),
        loaderId = continueFlag ? rawLoaderId.replace(/~$/, '') : rawLoaderId,
        loader = this.scoreboardsLoaders[loaderId];

      if (loader) {
        loadersList.push(switchMap(!continueFlag ? loader :
          (config: IScoreboardConfig) => loader(config).pipe(defaultIfEmpty(scoreboardConfig))));
      }
      return loadersList;
    }, []);

    return (observableOf(scoreboardConfig) as any).pipe(...loadChain);
  }

  /**
   * Check whether showing Visualization/Scoreboards is not disabled in CMS for current sport category.
   */
  private visualizationCmsGuard(): Observable<null | never> {
    return this.cmsService.getSystemConfig().pipe(
      switchMap((config: ISystemConfig) => {
        const categoriesMap = config && config.VisualisationDisabledCategory || {};
        return Object.keys(categoriesMap).some(id => id === this.eventEntity.categoryId && categoriesMap[id]) ?
          EMPTY : observableOf(null);
      })
    );
  }

  /**
   * Visualization loaders go here.
   * Each loader is an independent observable-based structure,
   * which can be piped into a chain in any order required.
   */
  private preMatchLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    return this.visEventService.checkPreMatchWidgetAvailability(this.eventId)
      .pipe(
        switchMap(response => {
          this.preMatchWidgetAvailable = response;
          return EMPTY;
        }),
        catchError((): Observable<IScoreboardConfig> => {
          return observableOf(scoreboardConfig);
        })
      );
  }

  private imgLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    return this.visDataHandler.init(this.eventEntity).pipe(
      switchMap(visData => {
        this.isIMGScoreboardAvailable = !!(visData && visData.eventsWithVisualizationParams &&
          visData.eventsWithVisualizationParams.length);

        if (this.isIMGScoreboardAvailable) {
          this.eventsWithVisualizationParams = visData.eventsWithVisualizationParams;
          return EMPTY;
        }
        return observableOf(scoreboardConfig);
      }),
      catchError((): Observable<IScoreboardConfig> => {
        this.isIMGScoreboardAvailable = false;
        return observableOf(scoreboardConfig);
      })
    );
  }

  private optaLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    return this.sportEventMainProviderService.checkOptaScoreboardAvailability(this.eventEntity).pipe(
      switchMap(() => {
        this.isOptaProviderPresent = this.sportEventMainProviderService.isOptaProviderPresent;
        this.isOptaScoreboardChecked = true;
        this.optaScoreboardAvailable = true;
        this.changeDetectorRef.detectChanges();
        return EMPTY;
      }),
      catchError((): Observable<IScoreboardConfig> => {
        return observableOf(scoreboardConfig);
      })
    );
  }

  private fallbackScoreboardLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    if (this.sysConfig && this.sysConfig.FallbackScoreboard && this.sysConfig.FallbackScoreboard.enabled) {
      const scoreTypes = Object.keys(this.sysConfig.FallbackScoreboard) as [IScoreType];
      this.fallbackScoreboardType = scoreTypes.find((scoreType: IScoreType) => {
        if (scoreType as string !== 'enabled') {
          const sportIds = this.sysConfig.FallbackScoreboard[scoreType] as string;
          if (sportIds.split(',').includes(this.eventEntity.categoryId)) {
            return true;
          }
        }
      });
    }

    this.isFallbackScoreboards = !!(this.eventEntity.comments && this.eventEntity.comments.teams) ||
      !!this.scoreParserService.parseScores(this.eventEntity.originalName, this.fallbackScoreboardType);

    return this.isFallbackScoreboards ? EMPTY : observableOf(scoreboardConfig);
  }

  private betGeniusLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    if (scoreboardConfig.type === 'betGenius') {
      return this.cmsService.getMenuItems().pipe(
        map((data: ISportCategory[]): ISportCategory => _.findWhere(data, { categoryId: Number(this.eventEntity.categoryId) })),
        switchMap((cmsConfig: ISportCategory): Observable<IScoreboardConfig | never> => {
          this.bgScoreboardConfig = {
            available: cmsConfig.showScoreboard,
            eventId: this.eventEntity.id
          };
          return this.bgScoreboardConfig.available ? EMPTY : observableOf(scoreboardConfig);
        }),
        catchError(() => {
          this.bgScoreboardConfig = { available: false };
          return observableOf(scoreboardConfig);
        })
      );
    }
    return observableOf(scoreboardConfig);
  }

  private betRadarLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig> {
    return this.sportEventMainProviderService.checkBetradarAvailability(this.eventEntity).pipe(
      switchMap((eventMapping: ISportByMapping) => {
        this.brScoreboardConfig = {
          available: true,
          eventId: this.eventEntity.id
        };
        this.betRadarMatchId = Number(eventMapping.feedMappings[0].id);
        return EMPTY;
      }),
      catchError((): Observable<IScoreboardConfig> => {
        return observableOf(scoreboardConfig);
      })
    );
 }

  /**
   * Get the img arena event details and enable flag to show img arena scoreboard
   * This function is part of scoreboard loader observables chain
   * Also check the device and category code
   * @param scoreboardConfig
   * @returns {*}
   * @private
   */
  private imgArenaLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig>{
    return this.sportEventMainProviderService.checkImgArenaScoreboardAvailability(this.eventEntity).pipe(
      switchMap((eventMapping: ISportByMapping) => {
        this.imgFrontRowArena = {
          available: true
        };
        this.imgEventDetails = eventMapping && eventMapping.feedMappings && eventMapping.feedMappings[0].id;
        return EMPTY;
      }),
      catchError((): Observable<IScoreboardConfig> => {
        return observableOf(scoreboardConfig);
      })
    );
  }

  private grandParadeLoader(scoreboardConfig: IScoreboardConfig): Observable<IScoreboardConfig | never> {
    this.checkGrandParadeAvailability();

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SYSTEM_CONFIG_UPDATED, (updatedConfig: ISystemConfig) => {
      if (!_.isEqual(this.sysConfig.Scoreboard, updatedConfig.Scoreboard)) {
        this.sysConfig.Scoreboard = updatedConfig.Scoreboard;
        this.checkGrandParadeAvailability(true);
      }
    });
    return observableOf(scoreboardConfig); // may be changed to EMPTY
  }

  /**
   * Checks if GrandParade scoreboards are available and updates the scoreboardUrl property.
   */
  private checkGrandParadeAvailability(forceUrlUpdate: boolean = false): void {
    const isLiveVisualisationAvailable = !!(this.eventsWithVisualizationParams && this.eventsWithVisualizationParams.length),
      isScoreboardCMSEnabled = this.coreTools.hasOwnDeepProperty(this.sysConfig, 'Scoreboard.showScoreboard') &&
        this.sysConfig.Scoreboard.showScoreboard === 'Yes';

    this.gpScoreboardAvailable = !this.isSpecialEvent && !isLiveVisualisationAvailable && isScoreboardCMSEnabled;

    if (this.gpScoreboardAvailable || forceUrlUpdate) {
      this.cmsService.getMenuItems().pipe(
        map((data: ISportCategory[]): string => {
          const sysConfigUrl = this.sysConfig && this.sysConfig.Scoreboard && this.sysConfig.Scoreboard.scoreboardUrl || '';
          const gpScoreboardsUrl = _.find(data, sport => sport.categoryId === Number(this.eventEntity.categoryId));
          return (gpScoreboardsUrl && gpScoreboardsUrl.scoreBoardUrl && gpScoreboardsUrl.showScoreboard)
            ? gpScoreboardsUrl.scoreBoardUrl : sysConfigUrl;
        })
      ).subscribe(scoreboardUrl => {
        this.scoreboardUrl = scoreboardUrl;
      });
    }
  }

  private addListeners(): void {
    this.subscribeEditAccaChanges();

    if (this.nativeBridgeService.isWrapper) {
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.IS_NATIVE_VIDEO_STICKED, (state: boolean) => {
        this.nativeBridgeService.handleNativeVideoPlaceholder(state, this.nativeVideoPlayerPlaceholder);
        this.pubSubService.publish(this.pubSubService.API.PIN_TOP_BAR, state);
      });
    }
  }
  /**
   * Assigns autoSeoData object and publish the data for event-autoseo
   */
  private eventAutoSeoData(): void {
    this.autoSeoData.isOutright = this.isOutRight;
    this.autoSeoData.categoryName = this.eventEntity.categoryName;
    this.autoSeoData.typeName = this.eventEntity.typeName;
    this.autoSeoData.name = this.eventEntity.name;
    this.pubSubService.publish(this.pubSubService.API.AUTOSEO_DATA_UPDATED, this.autoSeoData);
  }

  /** 
   * Excluding the fanzone MKTFLAG_FZ markets in the event data
  */
  private excludedFanzoneMarkets(): void {
    if(this.eventData.event && this.eventData.event[0] && this.eventData.event[0].markets) {
      this.eventData.event[0].markets = this.getExcludedDrilldownTagNameMarkets(this.eventData.event[0].markets);
    }
    
    if (this.eventData.collection && this.eventData.collection.length > 0) {
      this.eventData.collection.forEach((colection) => {
        if(colection.markets) {
          colection.markets = this.getExcludedDrilldownTagNameMarkets(colection.markets);
        }
      });
    }
  }

  /**
   * get excluded Fanzone drilldownTagNames markets
   * @param {IMarket[]} markets
   * @returns {IMarket[]}
   */
  private getExcludedDrilldownTagNameMarkets(markets: IMarket[]): IMarket[] {
    return markets.filter((market) => !(market.drilldownTagNames && market.drilldownTagNames.includes('MKTFLAG_FZ')));
  }

  /**
   * if isMTASport returns true, MTA doesn't apply
   * @returns {boolean}
   */
  protected isMTASport(): boolean{
    return !environment.CATEGORIES_DATA.unhandledSportsForMTA.includes(this.catId) && this.deviceService.getDeviceViewType().mobile && !this.deviceService.isTabletOrigin;
  }
  /**   
    * To check if LuckyDip Market available
   * @param {ISportEvent} event
   * @returns {boolean}
   */
  isLuckyDipMarket(event: ISportEvent): boolean|IMarket[] {
   let isLD : boolean | IMarket[] = false;
   const sysConfig: boolean = this.sysConfig && this.sysConfig.LuckyDip && this.sysConfig.LuckyDip.enabled;
   const obConfig: IMarket = event.markets.find(market => market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1);
   const isLuckyDipConfig = sysConfig && obConfig && event.eventSortCode === LUCKY_DIP_CONSTANTS.TNMT;
    event.markets.forEach(market => {
      market.isLuckyDip = market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1;
   });
   isLD = (isLuckyDipConfig)? true: (!sysConfig && obConfig)? event.markets = event.markets.filter(market => !market.isLuckyDip): false;
   return isLD;
  }
  /**
   * Returns whether quick switch panel is active or not
   */
  quickSwitchEnabled(): void {
    this.cmsService.getFeatureConfig('EventQuickSwitcher').subscribe((data: ISystemConfig) => {
      if(data?.isQuickSwitchEnabled) {
        this.isQuickSwitchEnabled = this.quickSwitchEnabledSports.includes(this.sportName) && !this.sportEventHelperService.isOutrightEvent(this.eventEntity) && !this.sportEventHelperService.isSpecialEvent(this.eventEntity, false);
        this.quickSwitchHandler.emit(this.isQuickSwitchEnabled);
      }
    });
  }
  /**
   * Hide/Show quick switch window
   */
  changeMatchToggle(): void {
    this.changeMatch = !this.changeMatch;
  }
  /**
   * Close quick switch window
   */
  closeQuickSwitchPanel(): void {
    this.changeMatch = false;
  }
  
  /**
   * Close quick switch window
   */
  handleQuickSwitchEvent(output: ILazyComponentOutput): void {
    if (output.output === 'closeQuickSwitchPanel') {
      this.changeMatch = false;
    }
  }
}
