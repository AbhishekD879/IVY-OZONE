import { PERFORMANCE_API_MARK } from '@lazy-modules/performanceMark/enums/performance-mark.enums';
import { Subscription } from 'rxjs';
import { Component, OnInit, OnChanges, OnDestroy, ChangeDetectorRef, Input, Output, EventEmitter, ChangeDetectionStrategy, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';
import { DeviceService } from '@app/core/services/device/device.service';

import environment from '@environment/oxygenEnvConfig';
import { IBadgeModel } from '../../models/output-module.model';
import { IOutputModule } from '@featured/models/output-module.model';
import { IFeaturedModel } from '../../models/featured.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ISystemConfig } from '@core/services/cms/models';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FeaturedModuleService } from '../../services/featuredModule/featured-module.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { UserService } from '@core/services/user/user.service';
import { EventService } from '@app/sb/services/event/event.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { IRpgConfig } from '@app/lazy-modules/rpg/rpg.model';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { IEagerLoadCMSCount } from '../../models/highlights-carousel.model';
import { StorageService } from '@core/services/storage/storage.service';
@Component({
  selector: 'featured-module',
  styleUrls: ['./featured-module.component.scss'],
  templateUrl: './featured-module.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedModuleComponent implements OnInit, OnDestroy, OnChanges {
  @Input() hubIndex: number;
  @Input() sportId: number = 0;
  @Input() sportName: string;
  @Input() shouldDisplayLoader: boolean = true;
  @Input() showOnlyBigCompetitionData: boolean = false;
  @Input() participants = [];
  @Input() surfaceBetIds = [];
  @Input() highlightCarouselIds = [];
  @Output() readonly isLoadedEvent = new EventEmitter<boolean>();
  @Output() readonly featuredEventsCount = new EventEmitter<number>();

  raceGridRaces: { data: any };
  moduleName: string = 'featured';
  isConnectSucceed: boolean;
  ssDown: boolean;
  badges: { [key: string]: IBadgeModel };
  featuredModuleData: IFeaturedModel;
  isYourcallInCmsEnabled: boolean;
  isSportsQuickLinksEnabled: boolean;
  isHighlightCarouselEnabled: boolean = false;
  isInplayModuleEnabled: boolean = false;
  isFanzoneConfigEnabled: boolean = false;
  isBetpackConfigEnabled: boolean = false;
  isModuleAvailable: boolean = false;
  noEventFound: boolean = false;
  initializedModulesMap: { [key: string]: boolean } = {};
  leaderBoardConfig: { [key: string]: boolean };
  betpackBanner: boolean;
  readFSCFromCF: boolean = true;
  eagerLoadCount: IEagerLoadCMSCount;
  isNextRacesLoaded: boolean = false;
  appBuildVersion: string;
  appMenuProperties: { [key: string]: string } = {};

  protected onSocketUpdate: Function;
  protected sysConfigSubscription: Subscription;
  protected ribbonSubscription: Subscription;
  
  private readonly QUICK_LINK_MODULE = 'QuickLinkModule';
  private readonly SURFACEBET_MODULE = 'SurfaceBetModule';
  private readonly INPLAY_MODULE = 'InplayModule';
  private readonly RACING_CATEGORIES = environment.CATEGORIES_DATA.racing;
  private readonly MATCH_RESULT_MARKET_IDENTIFICATOR: string = 'MR';
  private readonly FOOTBALL_CATEGORY_ID: string = environment.CATEGORIES_DATA.footballId;
  private readonly FOOTBALL_MARKETS_TO_MODIFY: string[] = ['To Qualify', 'Penalty Shoot Out Winner', 'Penalty Shoot-Out Winner'];
  private readonly FOOTBALL_MATCHES_TAB: string = '/sport/football/matches';
  private detectListener: number;
  private isLoaderShown: boolean = true;
  private isDisplayRpg: boolean = true;

  /**
   * Update spinner loader flag of featured module (if should be shown),
   *  emit value to notify parent.
   *
   * TODO: make sure to change ssDown and isConnectSucceed to actual values before changing showLoader
   *  or refactor flags logic
   *
   * @param showLoader
   */
  set showLoader(showLoader: boolean) {
    const isShown = showLoader && !this.ssDown && this.isConnectSucceed;

    this.isLoaderShown = isShown;
    this.changeDetectorRef.markForCheck();
    this.windowRef.nativeWindow.setTimeout(() => {
      if (this.sportId && !isShown && this.featuredModuleData.modules.length) {
        this.featuredEventsCount.emit(this.getFeaturedEventsCount(this.featuredModuleData.modules));
      }

      this.isLoadedEvent.emit(!isShown);
    });
  }

  get showLoader() {
    return this.shouldDisplayLoader && this.isLoaderShown;
  }
  constructor(
    protected locale: LocaleService,
    protected filtersService: FiltersService,
    protected windowRef: WindowRefService,
    protected pubsub: PubSubService,
    protected featuredModuleService: FeaturedModuleService,
    protected templateService: TemplateService,
    protected commentsService: CommentsService,
    protected wsUpdateEventService: WsUpdateEventService,
    protected sportEventHelper: SportEventHelperService,
    protected cmsService: CmsService,
    protected promotionsService: PromotionsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected routingHelperService: RoutingHelperService,
    public router: Router,
    public gtmService: GtmService,
    protected awsService: AWSFirehoseService,
    public user: UserService,
    public eventService: EventService,
    protected virtualSharedService: VirtualSharedService,
    protected bonusSuppressionService: BonusSuppressionService,
    protected deviceService: DeviceService,
    protected storage: StorageService
  ) {
    // for callbacks - to keep context and use same reference
    this.onSocketUpdate = (data: IOutputModule) => {
      this.featureTabOnSocketUpdate(data);
    };

    this.trackByModules = this.trackByModules.bind(this);

  }

  ngOnInit(): void {
    this.betpackBanner = (this.user.status && this.bonusSuppressionService.checkIfYellowFlagDisabled(rgyellow.BET_BUNDLES)) || (!this.user.status);    
    this.changeDetectorRef.detectChanges();
    this.sysConfigSubscription = this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        this.eagerLoadCount = config['EagerLoadImagesNumber'];
        this.leaderBoardConfig = config['FiveASideLeaderBoardWidget'];
        this.isYourcallInCmsEnabled = config.YourCallIconsAndTabs.enableIcon === true;
        this.isSportsQuickLinksEnabled = config['Sport Quick Links'] && config['Sport Quick Links'].enabled === true;
        this.isHighlightCarouselEnabled = config['Highlight Carousel'] && config['Highlight Carousel'].enabled === true;
        this.isInplayModuleEnabled = config['Inplay Module'] && config['Inplay Module'].enabled === true;
        this.isFanzoneConfigEnabled = config['Fanzone'] && config['Fanzone'].enabled === true;
        this.isBetpackConfigEnabled = config['BetPack'] && config['BetPack'].enableBetPack === true;
        this.readFSCFromCF = !(config['UseFSCCached'] && config['UseFSCCached'].enabled === false);
        this.changeDetectorRef.detectChanges();
        this.appMenuProperties = config.GamingEnabled;

        this.wsUpdateEventService.subscribe();
        this.featuredModuleData = this.getInitStateOfFeatured();
        this.fetchSurfaceBets();
        this.raceGridRaces = { data: null };
        this.isConnectSucceed = true;
        this.showLoader = true;
        this.changeDetectorRef.markForCheck();
        this.pubsub.subscribe('featuredModule', this.pubsub.API.FEATURED_CONNECT_STATUS, (isConnected: boolean) => {
          this.checkIfTheUserIsSegmented();
          this.isConnectSucceed = isConnected;
          this.showLoader = !isConnected;
          this.trackErrorMessage();
          if (isConnected) {
            this.featuredModuleService.addEventListener('FEATURED_STRUCTURE_CHANGED', (featured: IFeaturedModel) => {
              if (performance.mark) {
                performance.mark(PERFORMANCE_API_MARK.TTI);
              }
              this.sortAndFormFeaturedData(featured);
              this.featuredModuleService.trackDataReceived(featured, 'FEATURED_STRUCTURE_CHANGED');

              this.init(featured);
              this.pubsub.publish(this.pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
              this.changeDetectorRef.detectChanges();
            });
          }
          this.changeDetectorRef.markForCheck();
        });

        const connectionNameSpaceId = this.hubIndex ? this.hubIndex : this.sportId;
        const connectionType = this.hubIndex ? 'eventhub' : 'sport';

       
        if (this.readFSCFromCF) {
          this.cmsService.getFSC((this.hubIndex ? 'h' : '') + connectionNameSpaceId)
            .subscribe((featured: IFeaturedModel) => {
              this.processFSCContent(featured, connectionNameSpaceId, connectionType);
            },
              (error) => {
                const featured: IFeaturedModel = {
                  'modules': [],
                  directiveName: '',
                  showTabOn: '',
                  title: '',
                  visible: false
                };
                this.processFSCContent(featured, connectionNameSpaceId, connectionType);
              });
        } else {
          this.featuredModuleService.startConnection(connectionNameSpaceId, connectionType);
          this.addErrorHandler();
        }

        const appVersion = this.storage.get('appBuildVersion');
        this.handleDisplayRPG(appVersion);

        this.pubsub.subscribe('featuredModule', this.pubsub.API.NAMESPACE_ERROR, () => {
          this.handleErrorOnFirstLoad();
        });

        this.pubsub.subscribe('featuredModule', this.pubsub.API.WS_EVENT_UPDATED, () => {
          this.changeDetectorRef.detectChanges();
        });

        this.pubsub.subscribe('featuredModuleEventHub', this.pubsub.API.WS_EVENT_UPDATE, () => {
          this.changeDetectorRef.detectChanges();
        });

        this.pubsub.subscribe('featuredModule', this.pubsub.API.WS_EVENT_UPDATED, () => {
          this.changeDetectorRef.detectChanges();
        });

        this.pubsub.subscribe('featuredModuleEventHub', this.pubsub.API.WS_EVENT_UPDATE, () => {
          this.changeDetectorRef.detectChanges();
        });
        
        this.changeDetectorRef.markForCheck();
      });

      this.pubsub.subscribe('featuredModule', [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SUCCESSFUL_LOGIN], () => {
          this.betpackBanner = this.bonusSuppressionService.checkIfYellowFlagDisabled(rgyellow.BET_BUNDLES);
          this.changeDetectorRef.detectChanges();
      });
    this.pubsub.subscribe('featuredModule', this.pubsub.API.APP_BUILD_VERSION, (appBuildVersion: string) => {
      this.storage.set('appBuildVersion', appBuildVersion);
      this.handleDisplayRPG(appBuildVersion);

    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.fetchSurfaceBets();
  }

  processFSCContent(featured: IFeaturedModel, connectionNameSpaceId: number, connectionType: string){
    performance.mark(PERFORMANCE_API_MARK.TTI);   
    this.sortAndFormFeaturedData(featured);
    this.featuredModuleService.trackDataReceived(featured, 'FEATURED_STRUCTURE_CHANGED');
    this.init(featured); 
    this.featuredModuleService.startConnection(connectionNameSpaceId, connectionType);
    this.addErrorHandler();
    this.isConnectSucceed = true;
    this.showLoader = false;    
    this.pubsub.publish(this.pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
    this.changeDetectorRef.detectChanges();
    this.changeDetectorRef.markForCheck();
  }

  private addErrorHandler() {
    this.featuredModuleService.onError(() => {
      this.featuredModuleData = this.getInitStateOfFeatured();
      this.fetchSurfaceBets();
      this.ssDown = true;
      this.showLoader = false;
      this.trackErrorMessage();
    });
  }

  isFeaturedUrl(url: string): boolean {
    return url === '/' || url === '/home/featured';
  }

  checkIfTheUserIsSegmented() {
    this.user.username && this.featuredModuleService.segmentReceivedListner();
  }

  sortAndFormFeaturedData(featured: IFeaturedModel) {
      featured['modules'].sort((a: IOutputModule, b: IOutputModule) => a.segmentOrder - b.segmentOrder);
      featured['modules'].forEach((sortedData: IOutputModule) => {
        if ([this.SURFACEBET_MODULE, this.QUICK_LINK_MODULE, this.INPLAY_MODULE].includes(sortedData['@type'])) {
          this.moduleDataSort(sortedData,featured.segmented);
        }
      });
  }

  moduleDataSort(moduleData: IOutputModule, isHomePage: boolean) {
    if(isHomePage) {
      moduleData.data.sort((a: ISportEvent & ISportSegment & IRpgConfig, b: ISportEvent & ISportSegment & IRpgConfig) => a.segmentOrder - b.segmentOrder);
    } else {
      moduleData.data.sort((a: ISportEvent & ISportSegment & IRpgConfig, b: ISportEvent & ISportSegment & IRpgConfig) => a.displayOrder - b.displayOrder);
    }
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe('featuredModule');
    this.pubsub.unsubscribe('featuredModuleEventHub');
    this.featuredModuleService.clearSubscribedFeaturedTabModules();
    this.featuredModuleService.disconnect();
    this.featuredModuleService.cacheEvents(this.featuredModuleData);
    this.windowRef.nativeWindow.clearInterval(this.detectListener);

    this.sysConfigSubscription && this.sysConfigSubscription.unsubscribe();
    this.ribbonSubscription && this.ribbonSubscription.unsubscribe();
  }

  oddsCardHeaderInitialized(moduleId: string): void {
    if (!moduleId) {
      return;
    }
    this.initializedModulesMap[moduleId] = true;
  }

  reloadComponent(): void {
    this.featuredModuleService.reconnect();
    this.ssDown = false;
    this.isConnectSucceed = true;
    this.showLoader = true;
    this.changeDetectorRef.markForCheck();
  }

  isOutright(module: IOutputModule): boolean {
    const event = module.data[0];

    if (!event || !module.dataSelection || module.dataSelection.selectionType !== 'Market') { return false; }

    // Checks if event - OutRight.
    let sortCodeList;
    if (OUTRIGHTS_CONFIG.outrightsSports.indexOf(event.categoryCode) !== -1) {
      sortCodeList = OUTRIGHTS_CONFIG.outrightsSportSortCode;
    } else {
      sortCodeList = OUTRIGHTS_CONFIG.sportSortCode;
    }

    return sortCodeList.indexOf(event.eventSortCode) !== -1 && event.markets.length > 0;
  }

  isWoEw(module: IOutputModule): boolean {
    return module.dataSelection && module.dataSelection.selectionType === 'Market' &&
      module.data[0] && module.data[0].markets[0] &&
      module.data[0].markets[0].templateMarketName.toLowerCase() === 'win or each way';
  }

  trackByModules(i: number, module: IOutputModule): string {
    const isHorceRace = (module.dataSelection && module.dataSelection.selectionType === 'RaceTypeId');
    const isByMarketId = (module.dataSelection && module.dataSelection.selectionType === 'Market');

    let trackValue = `${i}_${module._id}`;

    if (module['@type'] === 'EventsModule' && !isHorceRace && !isByMarketId) {
      trackValue = `${trackValue}_${module.title}_${module.displayOrder}`;
    }

    return trackValue;
  }

  trackByModuleData(i: number, event: ISportEvent): string {
    return `${i}_${event.id}_${event.name}_${event.startTime}`;
  }

  /**
   * Check if to show module
   * @param {Object} module - featured module
   * @returns {boolean}
   */
  isModuleHidden(module: IOutputModule): boolean {
    return !(module.isLoaded && module.data.length === 0);
  }

  seeAllRaces(module: IOutputModule): void {
    const isVirtual = this.virtualSharedService.isVirtual(module.categoryId);

    const categoryId = module && module.categoryId,
      racingName = Object.keys(this.RACING_CATEGORIES)
        .filter(name => this.RACING_CATEGORIES[name].id === categoryId)[0] || '';

    if (racingName) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'featured module',
        eventAction: 'featured races',
        eventLabel: 'see all',
        sportName: racingName
      });

      if (isVirtual) {
        const classId = module.data.length && module.data[0].classId;
        const url = this.virtualSharedService.formVirtualTypeUrl(classId);
        this.router.navigateByUrl(url);
      } else {
        this.routingHelperService.formSportUrl(racingName).subscribe(url => this.router.navigateByUrl(url));
      }
    }
  }

    /**
   * Check for deviceType(IOS) and calls for buildVersion
   * @params {string}
   * @returns {void}
   */
  private handleDisplayRPG(appVersionIos: string) {
    if (this.deviceService.isWrapper && this.deviceService.isIos && this.appMenuProperties.iosVersionBlackList &&
      appVersionIos && this.appMenuProperties.iosVersionBlackList.includes(appVersionIos)) {
      this.isDisplayRpg = false;
    }
  }

  /**
   * Check if to show no events message
   * @returns {boolean}
   */
  checkNoEventFound(): boolean {
    const moduleData = this.featuredModuleData.modules;
    const moduleDataLength = moduleData && _.filter(moduleData, (mod: IOutputModule) => mod.isLoaded && mod.data.length === 0).length;
    const isDataNotExist = (moduleData && moduleData.length) === moduleDataLength;
    return isDataNotExist && !this.showLoader && !this.ssDown && this.isConnectSucceed;
    // TODO does this ^^ logic with showLoader (and it's setter) still make sense..?
  }

  /**
   * Check if to show odds-card-header
   * @param {Object} module - featured module
   * @returns {boolean}
   */
  isOddsCardHeaderShown(module: IOutputModule): boolean {
    return !this.isRace(module).racing && module.dataSelection.selectionType !== 'Enhanced Multiples';
  }

  /**
   * Get module data and subscribe to updates
   * @param {Object} module
   * @param {Boolean} isExpanded
   */
  manageSocketSubscription(module: IOutputModule, isExpanded: boolean): void {
    module.showExpanded = isExpanded;
    if (!module.data.length && module.dataSelection.selectionType !== 'RacingGrid') {
      module.showModuleLoader = true;
      const moduleId: string = this.featuredModuleService.checkEventModuleAndReturnValue(module);
      this.getDataAndSubscribe(moduleId);
      this.featuredModuleService.addModuleToSubscribedFeaturedTabModules(moduleId);
    }
  }

  // Update the view for feature Module

  updateFeatureModuleView() {
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Returns event type
   * @param event
   * @returns {string}
   */
  getEventType(event: ISportEvent): string {
    return this.sportEventHelper.isSpecialEvent(event, true) ? 'specials' : '';
  }

  /**
   * @description Get 'Show More' link text
   * @param {object} module from featuredModuleData
   * @returns {string}
   */
  getShowMoreText(module: IOutputModule): string {
    const isNotLinkText = !module.footerLink.text && module.totalEvents;
    const linkText = `${this.locale.getString('sb.viewAll')} ${module.totalEvents} ${module.title} ${this.locale.getString('sb.events')}`;
    return isNotLinkText ? linkText : module.footerLink.text;
  }

  /**
   * On click yourcall icon action
   * @param event
   */
  yourCallAction(event: MouseEvent | TouchEvent): void {
    event.stopPropagation();
    this.promotionsService.openPromotionDialog('YOUR_CALL');
  }

  /**
   * @description Check if it is Race Module
   * @param {object} module from featuredModuleData
   * @returns {{racingGrid: boolean, racingCard: boolean, racing: boolean}}
   */
  isRace(module): { racingGrid: boolean; racingCard: boolean; racing: boolean } {
    const selection = module.dataSelection.selectionType;
    return {
      racingGrid: selection === 'RacingGrid',
      racingCard: selection === 'RaceTypeId',
      racing: selection === 'RaceTypeId' || selection === 'RacingGrid'
    };
  }

  /**
   * Operations on module update receiving
   * @param {Object} data
   */
  onModuleUpdate(data: IOutputModule): void {
    if (!data._id) {
      return;
    }
    !this.isSimpleModule(data) && this.templateService.setCorrectPriceType(data.data, true);
    if (([this.SURFACEBET_MODULE, this.QUICK_LINK_MODULE].includes(data['@type']))) {
      this.moduleDataSort(data,data.segmented);
    }
    this.badges[data._id] = this.getBadge(data);

    this.featuredModuleData.modules = this.featuredModuleData.modules.map(module => {
      if (module._id === data._id) {
        data.showExpanded = true;
        data.showModuleLoader = false;
        (data.data as ISportEvent[]) = this.addClockToModule(data.data);
        // Adapt comments data for UI templates(badminton sport)
        this.updateCommentsDataFormat(data.data);
        data.isOutright = this.isOutright(data);
        data.isWoEw = this.isWoEw(data);
        this.modifyFootballMainMarkets(data);

        return data;
      }
      return module;
    });
    this.featuredModuleService.cacheEvents(this.featuredModuleData);
    this.isModuleAvailable = (data['@type'] === 'SurfaceBetModule' && data.data.length > 0) || this.featuredModuleData.modules.filter((module: IOutputModule) => module['@type'] === 'EventsModule').length > 0;
    this.fetchSurfaceBets();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Function is responsible for initialization of featuredModule
   *
   * @param {Object} featured
   */
  init(featured: IFeaturedModel): void {
    let data = featured;
    this.isNextRacesLoaded = true;

    if (!data || (data && data.modules && data.modules.length === 0)) {
      this.handleErrorOnFirstLoad(false);
      if (data && data.modules) {
        this.featuredModuleData.modules = data.modules;
        this.fetchSurfaceBets();
      }
      this.noEventFound = this.checkNoEventFound();
      return;
    } else if (data && data.modules && data.modules.length > 0) {
      this.noEventFound = false;
    }

    if (!this.featuredModuleService.tabModuleStates.size) {
      data.modules.forEach((module: IOutputModule) => {
        this.featuredModuleService.tabModuleStates.set(module._id, module.showExpanded);
      });
    }

    // listeners for updates of modules
    this.addModulesEventListeners(data);
    // listeners for updates of events in each module
    this.addEventListenersForEventsInModules(data);

    const currentDeviceTypes = [];
    _.each(this.windowRef.nativeWindow.view, (device: string, key: string) => {
      if (device) {
        currentDeviceTypes.push(key.toLowerCase().indexOf('tablet') !== -1 ? 'tablet' : key);
      }
    });


    data.modules = _.filter(data.modules, (module: IOutputModule) => {
      return module.publishedDevices.length === 0 || _.intersection(currentDeviceTypes, module.publishedDevices).length > 0;
    }).map((module: IOutputModule) => {
      module.isOutright = this.isOutright(module);
      module.isWoEw = this.isWoEw(module);

      if (module['@type'] === 'EventsModule') {
        (module.data as ISportEvent[]) = this.filtersService.orderBy(module.data as ISportEvent[], ['displayOrder', 'startTime', 'name']);
        this.templateService.setCorrectPriceType(module.data, true);
        module.isLoaded = this.isRace(module).racingGrid ? false : module.showExpanded;
        this.modifyFootballMainMarkets(module);
        this.defineHRsilksType(module);

        // Adapt comments data(if exists) for UI templates(badminton sport)
        this.updateCommentsDataFormat(module.data);
      }

      if (this.isHighLIghtCarouselModule(module)) {
        this.updateCommentsDataFormat(module.data);
      }

      this.updateCommentsInplayModule(module);
      return module;
    });

    if (this.featuredModuleData) {
      data.modules = this.merge(data.modules);
    } else {
      data = this.addClockToEvents(data);
    }

    // subscription and listeners for modules that were expanded manually
    this.resubscribeToManuallyExpandedModules();

    this.saveState(data);
    this.ssDown = false;
    this.showLoader = false;
    this.featuredModuleData = data;
    this.changeDetectorRef.markForCheck();
    this.badges = this.getBadges(data.modules);
    this.featuredModuleService.cacheEvents(this.featuredModuleData);
    const modules = _.filter(data.modules, (module: IOutputModule) => {
      return !this.isSurfaceBetsModule(module) || (this.isSurfaceBetsModule(module) && module.data.length > 0)
    });
    this.isModuleAvailable = this.isFeaturedModuleAvailable && modules.length > 0;
    this.fetchSurfaceBets();
  }

  /**
   * Function is responsible for running detectChanges on lazy-child component load
   */
  childComponentLoaded(): void {
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Function decides whether to show RpgModule or Not
   * @param {IOutputModule} outputModule
   * @returns {boolean}
   */
  showRpg(outputModule: IOutputModule): boolean {
    return this.isDisplayRpg && this.user && this.user.status && this.isFeaturedUrl(this.router.url.split('?')[0])
      && outputModule['@type'] === 'RecentlyPlayedGameModule';
  }

  /**
   * To show Leaderboard widget based on CMS Configuration
   * @param {string} url
   * @returns {boolean}
   */
  showLeaderboardWidget(url: string): boolean {
    let showLeaderboardWidget: boolean = false;
    const [baseURL] = url.split('?');
    if (this.isFeaturedUrl(baseURL) && this.leaderBoardConfig) {
      showLeaderboardWidget = this.leaderBoardConfig.homePage;
    } else if (baseURL === this.FOOTBALL_MATCHES_TAB && this.leaderBoardConfig) {
      showLeaderboardWidget = this.leaderBoardConfig.footballPage;
    }
    return showLeaderboardWidget;
  }

  /**
   * To show freeRide banner on homepage only
   * @param {string} url
   * @returns {boolean}
   */
  showFreeRideBanner(url: string): boolean {
    const [baseURL] = url.split('?');
    return this.isFeaturedUrl(baseURL);
  }

  handleErrorOnFirstLoad(ssDown: boolean = true): void {
    if (this.router.url === '/' && !this.routingHelperService.getPreviousSegment().includes('/home/')) {
      this.ribbonSubscription = this.cmsService.getRibbonModule().subscribe((data: { getRibbonModule }) => {
        const index = data.getRibbonModule.findIndex((item) => this.isFeaturedUrl(item.url)) + 1;
        const url = data.getRibbonModule[index].url;
        this.router.navigateByUrl(url);
      });
    } else {
      this.ssDown = ssDown;
      this.showLoader = false;
      this.changeDetectorRef.markForCheck();
      this.trackErrorMessage();
    }
  }

  /**
   * Handles new module data received from websocket updates.
   * @param {Object=} data
   */
  protected featureTabOnSocketUpdate(data?: IOutputModule): void {
    const module = data || this.getCleanModule();
    module.isLoaded = true;

    if (module.footerLink && module.footerLink.url) {
      module.footerLink.url = module.footerLink.url.replace(/(^\w+:|^)\/\//, '');
    }

    if (this.isInplayModule(module)) {
      this.onInplayModuleUpdate(module);
    } else {
      this.onModuleUpdate(module);
      this.addEventListenersWithinModule(module);
      if (!this.isSimpleModule(module) && !this.isSurfaceBetsModule(module)) {
        this.unsubscribe(module._id);
        const moduleId = this.featuredModuleService.checkEventModuleAndReturnValue(module);
        if (moduleId !== module._id) this.unsubscribe(moduleId);
      }
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Check if featured module is available
   * @returns {boolean}
   */
  get isFeaturedModuleAvailable(): boolean {
    return this.featuredModuleData && this.featuredModuleData.modules && this.featuredModuleData.modules.length > 0;
  }
  set isFeaturedModuleAvailable(value: boolean) { }
  protected getInitStateOfFeatured(): IFeaturedModel {
    return {
      directiveName: null,
      modules: [],
      showTabOn: null,
      title: null,
      visible: null
    };
  }

  /**
   * Check if module is Rpg or Quick Links
   * @param module
   * @returns {boolean}
   */
  protected isSimpleModule(module): boolean {
    return ['RecentlyPlayedGameModule', 'QuickLinkModule', 'AEM_BANNERS'].includes(module['@type']);
  }

  private getFeaturedEventsCount(modules: IOutputModule[]): number {
    let eventsCount = 0;

    const filters = [this.isSurfaceBetsModule];

    if (this.isInplayModuleEnabled) {
      filters.push(this.isInplayModule);
    }

    if (this.isHighlightCarouselEnabled) {
      filters.push(this.isHighLIghtCarouselModule);
    }

    modules.forEach((module: IOutputModule) => {
      if (filters.some((filter: Function) => filter(module))) {
        eventsCount += {}.hasOwnProperty.call(module, 'totalEvents') ? module.totalEvents : module.data.length;
      }
    });

    return eventsCount;
  }

  /**
   * Subscribe to updates
   * @param {String} _id
   */
  private getDataAndSubscribe(_id: string): void {
    this.featuredModuleService.addEventListener(_id, this.onSocketUpdate);
    this.featuredModuleService.emit('subscribe', _id);
    this.featuredModuleService.tabModuleStates.set(_id, true);
  }

  /**
   * Get badges object for all modules
   * @param {Array} modules
   * returns {Object}
   */
  private getBadges(modules: IOutputModule[]): { [key: string]: IBadgeModel } {
    const badges = {};
    _.each(modules, (module: IOutputModule) => (badges[module._id] = this.getBadge(module)));
    return badges;
  }

  /**
   * Get badge object for single module
   * @param {Object} module
   * returns {(Object|undefined)}
   */
  private getBadge(module: IOutputModule): IBadgeModel {
    switch (true) {
      case module.isEnhanced:
        return { label: 'Enhanced', className: 'pc-badge--enhanced' };
      case module.isSpecial:
        return { label: 'Special', className: 'pc-badge--specials' };
      default:
        return undefined;
    }
  }

  /**
   * Update comments data format(adapt for UI templates)
   * @param events - events list
   * @private
   */
  private updateCommentsDataFormat(events: ISportEvent[]): void {
    if (events.length) {
      _.each(events, (event: ISportEvent) => {
        if (event.categoryCode) {
          const methodName = `${event.categoryCode.toLowerCase()}MSInitParse`,
            updater = this.commentsService[methodName];

          if (event.comments && updater) {
            updater(event.comments);
          }
        }
      });
    }
  }

  /**
   * Function handle state (collapsed/expanded) of module
   * @param {Object} data
   */
  private saveState(data: IFeaturedModel): void {
    data.modules.forEach((module: IOutputModule) => {
      module.showModuleLoader = false;

      if (this.featuredModuleService.tabModuleStates.has(module._id) || !this.featuredModuleData) {
        return;
      }

      const fModule = _.find(this.featuredModuleData.modules, mod => mod._id === module._id);

      if (!fModule) {
        module.showExpanded = this.featuredModuleService.tabModuleStates.get(module._id) || module.showExpanded;
      }
    });
  }

  /**
   * Add clock data for all modules events
   * @param {Object} data
   * returns {Object}
   */
  private addClockToEvents(data: IFeaturedModel): IFeaturedModel {
    data.modules = data.modules.map((module: IOutputModule) => {
      (module.data as ISportEvent[]) = this.featuredModuleService.addClock(module.data);
      return module;
    });

    return data;
  }

  /**
   * Returns data for featuredModuleData property
   * if it is one of modules that was expanded manually we assigns old data until it will be updated
   * by module socket message
   * if it is another app just updates this module
   * @param modules
   * @return {Array}
   */
  private merge(modules: IOutputModule[]): IOutputModule[] {
    return modules.map(module => {
      const isOldManuallyExpandedModule = _.some(this.featuredModuleService.getSubscribedFeaturedTabModules(),
        modId => modId === module._id);
      const existingModule = _.find(this.featuredModuleData.modules, (mod: IOutputModule) => mod._id === module._id);

      if (existingModule && existingModule.showExpanded && !module.showExpanded) {
        module.showExpanded = true;
      }

      if (existingModule && !existingModule.showExpanded) {
        module.showExpanded = false;
      }
      if (existingModule && existingModule.dataSelection && existingModule.dataSelection.selectionType === 'RaceTypeId') {
        return existingModule;
      } else if (module.showExpanded && isOldManuallyExpandedModule && existingModule) {
        module.data = existingModule.data;
      } else {
        (module.data as ISportEvent[]) = this.addClockToModule(module.data);
      }
      module.isOutright = this.isOutright(module);

      return module;
    });
  }

  /**
   * Add clock data
   * @param {Array} data
   * returns {Array}
   */
  private addClockToModule(data: ISportEvent[]): ISportEvent[] {
    return this.featuredModuleService.addClock(data);
  }

  /**
   * HR: To define silks type on UK/IRE or International events
   * @param {{}} module - featured module
   */
  private defineHRsilksType(module: IOutputModule): void {
    module.data.forEach((el: ISportEvent) => {
      if (el.categoryCode === 'HORSE_RACING') {
        el.isUKorIRE = this.eventService.isUKorIRE(el);
      }
    });
  }

  /**
   * Football To qualify and Penalty markets have "home/away" type,
   * but we need to show all sections with "home/draw/away" odds card header.
   * thats why we need to emulate MatchResult market.
   * @param {{}} module - featured module
   */
  private modifyFootballMainMarkets(module: IOutputModule): void {
    if (module.data) {
      _.forEach(module.data, (event: ISportEvent) => {
        this.modifyMarket(event);
      });
    }
  }

  /**
   * Football To qualify and Penalty markets have "home/away" type,
   * but we need to show all sections with "home/draw/away" odds card header.
   * thats why we need to emulate MatchResult market.
   * @param {ISportEvent} event
   */
  private modifyMarket(event: ISportEvent): void {
    if (event.categoryId === this.FOOTBALL_CATEGORY_ID && event.markets.length > 0) {
      // each event has only one market
      const market = event.markets[0];

      if (market && _.contains(this.FOOTBALL_MARKETS_TO_MODIFY, market.templateMarketName)) {
        market.marketMeaningMinorCode = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
        market.dispSortName = this.MATCH_RESULT_MARKET_IDENTIFICATOR;
      }
    }
  }

  /**
   * Check if module is inplay
   * @param module
   * @returns {boolean}
   */
  private isInplayModule(module): boolean {
    return module['@type'] === 'InplayModule';
  }

  /**
   * Check if module is Surface Bets
   * @param module
   * @returns {boolean}
   */
  private isSurfaceBetsModule(module): boolean {
    return module['@type'] === 'SurfaceBetModule';
  }

  /**
   * Check if module is HighLightCarousel
   * @param module
   * @returns {boolean}
   */
  private isHighLIghtCarouselModule(module): boolean {
    return module['@type'] === 'HighlightCarouselModule';
  }

  /**
   * Goes through each module
   * @param data {Object}
   */
  private addEventListenersForEventsInModules(data: IFeaturedModel): void {
    _.each(data.modules, (module: IOutputModule) => {
      if (this.isInplayModule(module)) {
        const events = this.getEventsFromInplayModule(module);
        this.addEventsLiveUpdatesListener(events);
        this.featuredModuleService.addClock(events);
      } else {
        this.addEventListenersWithinModule(module);
      }
    });
  }

  /**
   * Returns all events from inplay module (required for live updates)
   * @param {IOutputModule} module
   * @returns {ISportEvent[]}
   */
  private getEventsFromInplayModule(module: IOutputModule): ISportEvent[] {
    const events = [];
    _.each(module.data, (sportSegment: ISportSegment) => {
      _.each(sportSegment.eventsByTypeName, (type: ITypeSegment) => {
        _.each(type.events, (event: ISportEvent) => {
          this.modifyMarket(event);
          events.push(event);
        });
      });
    });
    return events;
  }
  /**
   * Goes trough each event in module and sets callback for event updates
   * @param module {Array}
   */
  private addEventListenersWithinModule(module: IOutputModule): void {
    this.addEventsLiveUpdatesListener(module.data);
  }

  /**
   * Live updates handler
   * @param {ISportEvent[]} events
   */
  private addEventsLiveUpdatesListener(events: ISportEvent[]): void {
    _.each(events, (event: ISportEvent) => {
      if (event.id) {
        this.featuredModuleService.addEventListener(event.id.toString(), update => {
          this.pubsub.publish(this.pubsub.API.WS_EVENT_UPDATE, {
            events: [event],
            update
          });
        });
      }
    });
  }

  /**
   * Function returns featured modules ids
   * @param {Array} modules
   */
  private getModuleIds(modules: IOutputModule[]): string[] {
    return modules
      .filter(module => module.showExpanded)
      .map(module => module._id);
  }

  /**
   * Function adds socket event listener and handler
   * @param {Object} data
   */
  private addModulesEventListeners(data: IFeaturedModel): void {
    this.getModuleIds(data.modules)
      .forEach(id => this.featuredModuleService.addEventListener(id, this.onSocketUpdate));
  }

  /**
   * Resubscribes to manually expanded modules and reassigns listeners
   */
  private resubscribeToManuallyExpandedModules(): void {
    // manually subscribed featured modules
    const moduleIds: string[] = this.featuredModuleService.getSubscribedFeaturedTabModules();

    this.featuredModuleService.removeAllListeners(moduleIds);
    _.each(moduleIds, (item: string) => {
      this.featuredModuleService.emit('unsubscribe', [item]);

      this.featuredModuleService.emit('subscribe', item);
      this.featuredModuleService.addEventListener(item, this.onSocketUpdate);
    });
  }

  /**
   * Inplay module handler
   * @param module Inplay module update listener
   */
  private onInplayModuleUpdate(module: IOutputModule): void {
    this.featuredModuleData.modules = this.featuredModuleData.modules.map(currentModule => {
      if (currentModule._id === module._id) {
        this.updateInPlayCounter(currentModule, module);
      }
      return currentModule;
    });
    this.fetchSurfaceBets();
  }
  /**
   * Updates total events counter
   */
  private updateInPlayCounter(module: IOutputModule, newModule: IOutputModule): void {
    module.totalEvents = newModule.totalEvents;
    this.changeDetectorRef.markForCheck();
  }

  private getCleanModule(): IOutputModule {
    return {
      _id: null,
      title: null,
      displayOrder: null,
      showExpanded: null,
      maxRows: null,
      maxSelections: null,
      totalEvents: null,
      publishedDevices: [],
      data: [],
      dataSelection: null,
      footerLink: {
      },
      cashoutAvail: null,
      hasNoLiveEvents: null,
      outcomeColumnsTitles: [],
      errorMessage: null,
      special: null,
      enhanced: null,
      yourCallAvailable: null
    };
  }

  /**
   * Unsubscribe from updates
   * @param {String} _id
   */
  private unsubscribe(_id: string): void {
    this.featuredModuleService.tabModuleStates.set(_id, false);
    this.featuredModuleService.removeEventListener(_id, this.onSocketUpdate);
    this.featuredModuleService.emit('unsubscribe', [_id]);
  }

  /**
   * Track UI Message Service is unavailable
   */
  private trackErrorMessage(): void {
    if (this.sportId === 0 && (this.ssDown || !this.isConnectSucceed)) {
      this.awsService.addAction(`featured=>UI_Message=>Unavailable=>${this.ssDown ? 'ssError' : 'wsError'}`);
    }
  }

  /**
   * Adapt comments data for inplay module (for badminton)
   * @param module IOutputModule
   */
  private updateCommentsInplayModule(module: IOutputModule): void {
    if (this.isInplayModule(module)) {
      module.data.forEach((sportSegment: ISportSegment) => {
        sportSegment.eventsByTypeName.forEach((typeSegment: ITypeSegment) => {
          this.updateCommentsDataFormat(typeSegment.events);
        });
      });
    }
  }

  fetchSurfaceBets(): void {
    if (this.featuredModuleData) {
      if (this.showOnlyBigCompetitionData) {
        if (this.featuredModuleData && this.featuredModuleData.modules.length > 0) {
          const filteredData = this.featuredModuleData.modules.filter(module => {
            if (module['@type'] === 'SurfaceBetModule' && this.surfaceBetIds) {
              module.data = module.data.filter(obj => {
                if (this.surfaceBetIds.indexOf(obj.objId) !== -1) {
                  return obj;
                }
              });
              if (module.data.length) {
                return module;
              }
            }
            if (module['@type'] === 'HighlightCarouselModule' && this.highlightCarouselIds) {
              if (this.highlightCarouselIds.indexOf(module._id) !== -1) {
                module.Participants = this.participants;
                return module;
              }
            }
          });
          this.featuredModuleData.modules = filteredData;
          this.changeDetectorRef.detectChanges();
        }
      }
    }
  }
}