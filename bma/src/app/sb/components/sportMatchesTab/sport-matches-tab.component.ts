import {
  ChangeDetectorRef,
  Component,
  Input,
  Output,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
  EventEmitter
} from '@angular/core';
import { from, Subscription } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import * as _ from 'underscore';
import { CmsService } from '@core/services/cms/cms.service';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';
import { StorageService } from '@core/services/storage/storage.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { MarketSortService } from '@sb/services/marketSort/market-sort.service';
import { ITypeSegment, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { Location } from '@angular/common';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';
import { IMarket } from '@app/core/models/market.model';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import environment from '@environment/oxygenEnvConfig';
import { VanillaApiService } from '@frontend/vanilla/core';
import { UserService } from '@app/core/services/user/user.service';
import { TemplateService } from '@app/shared/services/template/template.service';
import { ISportConfigTab, ISystemConfig } from '@app/core/services/cms/models';
import { DeviceService } from '@app/core/services/device/device.service';
import { TimeService } from '@app/core/services/time/time.service';
@Component({
  selector: 'sport-matches-tab',
  templateUrl: 'sport-matches-tab.component.html'
})
export class SportMatchesTabComponent implements OnInit, OnDestroy, OnChanges {
  @Input() sport: GamingService;
  @Input() tab: string = '';
  @Input() featuredEventsCount: number;
  @Input() timeFilter: ICompetitionFilter;
  @Input() leagueFilter: ICompetitionFilter;
  @Input() isSportEventFiltersEnabled: boolean;
  @Input() targetTab: ISportConfigTab;

  @Output() readonly isLoadedEvent = new EventEmitter<ILazyComponentOutput>();
  @Output() readonly displayFilters = new EventEmitter<boolean>();

  eventsBySections: ITypeSegment[] = [];
  eventsBySectionsCopy: ITypeSegment[] = [];
  eventsCache: ISportEvent[] = [];

  showEventsBySections: boolean;
  enhancedEvents: ISportEvent[] = [];
  isLoaded: boolean = false;
  isResponseError: boolean = false;
  isExpandedEnhanced: boolean = true;
  isLoadedEnhanced: boolean = false;
  sportName: string;
  sportId: number;
  isDisplayTutorial: boolean;
  showAccordionBody: boolean;
  detectListener;
  groupedByDateEnhancedEvents: ITypeSegment;
  locationPath: string;
  isMarketSelectorActive: boolean;
  readonly tag = 'MatchesSportTabComponent';
  undisplayedMarket: IMarket;
  isMarketSwitcherConfigured: boolean = false;
  isMarketSwitcherComponentLoaded: boolean = false;
  isFirstLoad = true;
  isFanzoneEnabled = true;
  isListTemplate: boolean = false;
  currentTabName: string = '';
  selectedMarketSwitcher: string;
  twoUpMarkets = { '2Up - Instant Win': '2Up - Instant Win', '2Up&Win Early Payout': '2Up&Win - Early Payout' }
  currentURL: string;

  protected activeMarketFilter: string;
  private loadDataSubscription: Subscription;
  private enhancedMultiplesSubscription: Subscription;
  private marketSwitcherConfigSubscription: Subscription;
  private sportSchemaUrl: string;
  private schemaTabs = ['today','','tomorrow'];
  private readonly SB_TODAY: string = 'sb.today';
  private readonly TODAY: string = 'today';
  private readonly TOMORROW: string = 'tomorrow';
  constructor(
    private activatedRoute: ActivatedRoute,
    private cmsService: CmsService,
    private sportTabsService: SportTabsService,
    private marketSortService: MarketSortService,
    private enhancedMultiplesService: EnhancedMultiplesService,
    private storageService: StorageService,
    private pubSubService: PubSubService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private location: Location,
    private gtmService: GtmService,
    private routingHelperService: RoutingHelperService,
    private favouritesService: FavouritesService,
    private router: Router,
    private competitionFiltersService: CompetitionFiltersService,
    protected vanillaApiService: VanillaApiService,
    public user: UserService,
    private templateService: TemplateService,
    private deviceService: DeviceService,
    private timeService: TimeService
  ) {
    this.changeDetectorRef.detach();
    this.locationPath = this.location.path();
  }

  ngOnInit(): void {
    this.detectListener = this.windowRef.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
    }, 500);

    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
    this.sportId = Number(this.sport.sportConfig.config.request.categoryId);
    this.isDisplayTutorial = this.sportName === 'football' &&
      !this.storageService.get('footballTutorial') &&
      this.favouritesService.isFavouritesEnabled;

    this.activeMarketFilter = undefined;
    this.loadMatchesData();
    this.pubSubService.subscribe(this.tag, this.pubSubService.API.DELETE_MARKET_FROM_CACHE, () => {
      if (this.eventsCache) {
        this.sport.setMarketsAvailability(this.eventsCache, this.eventsBySections);
      }
      this.initMarketSelector(this.activeMarketFilter);
    });

    this.pubSubService.subscribe(this.tag, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: string) => {
      this.sportTabsService.deleteEvent(eventId, this.eventsBySections);
    });
    this.getMSDataFromCMSFeature();
    this.pubSubService.subscribe(this.tag, this.pubSubService.API.FANZONE_DATA, (fanzone) => {
      this.isFanzoneEnabled = false;
      this.changeDetectorRef.detectChanges();
      this.isFanzoneEnabled = true;
    });
  }

  ngOnDestroy(): void {
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }

    this.unsubscribeFromLiveUpdates();
    clearInterval(this.detectListener);
    this.pubSubService.unsubscribe(this.tag);
    this.enhancedMultiplesSubscription && this.enhancedMultiplesSubscription.unsubscribe();
    this.marketSwitcherConfigSubscription && this.marketSwitcherConfigSubscription.unsubscribe();
    this.removeSchemaForSportsTab();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.tab) {
      this.currentTabName = changes.tab.currentValue;
    }
    if (changes.tab && changes.tab.currentValue && changes.tab.previousValue) {
      this.activeMarketFilter = undefined;

      if (changes.tab.currentValue !== 'today') { // reset all filters if tab is different than 'today'
        this.timeFilter = null;
        this.leagueFilter = null;
      }
      this.removeSchemaForSportsTab();

      this.loadMatchesData();
    }

    if (changes.sport && changes.sport.currentValue !== changes.sport.previousValue) {
      this.sport = changes.sport.currentValue;
    }

    if (changes.featuredEventsCount && changes.featuredEventsCount.currentValue !== changes.featuredEventsCount.previousValue) {
      this.featuredEventsCount = changes.featuredEventsCount.currentValue;
    }

    if (changes.timeFilter && changes.timeFilter.currentValue !== changes.timeFilter.previousValue) {
      this.timeFilter = changes.timeFilter.currentValue;
      this.filterEventsByCompetitionFilter(this.leagueFilter, this.timeFilter);
    }

    if (changes.leagueFilter && changes.leagueFilter.currentValue !== changes.leagueFilter.previousValue) {
      this.leagueFilter = changes.leagueFilter.currentValue;
      this.filterEventsByCompetitionFilter(this.leagueFilter, this.timeFilter);
    }
  }

  updateDynamicProperties(): void {
    this.isMarketSelectorActive = this.eventsBySectionsCopy.length > 0;
    this.showEventsBySections = this.eventsBySections.length && (!this.isMarketSelectorActive || !!this.eventsBySections[0].defaultValue);
  }

  selectedMarket(eventsBySection: ITypeSegment): string {
    let setSelectedMarket;
    const request = this.sport.sportConfig.config.request;
    environment.CATEGORIES_DATA.defaultMarkets.filter(item => {
      if (item.sportIds.includes(this.sportId as any + '')) {
        setSelectedMarket = eventsBySection.defaultValue || item.name;
      }
    });
    if(!this.isMarketSwitcherConfigured && request.aggregatedMarkets && request.aggregatedMarkets.length) {
      setSelectedMarket = request.aggregatedMarkets[0].titleName;
    }
    return setSelectedMarket;
  }

  trackByTypeId(index: number, sportSection: ITypeSegment): string {
    return `${sportSection.typeId}_${sportSection.deactivated}`;
  }

  trackById(index: number, sportEvent: ISportEvent): number {
    return sportEvent.id;
  }

  filterEvents(marketFilter: string): void {
    this.selectedMarketSwitcher = this.twoUpMarkets[marketFilter];
    if (!this.activeMarketFilter || this.activeMarketFilter !== marketFilter) {
      this.initMarketSelector(marketFilter);
    }
  }

  hideEnhancedSection(): void {
    this.isExpandedEnhanced = false;
  }

  trackEvent(eventEntity: ISportEvent): void {
    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'upcoming module',
      eventAction: this.locationPath,
      eventName: eventEntity.name,
      eventLabel: 'view event',
      eventID: eventEntity.id
    });
  }

  trackByDate(index: number, dateGroup: IGroupedByDateItem) {
    return `${dateGroup.startTime}_${dateGroup.title.replace(' ', '_')}_${index}`;
  }

  isPrimaryMarket(eventsBySection: ITypeSegment): boolean {
    // non Football case
    if (!eventsBySection.defaultValue) {
      return true;
    }
    // Football Primary market case
    return eventsBySection.defaultValue.toLowerCase() === 'match result';
  }

  /**
   * Load Sport Matches Data
   * removed in html eventsGroup.marketsAvailability[eventsBySection.defaultValue?.toLowerCase()]
   * added below condition when default value contains multiple markets
   * if any one market available it will display odds card 
   */
  checkMarketsAvailability(eventsGroup: IGroupedByDateItem, defaultValue: string): boolean {
    let availability = false;
    const defaultValueMulti = defaultValue ? defaultValue.split(',') : [];
    if(_.contains(defaultValueMulti, 'match result')){
      defaultValueMulti.push('match betting');
    }
    defaultValueMulti.forEach((value: string) => {
      if (eventsGroup.marketsAvailability[value.trim().toLowerCase()]) {
        availability = true;
      }
    });
    return availability;
  }
  
  updateState(state: boolean, type, section?: ITypeSegment): void {
    if (type === 'enhanced') {
      this.isExpandedEnhanced = state;
    }

    if (type === 'event' && section) {
      // this.activeMarketFilter
      if (state) {
        // If section was not - subscribe for live updates
        this.subscribeForSectionUpdates(section);
      } else if (!state && section.isExpanded) {
        // If section was expanded - unsubscribe from live updates
        this.unsubscribeFromSectionUpdates(section);
      }

      section.isExpanded = state;
    }
  }

  goToCompetition(competitionSection: ITypeSegment): void {
    const competitionPageUrl = this.routingHelperService.formCompetitionUrl({
      sport: this.activatedRoute.snapshot.paramMap.get('sport'),
      typeName: competitionSection.typeName,
      className: competitionSection.className
    });

    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'upcoming module',
      eventAction: this.locationPath,
      eventLabel: 'see all',
      competitionName: competitionSection.sectionTitle
    });

    this.router.navigateByUrl(competitionPageUrl);
  }

  handleOutput(output: ILazyComponentOutput) {
    if (output.output === 'filterChange') {
      this.filterEvents(output.value);
    }
    if (output.output === 'hideEnhancedSection') {
      this.hideEnhancedSection();
    }
  }

  reinitHeader(changedMarket: IMarket): void {
    this.undisplayedMarket = changedMarket;
  }

  /**
   * Load Sport Matches Data
   */
  loadMatchesData(): void {
    this.isLoaded = false;
    this.currentURL = this.activatedRoute.snapshot['_routerState']?.url;
    this.isLoadedEvent.emit({ output: 'isLoadedEvent', value: this.isLoaded });
    this.isResponseError = false;
    this.isMarketSwitcherComponentLoaded = false;
    const isGolfMatches = this.sportId === 18 && this.currentURL.includes('golf_matches');
    const isGolfMobileEvents = this.sportId === 18 && this.currentURL.endsWith('/matches');
    let tabName = this.tab || 'upcoming';
    tabName = isGolfMobileEvents ? 'matchesTab' : tabName;
    tabName = isGolfMatches ? 'allEvents' : tabName;

    this.unsubscribeFromLiveUpdates();
    this.eventsBySections = [];
    this.eventsBySectionsCopy = []; // reset events copy when tab switches
    this.changeDetectorRef.detectChanges();
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }

    this.loadDataSubscription = from(this.sport.getByTab(tabName))
      .subscribe((events: ISportEvent[]) => {
        this.eventsCache = events;
        this.eventsBySections = events && events.length ?
          this.sportTabsService.eventsBySections(events, this.sport) : [];
        if (this.isFirstLoad) {
          this.isFirstLoad = false;
          this.displayFilters.emit(this.eventsBySections.length > 0);
        }
        this.isResponseError = false;
        this.eventsBySections = this.prepeareAccordions(this.eventsBySections);
        this.eventsBySectionsCopy = [...this.eventsBySections];
        this.deviceService.isRobot() && this.schemaForsportsTab(this.eventsBySectionsCopy);
        this.updateDynamicProperties();
        this.checkMarketSwitcherComponent();
        this.hideLoading();

        this.activeMarketFilter &&
          this.marketSortService.setMarketFilterForMultipleSections(this.eventsBySections, this.activeMarketFilter);
      }, (error) => {
        this.isResponseError = true;
        console.warn(`Matches ${tabName} Data:`, error && error.error || error);
        this.hideLoading();
      });

    this.enhancedMultiplesSubscription = this.enhancedMultiplesService.getEnhancedMultiplesEvents(this.sportName, this.tab)
      .subscribe((result: ISportEvent[]) => {
        this.enhancedEvents = this.sortSportEventsData(result);
        const upcomingEvents = (tabName === 'upcoming' || tabName === 'allEvents' ||tabName === 'matchesTab') ? this.filterUpcomingEvents(this.enhancedEvents)
          : this.enhancedEvents;
        if (upcomingEvents && upcomingEvents.length) {
          this.groupedByDateEnhancedEvents = this.sport.arrangeEventsBySection(upcomingEvents, true)[0];
        }
        this.isLoadedEnhanced = true;
        // display overlay
        setTimeout(() => {
          this.pubSubService.publish(this.pubSubService.API.SHOW_FOOTBALL_TUTORIAL);
        });
      }, (error => {
        this.isLoadedEnhanced = true;
        console.warn('Enhanced Data:', error && error.error || error);
      }));
  }

  protected prepeareAccordions(sections: ITypeSegment[]): ITypeSegment[] {
    let j: number = 0;

    _.each(sections, (section: ITypeSegment) => {
      if (!section.deactivated && j < 3) {
        this.updateState(true, 'event', section);
        j++;
      } else if (!section.isExpanded) {
        this.updateState(false, 'event', section);
      }
    });
    return sections;
  }

  protected initMarketSelector(marketFilter: string): void {
    this.isMarketSwitcherComponentLoaded = true;
    this.activeMarketFilter = marketFilter;
    this.showAccordionBody = false;
    this.isListTemplate = this.templateService.isListTemplate(marketFilter);
    this.isSportEventFiltersEnabled && (this.competitionFiltersService.selectedMarket = marketFilter);
    this.marketSortService.setMarketFilterForMultipleSections(this.eventsBySections, marketFilter);
    this.isSportEventFiltersEnabled && this.marketSortService.setMarketFilterForMultipleSections(this.eventsBySectionsCopy, marketFilter);

    this.windowRef.nativeWindow.setTimeout(() => {
      if (this.isSportEventFiltersEnabled) {
        this.filterEventsByCompetitionFilter(this.leagueFilter, this.timeFilter);
      }

      this.eventsBySections = [...this.prepeareAccordions(this.eventsBySections)];
      this.updateDynamicProperties();
      this.showAccordionBody = true;
    });
  }

  activeIndex(currIndex): number {
    let activeInd = 0;
    this.eventsBySections.forEach((eventsBySection, index) => {
      if(!eventsBySection.deactivated && index < currIndex) {
        activeInd++;
      }
    })
    return activeInd;
  }

  /**
   * Filters current events by selected | deselected league | time filter
   * @param {ICompetitionFilter} league
   * @param {ICompetitionFilter} time
   * @private
   */
  private filterEventsByCompetitionFilter(league: ICompetitionFilter, time: ICompetitionFilter): void {
    this.eventsBySections = this.prepeareAccordions(
      this.competitionFiltersService.filterEvents(league, time, this.eventsBySectionsCopy) as ITypeSegment[]
    );
  }

  private isInPlayEvent(event: ISportEvent): boolean {
    return Boolean(event.isLiveNowEvent) === true || Boolean(event.isStarted) === true;
  }

  private filterOutInplayEvents(events: ISportEvent[]) {
    return _.filter(events, event => !this.isInPlayEvent(event));
  }

  private filterUpcomingEvents(events: ISportEvent[]): ISportEvent[] {
    const upcomingEvents = this.sport.filterOutFutureEvents(events);
    return this.filterOutInplayEvents(upcomingEvents);
  }

  private checkMarketSwitcherComponent(): void {
    this.getMSDataFromCMSFeature();
    this.isMarketSwitcherComponentLoaded =
      this.isMarketSwitcherConfigured &&
        environment.CATEGORIES_DATA.categoryIds.includes(this.sport.sportConfig.config.request.categoryId) ? false : true;
  }

  /**
   * Sort results data
   * @param {ISportEvent[]} data
   * @returns {ISportEvent[]}
   */
  private sortSportEventsData(data: ISportEvent[]): ISportEvent[] {
    return _(data).chain().sortBy((event: ISportEvent) => {
      return event.name.toLowerCase();
    }).sortBy((event: ISportEvent) => {
      return event.startTime;
    }).value();
  }

  private hideLoading(): void {
    this.isLoaded = true;
    this.changeDetectorRef.detectChanges();
    this.windowRef.nativeWindow.setTimeout(() => this.isLoadedEvent.emit({ output: 'isLoadedEvent', value: this.isLoaded }));
  }

  /**
   * Subscribe for sEVENT, sEVMKT, sSELCN updates of all events in given section.
   * @param {ITypeSegment} section
   */
  private subscribeForSectionUpdates(section: ITypeSegment): void {
    if (section && !section.subscriptionKey) {
      section.subscriptionKey = this.sport.subscribeEventChildsUpdates(section.events, Number(section.typeId));
    }
  }

  /**
   * Ububscribve from sEVENT, sEVMKT, sSELCN updates of all events in given section by given section key.
   * @param {ITypeSegment} section
   */
  private unsubscribeFromSectionUpdates(section: ITypeSegment): void {
    if (section && section.subscriptionKey) {
      this.sport.unsubscribeEventChildsUpdates(section.subscriptionKey);
      section.subscriptionKey = null;
    }
  }

  /**
   * Ububscribve from sEVENT, sEVMKT, sSELCN updates of all events in all sections.
   */
  private unsubscribeFromLiveUpdates(): void {
    // unSubscribe LS Updates via WS
    _.each(this.eventsBySections, (section: ITypeSegment) => {
      this.unsubscribeFromSectionUpdates(section);
    });
  }
  /**
   * sort and publish events for seo schema
   * @param eventsBySections 
   */
  private schemaForsportsTab(eventsBySections: ITypeSegment[]): void {
    const filteredEvents: ISportEvent[] = [];
    let eventsForSchema: ISportEvent[] = [];
    let schemaConfig: string[] = [];
    if(eventsBySections && this.schemaTabs.indexOf(this.tab)>-1)
    {
      this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) =>{
        schemaConfig = sysConfig?.SeoSchemaConfig?.schemaConfig
      });
      eventsBySections.forEach((eventsBySection: ITypeSegment) => {
        eventsBySection?.events?.forEach((event: ISportEvent) => {
          const eventDayValue = event && this.timeService.determineDay(event.startTime, false);
          if(schemaConfig?.length && ((schemaConfig.includes(this.TODAY) && eventDayValue === this.TODAY) || (schemaConfig.includes(this.TOMORROW) && eventDayValue === this.TOMORROW))){
           filteredEvents.push(event);
          }
        });
      });
      this.routingHelperService.formSportUrl(this.sportName, this.tab).subscribe((url: string) => {
        this.sportSchemaUrl = url;
      });
      eventsForSchema = filteredEvents.length && this.competitionFiltersService.getSeoSchemaEvents(filteredEvents);
      eventsForSchema.length && this.pubSubService.publish(this.pubSubService.API.SCHEMA_DATA_UPDATED, [eventsForSchema, this.sportSchemaUrl]);
    }
  }
  /**
  * to remove the schemaScript
  */
  private removeSchemaForSportsTab(): void {
    this.deviceService.isRobot() && this.sportSchemaUrl && this.pubSubService.publish(this.pubSubService.API.SCHEMA_DATA_REMOVED, this.sportSchemaUrl);
  }
  /**
  * to add cms configs
  */
  private getMSDataFromCMSFeature(): void {
    this.marketSwitcherConfigSubscription = this.cmsService.getMarketSwitcherFlagValue(this.sport.sportConfig.config.name)
      .subscribe((flag: boolean) => {
        this.isMarketSwitcherConfigured = 
        (this.sport.sportConfig.config.name == 'golf' && this.currentURL.includes('golf_matches')) ? true : flag;
      });
  }
}
