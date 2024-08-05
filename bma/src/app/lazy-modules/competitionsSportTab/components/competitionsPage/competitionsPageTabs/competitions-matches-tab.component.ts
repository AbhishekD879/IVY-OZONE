import { Component, Input, OnChanges, SimpleChanges, OnInit, OnDestroy } from '@angular/core';

import { Subscription } from 'rxjs';
import { MarketSortService } from '@sb/services/marketSort/market-sort.service';
import { ITypeSegment, IGroupedByDateObj, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@core/services/cms/cms.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import { ISportConfig } from '@app/core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'competitions-matches-tab',
  templateUrl: 'competitions-matches-tab.component.html'
})
export class CompetitionsMatchesTabComponent implements OnInit,OnChanges,OnDestroy {
  @Input() eventsByCategory: ITypeSegment;
  @Input() eventsByCategoryCopy?: ITypeSegment; // needed only on Competitions Page for market selector with filters available
  @Input() sportId: string;
  @Input() sport: GamingService;
  @Input() isLoaded: boolean;
  @Input() competitionPage: boolean = false;
  @Input() inner: boolean = true;
  @Input() targetTab: ISportConfig;
  @Input() eventQuickSwitch: boolean = false;
  @Input() filteredQuickSwitchEvents: IGroupedByDateItem[] = [];

  public isMarketSelected: boolean = false;
  public isMarketSelectorSticky: boolean = true;
  undisplayedMarket: IMarket;
  filteredMatches: IGroupedByDateItem[] = [];
  isMarketSelectorAvailable: boolean = true;
  isMarketSwitcherConfigured: boolean = false;
  isMarketSwitcherLoaded: boolean = false;
  private marketSwitcherConfigSubscription: Subscription;
  private setSelectedMarket: string;
  selectedMarketSwitcher: string;
  isLoadedFilter: boolean = true;
  twoUpMarkets = {'2Up - Instant Win':'2Up - Instant Win','2Up&Win Early Payout':'2Up&Win - Early Payout'};
  showNoEvents = false;
  private readonly componentId = 'competitionsMatchesTab';

  constructor(
    private marketSortService: MarketSortService,
    private filterService: FiltersService,
    private cmsService: CmsService,
    private competitionFiltersService: CompetitionFiltersService,
    private pubSubService: PubSubService
  ) { }

  ngOnInit() {
    this.isMarketSelectorAvailable = environment.CATEGORIES_DATA.categoryIds.includes(this.sportId as any);
    this.marketSwitcherConfigSubscription = this.cmsService.getMarketSwitcherFlagValue(this.sport.sportConfig.config.name)
      .subscribe((flag: boolean) => {
        this.isMarketSwitcherConfigured = flag;
        this.isMarketSwitcherLoaded = !(this.competitionPage && this.isMarketSwitcherConfigured) || this.eventQuickSwitch;
        if(this.isMarketSwitcherConfigured && !this.isMarketSwitcherLoaded){
          this.isLoadedFilter = true;
          if(!this.isLoaded && environment.CURRENT_PLATFORM == "mobile"){
            this.isLoaded = false;
          }
          if(this.isLoaded && environment.CURRENT_PLATFORM == "desktop"){
            this.isLoaded = !this.eventsByCategoryCopy ? true : false;
          }
        }
      });
    if(this.eventQuickSwitch) {
      this.filteredMatches = this.getFilteredMatches();
      this.validateMatches();
      this.pubSubService.subscribe(this.componentId, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, () => {
        this.validateMatches();
      });
    }
  }
  /**
   * Checks if markets are available or not
   * @returns {void}
   */
  validateMatches(): void {
    this.filteredMatches.forEach(comp => {
      comp.events.forEach(event => {
        if (event.markets.length === 0){
          this.showNoEvents = true;
          return;
        }
      })
    })
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(this.isMarketSwitcherConfigured && changes.isLoaded){
      this.isLoadedFilter = false;
    }
    if (changes.eventsByCategory && changes.eventsByCategory.currentValue) {
      this.isMarketSelected = this.checkSelectedMarkets(changes.eventsByCategory.currentValue);
      this.filteredMatches = this.getFilteredMatches();
    }
    if (changes.filteredQuickSwitchEvents) {
      this.filteredQuickSwitchEvents = changes.filteredQuickSwitchEvents.currentValue;
      this.filteredMatches = this.filteredQuickSwitchEvents;
    }
    if (changes.isLoaded) {
      this.isLoaded = changes.isLoaded.currentValue;
    }
  }

