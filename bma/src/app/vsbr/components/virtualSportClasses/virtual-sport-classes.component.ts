import { from as observableFrom, of, Subscription } from 'rxjs';
import { catchError, concatMap } from 'rxjs/operators';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { DatePipe } from '@angular/common';
import { Component, OnInit, OnDestroy, ChangeDetectorRef, Input, ViewChild, ElementRef } from '@angular/core';
import * as _ from 'underscore';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { PanelStateService } from '../../services/panel-state.service';
import { VirtualSportsService } from '../../services/virtual-sports.service';

import {
  forecastFilter,
  MARKETS_CONFIG, tricastFilter, verticalTemplateName,
  VIRTUAL_ROUTE_NAME, winEwFilter, winEwTemplateName
} from '@app/vsbr/constants/virtual-sports.constant';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IMarketEntity } from '@core/models/market-entity.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { VirtualMenuDataService } from '@app/vsbr/services/virtual-menu-data.service';
import { ICategoryAliases, IVirtualChildCategory } from '@app/vsbr/models/virtual-sports-structure.model';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IMarketsConfig } from '@app/vsbr/models/virtual-sports-config.model';
import { VirtualSportsMapperService } from '@app/vsbr/services/virtual-sports-mapper.service';
import { IAutoSeoData } from '@app/core/services/cms/models/seo/seo-page.model';
import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { IOutcome } from '@root/app/core/models/outcome.model';
import { SbFiltersService } from '@app/sb/services/sbFilters/sb-filters.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { LocaleService } from '@core/services/locale/locale.service';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import environment from '@environment/oxygenEnvConfig';
import {
  IPerformGroupConfig,
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { PerformGroupService } from '@lazy-modules/eventVideoStream/services/performGroup/perform-group.service';
import { NEXT_RACES_HOME_CONSTANTS } from '@app/lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';

@Component({
  selector: 'virtual-sport-classes',
  styleUrls: ['./virtual-sport-classes.scss'],
  templateUrl: './virtual-sport-classes.component.html'
})
export class VirtualSportClassesComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  childMenu: IVirtualSportsMenuItem[];
  eventsData: ISportEventEntity[];
  activeClass: IVirtualChildCategory;
  events: ISportEventEntity[];
  currentEventIndex: number;
  currentEvent: ISportEventEntity;
  event: ISportEvent;
  market: IMarket;
  panelsStates: Object = {};
  sections: IMarketEntity[];
  requestedEventNotFound: boolean = false;
  terms: string = '';
  showTerms: boolean;
  hasWinOrEachWay: boolean = false;
  categoryAlias: string;
  parentCategoryAlias: string;
  categoryId: string;
  switchers: ISwitcherConfig[] = [];
  activeChild: number;
  ctaText: string;
  ctaUrl: string;
  navigatedFromEventId: string;
  isDesktop: boolean = this.deviceService.isDesktop;

  filter: string = winEwFilter;
  forecastFilter: string = forecastFilter;
  tricastFilter: string = tricastFilter;
  MARKETS_CONFIG: IMarketsConfig = MARKETS_CONFIG;
  expandedSummary = [];
  isWrapper: boolean = false;
  showQuantumLeap: boolean;
  isNotAntepostOrSpecials: boolean;
  isLegendsSport: boolean = false;
  isInfoHidden: {'info': boolean};
  sortOptionsEnabled: boolean = false;
  selectedMarket: string;
  toteLabel: string;
  sortBy: string = 'Price';
  isGreyhoundEdp: boolean = false;
  isRacingSpecialsCondition: boolean;
  isMarketAntepost: boolean;
  isFullScreenConfig: boolean = false;
  fullScreenDrillDownTags: string[] = [''];
  insightsDrillDownTags: string[] = [''];
  preloadStream: boolean;
  isHorseRacingScreen: boolean;
  racingName: string;
  shouldShowCSBIframe: boolean;
  performConfig: IPerformGroupConfig;
  streamControl: any;
  racingPostDataLoaded: boolean = false;
  videoStreamStarted = false;
  playerLoaded = false;
  frameWidth: number;
  frameHeight: number;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: '',
    otherProviders: 'live-column watch-live'
  };
  @Input() sportName: string;
  @Input() streamFilter: string;
  @ViewChild('nativeVideoPlayerPlaceholder', {static: true}) nativeVideoPlayerPlaceholderRef: ElementRef;
  spinner = {
    isActive: false
  };
  protected isHR: boolean;
  private autoSeoData: IAutoSeoData = { name: '' };
  private eventId: string;
  private pollingTimer: number;
  private timeOutListener;
  private intervalValue: number = 500;
  private paramsSubscriber: Subscription;

  private readonly tagName: string = 'VirtualSportClassesCtrl';

  constructor(
    private windowRef: WindowRefService,
    private filterService: FiltersService,
    private timeService: TimeService,
    private datePipe: DatePipe,
    private panelState: PanelStateService,
    private virtualSportsService: VirtualSportsService,
    private route: ActivatedRoute,
    private router: Router,
    public deviceService: DeviceService,
    private nativeBridge: NativeBridgeService,
    private pubsub: PubSubService,
    private changeDetRef: ChangeDetectorRef,
    private virtualMenuDataService: VirtualMenuDataService,
    private vsMapperService: VirtualSportsMapperService,
    private greyhoundService: GreyhoundService,
    private routingState: RoutingState,
    protected watchRulesService: WatchRulesService,
    protected horseracing: HorseracingService,
    protected sbFilters: SbFiltersService,
    protected racingPostService: RacingPostService,
    protected cmsService: CmsService,
    protected localeService: LocaleService,
    protected sortByOptionsService: SortByOptionsService,
    protected gtmService: GtmService,
    protected racingGaService: RacingGaService,
    protected performGroupService: PerformGroupService,
    public elementRef: ElementRef<HTMLElement>
  ) {
    super()/* istanbul ignore next */;
    this.sortOptionsEnabledFn = this.sortOptionsEnabledFn.bind(this);
  }

  ngOnInit(): void {
    this.addChangeDetection();
    this.init();
    this.reloadListener();
    this.isWrapper = this.deviceService.isWrapper;
    const segment = this.routingState.getCurrentSegment();
    this.isHorseRacingScreen = segment.indexOf('horseracing') >= 0;
    this.calculateVideoPlayerHeight();
  }

  ngOnDestroy(): void {
    this.timeOutListener && this.windowRef.nativeWindow.clearInterval(this.timeOutListener);
    this.pubsub.unsubscribe(this.tagName);
    this.windowRef.nativeWindow.clearInterval(this.pollingTimer);
    this.paramsSubscriber && this.paramsSubscriber.unsubscribe();
    this.virtualSportsService.unsubscribeFromUpdates();
    this.virtualSportsService.unSubscribeVSBRForUpdates();
  }

  goToCtaUrl(): void {
    this.ctaUrl = this.ctaUrl ? this.ctaUrl : '/';
    this.router.navigate([this.ctaUrl]);
  }

  trackMarketSectionById(index: number, item: { id?: string }) {
    return `${index}${item.id}`;
  }

  /**
   * Check if event ongoing
   * @returns {Boolean}
   */
  isEventOngoing(): boolean {
    return this.goToNextIfStarted(this.currentEventIndex) && !this.hasEventFinished(this.currentEventIndex);
  }

  /**
   * Set Collapsed Panel.
   * @param {String} panelId
   */
  changeStatePanel(panelId: string): void {
    this.panelState.changeStatePanel(this.currentEventIndex, panelId);
  }

  /**
   * Display active Collapsed Panel.
   * @param {String} panelId
   * @returns {Boolean}
   */
  activeStatePanel(panelId: string): boolean {
    return (this.panelsStates[this.currentEventIndex] !== undefined)
      ? this.panelsStates[this.currentEventIndex][panelId] : false;
  }

  /**
   * Get formatted event start date
   * @param {number} startDate
   * @returns {String}
   */
  getEventStartDate(startDate: number | string): string {
    return this.datePipe.transform(startDate, 'yyyy-MM-dd');
  }

  /**
   * Get formatted event start time
   * @param {number} startTime
   * @returns {String}
   */
  getEventStartTime(startTime: number | string): string {
    return this.datePipe.transform(startTime, 'HH:mm');
  }

  /**
   * Tabs panel callback
   * @param {object} tab
   */
  onTabClick({ tab }: { id: string; tab: any; }): void {
    this.goToEvent(tab.event.id.toString());
  }

  goToEvent(eventId: string) {
    this.requestedEventNotFound = false;
    this.currentEventIndex = this.events.findIndex(e => e.event.id.toString() === eventId);

    if (this.currentEventIndex < 0) {
      this.currentEventIndex = 0;
    }

    this.update();

    if (this.deviceService.isWrapper) {
      this.nativeBridge.onVirtualsSelected(this.categoryId, eventId);
    }
  }

  /**
   * Add change detection
   */
  addChangeDetection(): void {
    this.changeDetRef.detach();
    this.timeOutListener = this.windowRef.nativeWindow.setInterval(() => {
      this.changeDetRef.detectChanges();
    }, this.intervalValue);
  }

  onPlayLiveStreamError($event: { value: string }): void {
    if (this.isWrapper && !this.watchRulesService.isInactiveUser($event.value)) {
      this.streamFilter = 'hideStream';
    }
    this.videoStreamStarted = true;
  }

  /**
   * Expand/Collapse of Racing form data
   * @param  {Array<Array<boolean>>} expandedSummary
   * @param  {number} mIndex
   * @param  {number} oIndex
   * @returns void
   */
  onExpandSection(expandedSummary: Array<Array<boolean>>, mIndex: number, oIndex: number): void {
    expandedSummary[mIndex][oIndex] = !expandedSummary[mIndex][oIndex];
    const hideInfoChecker: boolean = expandedSummary[mIndex].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info': !hideInfoChecker };
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'race card',
      eventCategory: this.isGreyhoundEdp ? 'greyhounds' : 'horse racing',
      eventLabel: expandedSummary[mIndex][oIndex] ? 'show more' : 'show less',
      categoryID: this.event.categoryId,
      typeID: this.event.typeId,
      eventID: this.event.id
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Toggle function for Expand/Collapse of form data
   * @param  {Array<Array<boolean>>} expandedSummary
   * @param  {number} mIndex
   * @param  {boolean} showOption
   * @returns void
   */
  toggleShowOptions(expandedSummary: Array<Array<boolean>>, mIndex: number, showOption: boolean): void {
    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex][i] = showOption;
    }
  }

  /**
   * Sort Options Enabler function for Odds Card
   * @param  {boolean} isEW
   * @param  {boolean} checkMarket?
   * @param  {IMarket} market?
   * @returns boolean
   */
  sortOptionsEnabledFn(isEW: boolean, checkMarket?: boolean, market?: IMarket): boolean {
    const checks = isEW && this.sortOptionsEnabled && this.selectedMarket !== this.toteLabel;
    const selectedMarket = this.selectedMarket &&
      _.find(this.event.sortedMarkets, sortedMarket => sortedMarket.name === this.selectedMarket);

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

  /**
   * GA tracking handler for Expand/Collapse
   * @param  {boolean} showOption
   * @returns void
   */
  toggleShowOptionsGATracking(showOption: boolean): void {
    this.racingGaService.toggleShowOptionsGATracking(this.event, showOption, this.isGreyhoundEdp);
    const gtmData = {
      event: NEXT_RACES_HOME_CONSTANTS.TRACKEVENT,
      eventAction: NEXT_RACES_HOME_CONSTANTS.RACE_CARD,
      eventCategory: this.isGreyhoundEdp ? NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE,
      eventLabel: showOption ? NEXT_RACES_HOME_CONSTANTS.SHOW_INFO : NEXT_RACES_HOME_CONSTANTS.HIDE_INFO,
      categoryID: this.event.categoryId,
      typeID: this.event.typeId,
      eventID: this.event.id
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Check for Watch and Insights eligibility
   * @returns boolean
   */
  showWatchAndInsights(): boolean {
    const tagList = this.insightsDrillDownTags.find((tag: string) => (this.event && this.event.drilldownTagNames && this.event.drilldownTagNames.includes(tag)));
    if (tagList) {
      return this.event.isUKorIRE && this.event.categoryId === environment.HORSE_RACING_CATEGORY_ID;
    }
    return false;
  }

  /**
   * Emitter on live stream started
   * @returns void
   */
  onLiveStreamStarted(): void {
    this.videoStreamStarted = true;
  }

  /**
   * Emitter on Player loaded
   * @returns void
   */
  onPlayerLoadedStatus(): void {
    this.playerLoaded = true;
  }

  private reloadListener() {
    this.pubsub.subscribe(this.tagName, this.pubsub.API.RELOAD_COMPONENTS, () => {
      this.init();
    });
  }
  /**
   * Check if event started
   * @param {Number} eventIndex
   * @returns {Boolean}
   */
  private goToNextIfStarted(eventIndex: number): boolean {
    const currentEvent = this.events[eventIndex] && this.events[eventIndex].event;

    if (currentEvent) {
      currentEvent.isStarted = (currentEvent.startTimeUnix - Date.now() <= 0);
      if (currentEvent.isStarted && this.navigatedFromEventId !== this.events[eventIndex].id && this.events[eventIndex + 1]) {
          this.navigatedFromEventId = this.events[eventIndex].id;
          this.goToEvent(this.events[eventIndex + 1].event.id.toString());
      }
      return currentEvent.isStarted;
    }

    return false;
  }

  /**
   * check if event finished
   * @param {Number} eventIndex
   */
  private hasEventFinished(eventIndex: number): boolean {
    return this.events[eventIndex] ? this.events[eventIndex].event.isFinished === 'true' : false;
  }

  /**
   * Update data according to selected event
   */
  private updateCurrentEvent(): void {
    // get new current event
    this.currentEvent = this.events[this.currentEventIndex];

    if (this.currentEvent) {
      // get new market current sections
      const marketSections = this.virtualSportsService.getMarketSectionsArray(this.currentEvent);
      this.sections = this.filterService.orderBy(marketSections, ['displayOrder']);
      this.setSwitchers();
    }
    if (this.isLegendsSport) {
      this.showQuantumLeap = this.event && this.event.isUKorIRE && this.sportName !== 'greyhound';
      this.isNotAntepostOrSpecials = !this.isAntepostMarket() && !this.horseracing.isRacingSpecials(this.event);
      this.isRacingSpecialsCondition = this.horseracing.isRacingSpecials(this.event);
      this.isMarketAntepost = this.isAntepostMarket();
      this.syncToApplySorting();
      this.streamFilter = 'hideStream';
      this.shouldShowCSBIframe = this.watchRulesService.shouldShowCSBIframe(this.event, this.performConfig);
      this.videoStreamStarted = false;
      this.playerLoaded = false;
    }
  }

  /**
   * Set switchers configs for event markets
   */
  private setSwitchers(): void {
    const marketSwitchers: ISwitcherConfig[] = [];
    const marketNames: string[] = Object.keys(MARKETS_CONFIG);

    this.hasWinOrEachWay = false;
    this.showTerms = false;
    this.event = this.virtualSportsService.normalizeData(this.currentEvent, this.isEventOngoing());

    this.event.markets.filter(
      market => market.template === winEwTemplateName ||
        (market.template === verticalTemplateName &&
          marketNames.includes(market.marketName.toLowerCase())))
      .forEach((market: IMarket) => {
        const isWinEW = market.template === winEwTemplateName;
        const filterName = isWinEW ? market.template.toLowerCase() : market.marketName.toLowerCase();
        const marketSwitcher = this.getMarketSwitcherConfig(filterName);

        marketSwitchers.push(marketSwitcher);

        if (isWinEW) {
          this.hasWinOrEachWay = true;
          this.market = market;
          this.filter = filterName;
          this.terms = this.virtualSportsService.genTerms(market);
          this.showTerms = this.virtualSportsService.showTerms(market)
            && !(this.currentEvent.event && this.currentEvent.event.className === '|Virtual Speedway|');

          const isForecastMarket: boolean = market.ncastTypeCodes && market.ncastTypeCodes.includes('CF') && market.outcomes.length >= 2;
          const isTriCastMarket: boolean = market.ncastTypeCodes && market.ncastTypeCodes.includes('CT') && market.outcomes.length >= 3;

          if (isForecastMarket) {
            const switcher = this.getMarketSwitcherConfig(forecastFilter);
            marketSwitchers.push(switcher);
          }

          if (isTriCastMarket) {
            const switcher = this.getMarketSwitcherConfig(tricastFilter);
            marketSwitchers.push(switcher);
          }
        }
      });
      this.applySortByName();
      if (this.market) {
        this.selectedMarket = this.market.label;
      }
    this.switchers = marketSwitchers;
  }

  /**
   * Create switcher config for specific market
   * @param filterName - name of specific market
   * return {ISwitcherConfig} - switcher config
   */
  private getMarketSwitcherConfig(filterName: string): ISwitcherConfig {
    const marketName: string = MARKETS_CONFIG[filterName];

    if (marketName) {
      return {
        onClick: () => this.filter = filterName,
        viewByFilters: filterName,
        name: marketName
      };
    }
  }

  /**
   * Delete current event, update indexes
   * param {String} eventId
   */
  private deleteEvents(eventIds: Array<string>): void {
    if (!this.events.length) {
      return;
    }
    this.events = this.events.filter(item => !eventIds.includes(item.event.id.toString()));
    if (!this.events.length) {
      this.pubsub.publish(this.pubsub.API.RELOAD_COMPONENTS);
      return;
    }

    if (this.currentEventIndex !== 0) {
      this.currentEventIndex = this.events.findIndex(e => e.event.id.toString() === this.currentEvent.id.toString());

      if (this.currentEventIndex < 0) {
        this.currentEventIndex = 0;
      }
    }

    this.update();
    this.activeClass.startTimeUnix = this.currentEvent && this.currentEvent.event.startTimeUnix;
  }

  /**
   * Removes outdated events
   */
  private removeOutdatedEvents(): void {
    let startedEventIds: string[] = this.events
      .filter(e => e.event.startTimeUnix < Date.now())
      .map(e => e.event.id.toString());

    startedEventIds = startedEventIds.slice(0, startedEventIds.length - 1);
    if(startedEventIds && startedEventIds.length) {
      this.deleteEvents(startedEventIds);
    }
  }

  /**
   * Add fields that are needed for tabs panel
   */
  private prepareEventsForTabs(): void {
    _.each(this.events, item => {
      item.title = this.datePipe.transform(item.event.startTimeUnix, 'HH:mm');
      item.id = item.event.id;
    });
  }

  /**
   * Update data
   */
  private update(): void {
    this.updateCurrentEvent();
    this.panelsStates = this.panelState.getPanelsStates();
  }

  /**
   * Init data
   */
  private init(): void {
    this.paramsSubscriber = this.route.params.pipe(
      concatMap((params: Params) => {
        this.showSpinner();
        return observableFrom(this.virtualSportsService.getEventsWithRacingForms(params.alias)).pipe(catchError(() => {
          this.showError();
          return of();
        }));
      })).subscribe((eventData: ISportEventEntity[]) => {
        this.eventsData = eventData;

        this.parentCategoryAlias = this.route.snapshot.params['category'];
        this.categoryAlias = this.route.snapshot.params['alias'];
        this.virtualAutoseoData();
        this.eventId = this.route.snapshot.params['eventId'];

        this.childMenu = this.virtualMenuDataService.getChildMenuItems(this.parentCategoryAlias);
        this.activeChild = this.virtualMenuDataService.activeChildIndex;

        this.activeClass = this.virtualSportsService.getActiveClass(this.categoryAlias);
        this.isLegendsSport = this.activeClass.classId == '223';
        const parentCategory = this.vsMapperService.getParentByAlias(this.parentCategoryAlias);
        this.ctaText = parentCategory && parentCategory.ctaButtonText;
        this.ctaUrl = parentCategory && parentCategory.ctaButtonUrl;

        this.events = this.virtualSportsService.filterEvents(this.eventsData);
        this.prepareEventsForTabs();

        // first event shown by default first elem of array
        this.currentEventIndex = this.eventId ? this.events.findIndex(e => e.event.id.toString() === this.eventId.toString()) : 0;

        if (this.currentEventIndex < 0) {
          this.requestedEventNotFound = true;
          this.currentEventIndex = 0;
        }

        // subscribe for live serve updates
        this.virtualSportsService.unSubscribeVSBRForUpdates();
        this.virtualSportsService.subscribeVSBRForUpdates(this.events);

        this.goToNextIfStarted(this.currentEventIndex);
        this.update();
        if (this.isLegendsSport) {
          const eventsFromEntity = this.events.map((event: ISportEventEntity) => event.event);
          this.events.forEach((event: ISportEventEntity) => {
            const masterEventIndex = this.events.findIndex(e => e.event.id == event.id);
            const currentEventEntity = this.events[masterEventIndex];
            this.event = this.virtualSportsService.normalizeData(currentEventEntity, this.isEventOngoing());
          });
          this.racingPostDataLoaded = false;
          this.racingPostService.updateRacingEventsList(eventsFromEntity, true).subscribe(() => {
            this.update();
            this.racingPostDataLoaded = true;
          });

          this.isHR = this.event.categoryCode === 'HORSE_RACING';
          this.isGreyhoundEdp = this.event.categoryCode !== 'HORSE_RACING';
          this.streamControl = {
            externalControl: true,
            playLiveSim: _.noop,
            playStream: _.noop,
            hideStream: _.noop
          };
          this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
            this.performConfig = config.performGroup;
            this.sortOptionsEnabled = config.SortOptions && config.SortOptions.enabled && (this.isHR) && !this.isAntepostMarket();
            this.toteLabel = this.localeService.getString('uktote.totepool');
            this.syncToApplySorting();
            this.racingName = this.racingService.getConfig().name;
          });
          this.cmsService.getFeatureConfig('NativeConfig').subscribe(data => {
            if (data && data.showFullScreen && data.fullScreenDrillDownTags) {
              this.isFullScreenConfig = true;
              this.fullScreenDrillDownTags = data.fullScreenDrillDownTags;
            }
            if (data && data.insightsDrillDownTags) {
              this.insightsDrillDownTags = data.insightsDrillDownTags;
            }
          });
          this.sortByOptionsService.isGreyHound = this.isGreyhoundEdp;
          this.sortBy = this.sortByOptionsService.get();
        }

        if (this.deviceService.isWrapper) {
          this.categoryId = this.virtualSportsService.getCategoryByAlias(this.categoryAlias);
          const eventId = this.eventId ? this.eventId : this.events[0].id;
          this.nativeBridge.onVirtualsSelected(this.categoryId, eventId);

          this.pubsub.subscribe(this.tagName, this.pubsub.API.VIRTUAL_ORIENTATION_CHANGED, classId => {
            // return both parent and child aliases
            const aliases: ICategoryAliases = this.virtualSportsService.getAliasesByClassId(classId);

            if (aliases && aliases.childAlias !== this.categoryAlias) {
              this.router.navigate([VIRTUAL_ROUTE_NAME, aliases.parentAlias, aliases.childAlias]);
            }
          });
        }

        this.pubsub.subscribe(this.tagName, this.pubsub.API.VS_EVENT_FINISHED, args => {
          this.requestedEventNotFound = false;
          this.updateFinishedStatus(args.eventId);
          setTimeout(() => this.deleteEvents([args.eventId]), this.timeService.goForNextVsEvent);
        });

        // This is handling event switching in case we do not receive valid event updates finish status.
        this.pollingTimer = this.windowRef.nativeWindow
          .setInterval(() => this.removeOutdatedEvents(), this.timeService.eventPollingInterval);

        this.hideSpinner();
        this.hideError();
      }, () => {
        this.showError();
      });
  }

  private updateFinishedStatus(finishedId: string) {
    this.events.forEach((event: ISportEventEntity) => {
      if (event.event.id.toString() === finishedId) {
        event.event.isFinished = 'true';
      }
    });
  }
  /**
  * Assigns autoSeoData object and publish the data for virtual sports-autoseo
  */
  private virtualAutoseoData(): void {
    this.autoSeoData.isOutright = false;
    this.autoSeoData.categoryName = this.parentCategoryAlias;
    this.autoSeoData.typeName = this.categoryAlias;
    this.pubsub.publish(this.pubsub.API.AUTOSEO_DATA_UPDATED, (this.autoSeoData));
  }

  /**
   * Check for market with antepost flag
   * @returns {boolean}
   */
  private isAntepostMarket(): boolean {
    return this.event &&
      this.event.markets &&
      this.event.markets[0] &&
      this.event.markets[0].isAntepost === 'true';
  }
  /**
   * Handler for Sort by name
   * @param  {number} mindex
   */
  private applySortByName(): void {
    this.event.markets.forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFilters.orderOutcomesByName(market.outcomes);
      _.each(market.outcomes, (outcome: IOutcome) => {
        outcome.nonRunner = outcome.name.search(/N\/R$/) > -1;

        if (outcome.runnerNumber) {
          const index = outcome.name.search(/(\(RES\))/);
          outcome.trapNumber = index !== -1 ? outcome.displayOrder : Number(outcome.runnerNumber);
        }

        if (outcome.children && outcome.children[0].price) {
          outcome.prices = [outcome.children[0].price];
        } else {
          _.extend(outcome.prices, [{ priceType: market.priceTypeCodes }]);
        }
      });
      this.setMarketsInfo(market, mindex);
    });
  }

  /**
   * Handler for setting markets info
   * @param  {IMarket} market
   * @param  {number} mindex
   * @returns void
   */
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
   * Handler for setting outcome favourite
   * @param  {IOutcome} outcomeEntity
   * @returns void
   */
  private setOutcomeFavourite(outcomeEntity: IOutcome): void {
    outcomeEntity.isFavourite = +outcomeEntity.outcomeMeaningMinorCode > 0 ||
      outcomeEntity.name.toLowerCase() === 'unnamed favourite' ||
      outcomeEntity.name.toLowerCase() === 'unnamed 2nd favourite';
  }

  /**
   * Initialize pubsub for Sorting
   * @returns void
   */
  private syncToApplySorting(): void {
    if (this.sortOptionsEnabled) {
      this.pubsub.subscribe('RacingEventComponent', this.pubsub.API.SORT_BY_OPTION, (option: string) => {
        this.applySortBy(option);
        this.racingGaService.updateGATracking(this.event, option, this.isGreyhoundEdp);
      });
      this.pubsub.subscribe('RacingEventComponent', `${this.pubsub.API.SORT_BY_OPTION}${this.event.id || ''}`, (option: string) => {
        this.applySortBy(option);
      });
    }

    const sortByName = this.event.markets.every((market: IMarket) => {
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
   * Sorting handler logic for odds cards
   * @param  {string} option
   * @returns void
   */
  private applySortBy(option: string): void {
    const noRunnerNumbers = this.event.markets.every(
      (market: IMarket) => market.outcomes.every((outcome: IOutcome) => !Number(outcome.runnerNumber))
    );

    const byPrice = option.toLowerCase() === 'price' || noRunnerNumbers;
    this.sortBy = option;
    [this.market].forEach((market: IMarket, mindex: number) => {
      market.outcomes = this.sbFilters.orderOutcomeEntities(market.outcomes,
        market.isLpAvailable && byPrice, true, true, false, false,
        !this.isHR && !this.event.isResulted);
      this.setMarketsInfo(market, mindex);
    });
  }

  private get racingService(): HorseracingService | GreyhoundService {
    return this.isHorseRacingScreen ? this.horseracing : this.greyhoundService;
  }
  private set racingService(value: HorseracingService | GreyhoundService) { }

  /**
   * Calculating video player height based on device
   * @returns void
   */
  private calculateVideoPlayerHeight(): void {
    const HEIGHT_COEFFICIENT: number = 1.37;
    const MAX_FRAME_WIDTH: number = 600;
    const elWidth: number = this.performGroupService.getElementWidth(this.elementRef);
    const updatedFrameWidth: number = elWidth > MAX_FRAME_WIDTH
      ? MAX_FRAME_WIDTH
      : elWidth;

    if (updatedFrameWidth === this.frameWidth) {
      return;
    }

    // Initial size of iframe
    this.frameWidth = updatedFrameWidth;
    this.frameHeight = Math.round(this.frameWidth / HEIGHT_COEFFICIENT);
  }
}