  ngOnDestroy(): void {
    this.marketSwitcherConfigSubscription && this.marketSwitcherConfigSubscription.unsubscribe();
    this.pubSubService.unsubscribe(this.componentId);
  }

  selectedMarket(eventsByCategory: ITypeSegment): string {
    const request = this.sport.sportConfig.config.request;
    environment.CATEGORIES_DATA.defaultMarkets.filter(item => {
      if (item.sportIds.includes(this.sportId as any)) {
        this.setSelectedMarket = eventsByCategory.defaultValue || item.name;
      }
    });
    if(!this.isMarketSwitcherConfigured && request.aggregatedMarkets && request.aggregatedMarkets.length){
      this.setSelectedMarket = request.aggregatedMarkets[0].titleName;
  }
    return this.setSelectedMarket;
  }

  /**
   * Filter Events by Markets selector
   * @param {string} marketFilter
   */
  filterEvents(marketFilter: ILazyComponentOutput): void {
    this.isMarketSwitcherLoaded = true;
    this.isLoaded = true;
    this.isLoadedFilter = true;
    this.selectedMarketSwitcher = this.twoUpMarkets[marketFilter.value];
    this.eventsByCategoryCopy && (this.competitionFiltersService.selectedMarket = marketFilter.value);
    this.marketSortService.setMarketFilterForOneSection(this.eventsByCategory, marketFilter.value);
    this.eventsByCategoryCopy && this.marketSortService.setMarketFilterForOneSection(this.eventsByCategoryCopy, marketFilter.value);
    this.filteredMatches = !this.eventsByCategoryCopy
      ? this.getFilteredMatches()
      : this.competitionFiltersService.filterEventsByHiddenMarkets(this.getFilteredMatches()) as IGroupedByDateItem[];
  }

  /**
   * Check event markets are selected
   * @param {ITypeSegment} eventsByCategory
   * @returns {boolean}
   */
  checkSelectedMarkets(eventsByCategory: ITypeSegment): boolean {
    return eventsByCategory.events ? eventsByCategory.events.some((event: ISportEvent) => {
      return event.markets.some((market: IMarket) => {
        market.name = market.name === 'Match Betting'
        && this.sportId === environment.CATEGORIES_DATA.footballId ? 'Match Result' : market.name;
        let selectedMarket: any = this.selectedMarket(eventsByCategory);
        selectedMarket = selectedMarket ? selectedMarket.split(',') : [];
        return selectedMarket.includes(market.templateMarketName) || selectedMarket.includes(market.name);
      });
    }) : false;
  }

  /**
   * Track Events by typeId
   * @param {ITypeSegment} event
   * @returns {string}
   */
  trackByTypeId(event: ITypeSegment): string {
    return event.typeId;
  }

  /**
   * Fet Filtered Matches
   * @param {IGroupedByDateObj} matches
   * @returns {IGroupedByDateItem[]}
   */
  getFilteredMatches(): IGroupedByDateItem[] {
    if(this.eventQuickSwitch) return this.filteredQuickSwitchEvents;
    const groupedByDate: IGroupedByDateObj = this.eventsByCategory && this.eventsByCategory.groupedByDate;

    if (!groupedByDate) {
      return [];
    }

    const groups = [];

    Object.keys(groupedByDate).forEach((date: string) => {
      if (!groupedByDate[date].deactivated) {
        groupedByDate[date].events = this.filterService.orderBy(groupedByDate[date].events, ['startTime', 'displayOrder', 'name']);
        groups.push(groupedByDate[date]);
      }
    });

    return groups;
  }

  reinitHeader(changedMarket: IMarket): void {
    this.undisplayedMarket = changedMarket;
  }
}
