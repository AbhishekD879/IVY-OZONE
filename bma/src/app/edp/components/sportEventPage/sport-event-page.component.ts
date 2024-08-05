import { Component, OnDestroy, Input, OnInit, ChangeDetectorRef } from '@angular/core';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Router, Event, NavigationEnd, ActivatedRoute, NavigationStart } from '@angular/router';
import { SportEventPageProviderService } from './sport-event-page-provider.service';
import { ISystemConfig } from '@core/services/cms/models';
import * as _ from 'underscore';
import { IMarketCollection, IPill } from '@core/models/market-collection.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IMarketTemplate } from '@core/models/market.model';
import { IConstant } from '@core/services/models/constant.model';
import { FootballExtensionService } from '@app/edp/services/footballExtension/football-extension.service';
import { TennisExtensionService } from '@app/edp/services/tennisExtension/tennis-extension.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IMarketsGroup } from '@edp/services/marketsGroup/markets-group.model';
import { ReplaySubject, Subscription } from 'rxjs';
import { TemplateService } from '@shared/services/template/template.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { IReference } from '@core/models/live-serve-update.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import environment from '@environment/oxygenEnvConfig';
import { ITab } from '@core/models/tab.model';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';
import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SeoDataService } from '@app/core/services/seoData/seo-data.service';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';
import { MARKET_VIEWTYPE } from '@edp/models/market-constants';
@Component({
  selector: 'sport-event-page',
  styleUrls: ['sport-event-page.component.scss'],
  templateUrl: './sport-event-page.component.html'
})
export class SportEventPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() isMobileOnly?: boolean = false;
  @Input() isOptaAvailable: boolean;
  @Input() isOptaProviderPresent: boolean;

  public showYourCallContent: boolean = false;
  public showFiveASideContent: boolean = false;
  public liveMaketTemplateMarketName: string;
  public eventEntity: ISportEvent;
  public marketGroup: IMarket[];
  public filteredMarketGroup: IMarket[];
  public aggregatedMarketsGroup: IMarketTemplate[];
  public scorecastInTabs: string[];
  public isScorecastMarketsAvailable: boolean;
  public eventTabs: ITab[];
  public isSpecialEvent: boolean = false;
  public activeTab: IMarketCollection;
  public typeId: string;
  public marketConfig: IMarket[];
  public marketAvailable: IConstant;
  public openedMarketTabsCountByDefault: number = 2;
  public initialized: boolean = false;
  public showSurfaceBets: boolean = false;
  public isMTASport: boolean = false;
  associatedMarkets: IMarket[];
  drilldownTagNames: string[];
  fiveASideTitle: string;
  fiveASideContent: string;
  position: number;
  showBanner: boolean;
  showPills: boolean = false;
  loading: boolean = false;
  is2UpAvailableCurr: boolean = false;
  is2UpAvailablePrev: boolean = false;
  public replaySubj: ReplaySubject<IMarketLinks[]> = new ReplaySubject(1);
  isExtend: boolean = false;

  protected marketName: string = '';
  protected routeChangeListener: Subscription;
  protected sportDataSubscription: Subscription;
  protected yourCallMarketAvailable: boolean = false;

  private fiveASideLauncher: string = 'FiveASideGameLauncher';
  private launcher: string = 'tab-5-a-side';
  private allMarketsTab: string = 'tab-all-markets';
  private defaultMarketName: string = 'main-markets';
  private MTA_SORT_CODES: string[] = environment.CATEGORIES_DATA.sortCodesForMTA;
  private openedMarketTabsMap: IConstant = {};
  private sportName: string = '';
  private isFootball: boolean = false;
  private sport: any = {};
  marketsByCollection: IMarketCollection[];
  private sysConfig: ISystemConfig;
  private sportsConfigSubscription: Subscription;
  private activePill: string;
  public eventName: string = '';
  public eventId: string;
  public brand: string;
  public isStatContentInfo : boolean = false;

  private bybTabsRe = /^tab-(build-your-bet|bet-builder|5-a-side)$/;
  twoUpMarketName: string;

  constructor(
    protected router: Router,
    protected activatedRoute: ActivatedRoute,
    protected sportEventPageProviderService: SportEventPageProviderService,
    protected templateService: TemplateService,
    private footballExtension: FootballExtensionService,
    private tennisExtension: TennisExtensionService,
    private routingHelperService: RoutingHelperService,
    protected pubSubService: PubSubService,
    private sportConfigService: SportsConfigService,
    private changeDetectorRef: ChangeDetectorRef,
    protected windowRefService: WindowRefService,
    private cmsService: CmsService,
    private routingState: RoutingState,
    protected marketsOptaLinksService: MarketsOptaLinksService,
    protected locale: LocaleService,
    protected seoDataService: SeoDataService,
    protected isPropertyAvailableService: IsPropertyAvailableService,
    protected cashOutLabelService: CashOutLabelService,
    protected sportEventPageService: SportEventPageService
  ) {
    super()/* istanbul ignore next */;
    this.marketName = this.activatedRoute.snapshot.paramMap.get('market') || this.defaultMarketName;
    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
    this.isFootball = this.sportName === 'football';
    this.eventId = this.activatedRoute.snapshot.paramMap.get('id');
    this.eventName = this.activatedRoute.snapshot.paramMap.get('eventName');
    this.twoUpMarketName = this.locale.getString('bma.twoUpMarketName');
    this.getTrackByValue = this.getTrackByValue.bind(this);
    // handle market deletion when market is undisplayed or all selections are undisplayed
    this.pubSubService.subscribe('sportEventPageCtrl', pubSubService.API.DELETE_MARKET_FROM_CACHE, marketId => {
      this.marketsByCollection && this.marketsByCollection.forEach((colection: IMarketCollection) => {
        const marketIndex = _.findIndex(colection.markets, {
          id: marketId
        });

        if (marketIndex >= 0) {
          colection.markets.splice(marketIndex, 1);
          this.init();
        }
      });
    });
    this.sportDataHandler = this.sportDataHandler.bind(this);

    this.subscribeToEvents();
  }

  public showLimit(marketEntity: IMarket): number {
    return !marketEntity.isAllShown ? marketEntity.showLimit : undefined;
  }

  /**
   * Check for showing YourCall markets
   * @param {object} market
   * @return {boolean}
   */
  public showYourCallMarket(market: IMarketsGroup): boolean {
    return this.yourCallMarketAvailable && market.localeName === 'yourCall';
  }

  /**
   * Check if event has scorecast market
   * @param market
   * return {boolean}
   */
  public hasScorecastMarket(market: IMarket): boolean {
    const correctScorePattern = new RegExp('^correct\\sscore$', 'i');
    const matchCorrectScorePattern = market.name.toString().match(correctScorePattern) !== null;

    return this.isFootball && matchCorrectScorePattern && this.isScorecastMarketsAvailable &&
      !this.eventEntity.isStarted &&
      (this.scorecastInTabs.indexOf((this.isMobileOnly && this.showPills) ? this.getActivePill() : this.activeTab.marketName) > -1);
  }

  /**
   * Toggle method to show hide selections on YourCall markets
   * @param marketEntity
   */
  public toggleShowYourCallMarket(marketEntity: IMarket) {
    marketEntity.isAllShown = !marketEntity.isAllShown;
  }

  /**
   * Hide Accordion header
   * @param {Object} market
   * @returns {Boolean}
   */
  public isHeaderHidden(market: IMarket): boolean {
    return market.marketsGroup || market.viewType === MARKET_VIEWTYPE.CORRECT_SCORE || market.viewType === MARKET_VIEWTYPE.SCORER;
  }

  /**
   * Accordion expand status
   * @param {Number} index
   * @param {Object} market
   */
  public isExpanded(id?: string, market?: IMarket): boolean {
    const isMarket = market ? market.isSCAvailable || this.isHeaderHidden(market) : false;
    const keyName = market ? this.isMTASport ? market.name : market.id : id;
    return this.openedMarketTabsMap[keyName] || isMarket;
  }

  public changeAccordionState(market: IMarket, value: boolean) {
    const keyName = this.isMTASport ? market.name : market.id;
    this.openedMarketTabsMap[keyName] = value;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Get trackBy Value
   * @param {number} index
   * @param {object} market
   * @return {string}
   */
  public getTrackByValue(index: number, market: IMarket): string {
    return `${this.isFootball ? index : market.id}-${this.activeTab && this.activeTab.id ? this.activeTab.id : ''}`;
  }

  public getTrackById(index: number, entity: any) {
    return `${entity.id}_${index}`;
  }

  public childComponentLoaded(): void {
    this.initialized = true;
  }

  /**
   * Group if markets are turn on in cms
   */
  public isEnabledOnCms(): boolean {
    return !!(this.sysConfig.yourCallPlayerStatsName && this.sysConfig.yourCallPlayerStatsName.enabled);
  }

  recalculateExpandedMarkets(event: { id: string; tab: any }, resetInit: boolean = true) {
    this.validateMarketTab(event);
    if (resetInit) {
      this.initialized = false;
    }
    this.isMTASport ? this.aggregatedMarketsGroup.forEach((m, i) => this.initOpenMarketTabs(m, i))
      : this.filteredMarketGroup.forEach((m, i) => this.initOpenMarketTabs(m, i));
  }
  /**
   * initialize controller
   */
  public init(): void {
    this.brand = environment.brand;
    let localMarketName = this.marketName;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) =>{
      this.isStatContentInfo = config.StatisticalContentInformation && config.StatisticalContentInformation.enabled;
    });

    if (localMarketName === "all-markets" && this.isMobileOnly) {
      this.showPills = true;
    } else {
      this.showPills = false;
    }
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) =>{
      this.isStatContentInfo = config.StatisticalContentInformation && config.StatisticalContentInformation.enabled;
    });
    if (this.eventEntity && !this.isSpecialEvent && this.eventTabs.length) {
      // redirecting to 404 if wrong market.
      if (!this.sport.isMarketTabCorrect(this.eventTabs, localMarketName) && !this.checkBybUrl()) {
        const edpUrl = this.routingHelperService.formEdpUrl(this.eventEntity);
        if (localMarketName === this.defaultMarketName) {
          localMarketName = 'all-markets';
        } else {
          localMarketName = this.defaultMarketName;
        }
        this.router.navigateByUrl(`${edpUrl}/${localMarketName}`);
      }
      this.checkBybTabs();
      // Select active tab.
      const renamedMainTab = _.findWhere(this.eventTabs, { id: `tab-main` });
      localMarketName = renamedMainTab && localMarketName === 'main-markets' ? 'main' : localMarketName;
      this.activeTab = _.findWhere(this.eventTabs, { id: `tab-${localMarketName}` });
      this.showYourCallContent = this.activeTab && (this.activeTab.id === 'tab-build-your-bet' || this.activeTab.id === 'tab-bet-builder');
      this.showFiveASideContent = this.activeTab && this.activeTab.id === 'tab-5-a-side';

      this.showSurfaceBets = !!this.eventEntity.id && !this.showYourCallContent && !this.showFiveASideContent;

      // Get selected market group.
      let activeLabel: string;
      if (this.checkBybUrl()) {
        const allMarkets: any = this.eventTabs.find((event: any) => event.id === this.allMarketsTab);
        if (allMarkets.pills.find((pill) => pill.marketName.includes('main'))) {
          allMarkets.pills.find((pill) => pill.marketName.includes('main')).active = true;
        } else {
          allMarkets.pills[0].active = true;
        }
        activeLabel = allMarkets.pills.find((pill) => pill.marketName.includes('main'))?.label || this.eventTabs[0].label;
        this.showPills = true;
        if (!this.activeTab) {
          this.activeTab = _.findWhere(this.eventTabs, { id: this.allMarketsTab });
        }
        this.activePill = activeLabel;
      } else if (this.showPills) {
        const allMarkets: any = this.eventTabs.find((event: any) => event.marketName === this.marketName);
        if (this.activePill) {
          allMarkets.pills.find((pill) => pill.label === this.activePill).active = true;
          activeLabel = this.activePill;
        } else {
          if (environment.brand === 'bma' && allMarkets.pills.find((pill) => pill.marketName.includes('main'))) {
            const activePillAvailable = allMarkets.pills.find((pill) => pill.active === true);
            if (activePillAvailable) {
              activeLabel = activePillAvailable.label;
            } else {
              allMarkets.pills.find((pill) => pill.marketName.includes('main')).active = true;
              activeLabel = allMarkets.pills.find((pill) => pill.marketName.includes('main')).label;
            }
          } else {
            allMarkets.pills.find((pill) => pill.marketName === this.marketName).active = true;
            activeLabel = allMarkets.pills.find((pill) => pill.marketName === this.marketName).label;
          }
          this.activePill = activeLabel;
        }
      } else {
        activeLabel = this.activeTab?.label;
      }
      this.filterAndSortMarkets(activeLabel);
    }
  }
  goToSeo(eventEntity: ISportEvent): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(eventEntity);
    this.seoDataService.eventPageSeo(eventEntity, edpUrl);
  }
  ngOnInit(): void {
    this.sportDataSubscription = this.sportEventPageProviderService.sportData
      .subscribe(this.sportDataHandler, () => this.showError());
    this.marketsOptaLinksService.getMarketLinks().subscribe((links: IMarketLinks[]) => {
      this.replaySubj.next(links);
    }
    );
    this.routeChangeListener = this.router.events.subscribe((event: Event) => {
      if(event instanceof NavigationStart) { 
        if(event?.navigationTrigger === 'popstate') {
          const history = this.routingState.getHistory();
           if(history?.length > 0) {
            const eventTabs = this.eventTabs.map(item => item.marketName);
            const isTab = eventTabs.some(item => event?.url.includes(item));
            if(isTab) {
              this.router.navigate([event?.url]);
            } else {
              const tabs = [
                'all-markets',
                'main-markets',
                'other-markets',
                ...eventTabs,
              ];
              const filterHistory = [...history].reverse().filter(item => (
               !(tabs.some(value => item.includes(value)))
                  ));
              if(filterHistory.length > 0) {
                this.routingState.setHistory([...filterHistory].reverse());
                this.router.navigate([filterHistory[0]]);
              }
            }
            
          }
        }
      } else if (event instanceof NavigationEnd) {
           this.marketName = this.activatedRoute.snapshot.paramMap.get('market');
           this.openedMarketTabsMap = {};
           this.init();
        }
       
      });
    }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('sportEventPageCtrl');
    this.replaySubj.unsubscribe();

    if (this.sportDataSubscription) {
      this.sportDataSubscription.unsubscribe();
    }

    if (this.routeChangeListener) {
      this.routeChangeListener.unsubscribe();
    }

    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  isYourCallMarket(market): boolean {
    const yourCallMarketPattern = /(YourCall)/i;
    return !!(market.templateMarketName && market.templateMarketName.match(yourCallMarketPattern));
  }

  protected sportDataHandler(data: {
    sport: IConstant,
    eventData: { event: ISportEvent },
    marketsByCollection: IMarketCollection[],
    eventTabs: ITab[],
    sysConfig: ISystemConfig,
    isSpecialEvent: boolean,
    isMTASport: boolean,
    liveMaketTemplateMarketName: string,
  }): void {
    if (data) {
      this.sport = data.sport;
      this.eventEntity = data.eventData.event[0];
      this.marketsByCollection = data.marketsByCollection;
      this.eventTabs = data.eventTabs;
      this.sysConfig = data.sysConfig;
      this.typeId = this.eventEntity.typeId;
      this.isSpecialEvent = data.isSpecialEvent;
      this.isMTASport = data.isMTASport;
      this.liveMaketTemplateMarketName = data.liveMaketTemplateMarketName;
      this.init();
      this.goToSeo(this.eventEntity);
    }

    this.hideSpinner();
  }

  /**
   * Generate your call markets without grouping
   */
  protected generateYourCallMarkets(): void {
    this.yourCallMarketAvailable = this.marketGroup && this.marketGroup.some(market => this.isYourCallMarket(market));

    if (this.yourCallMarketAvailable) {
      _.each(this.eventEntity.markets, marketEntity => {
        if (this.isYourCallMarket(marketEntity)) {
          marketEntity.showLimit = 6;
          // isAllShown - indicates whether use limit or not
          marketEntity.isAllShown = false;
          if (marketEntity.outcomes && marketEntity.outcomes.length > 0) {
            marketEntity.outcomes = this.templateService.sortOutcomesByPriceAndDisplayOrder(marketEntity.outcomes);
          }
        }
      });
    }
  }

  /**
   * Emits filter to the parent component
   * @param {any} pill
   */
  onFilterSelect(selectedPill: IPill): void {
    if(this.activePill === selectedPill.label) {
      return;
    }
    this.activePill = selectedPill.label;
    if(this.activeTab.marketName === 'all-markets') {
      this.activeTab.pills.forEach((pill) => {
        if (pill.marketName === selectedPill.marketName) {
          pill.active = true;
        } else {
          pill.active = false;
        }
      });
    }
    this.filterAndSortMarkets(selectedPill.label);
    this.recalculateExpandedMarkets(null,true);
    this.windowRefService.document.body.scrollTop = 0; // For Safari
    this.windowRefService.document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }

  private getActivePill(): string {
    const eventTab = this.eventTabs.find((tab) => tab['pills'] && tab['pills'].length) as any;
    return eventTab.pills.find((pill) => pill.label === this.activePill)?.marketName;
  }

  // To check if the edp page is opened from home page BYB.
  private checkBybUrl(): boolean {
    return this.isMobileOnly && (this.routingState.getPreviousUrl().includes('betbuilder') || this.routingState.getPreviousUrl().includes('buildyourbet')) &&
      !(_.findWhere(this.eventTabs, { id: 'tab-build-your-bet' })) && !(_.findWhere(this.eventTabs, { id: 'tab-bet-builder' }));
  }

  private filterAndSortMarkets(activeLabel: string): void {
    // Get selected market group.
    const selectedMarketGroup = _.find(this.marketsByCollection.filter(coll => coll.markets), mar => this.activeTab &&
    mar.name === activeLabel);
    if (selectedMarketGroup) {
      this.marketGroup = selectedMarketGroup.markets;
    }
    this.invokeSportExtension();
    this.generateYourCallMarkets();

    if (this.isPlayerStatsMarketsPresent()) {
      this.createPlayerStatsMarketsGroup();
    }

    this.marketGroup = _.chain(this.marketGroup)
      .sortBy(data => {
        return data.name.toLowerCase();
      })
      .sortBy('displayOrder')
      .value();

    this.is2UpAvailablePrev = this.is2upMarketAvaialable();
    this.filteredMarketGroup = _.filter(this.marketGroup, market => {
      return market.viewType !== 'marketsGroup' &&
        !market.hidden && (market.marketsGroup || (market.outcomes && market.outcomes.length > 0) || !!market.isDisplayed);
    });
    this.is2UpAvailableCurr = this.is2upMarketAvaialable();

    if (this.is2UpAvailableCurr || this.is2UpAvailablePrev) {
      this.loading = true;
      this.changeDetectorRef.detectChanges();
      this.loading = false;
    }
    if(!this.isMTASport){
      // Init opened markets tabs
      if (!Object.keys(this.openedMarketTabsMap).length) {
        this.filteredMarketGroup.forEach((m, i) => this.initOpenMarketTabs(m, i));
      }
      // Recalculate opened markets tabs states on markets count change
      if (this.filteredMarketGroup.length !== Object.keys(this.openedMarketTabsMap).length) {
        this.filteredMarketGroup.forEach((m, i) => this.insertCollapsedState(m, i));
      }    
    }

    this.sportEventPageService.transformMarkets(this.filteredMarketGroup);
    if (environment.brand === bma.brands.ladbrokes.toLowerCase()) {
      this.setFiveASideLauncher(this.activeTab);
    }

    this.replaySubj.subscribe((links: IMarketLinks[]) => {
      this.extendMarketsWithOptaLinks(this.filteredMarketGroup, this.marketConfig, links);
    });

    if(this.isMTASport){
      this.filteredMarketGroup.forEach((market) => {
        market.isAggregated = this.MTA_SORT_CODES.includes(market.marketMeaningMinorCode);
      });
      this.formAggregatedMarkets();
      if(!Object.keys(this.openedMarketTabsMap).length){
        this.aggregatedMarketsGroup.forEach((m, i) => this.initOpenMarketTabs(m, i));
      }
      if (this.aggregatedMarketsGroup.length !== Object.keys(this.openedMarketTabsMap).length) {
        this.aggregatedMarketsGroup.forEach((m, i) => this.insertCollapsedState(m, i));
      }  
    }
  }
  /**
   * Extend markets data with Opta links
   * @param {IMarket[]} markets
   * @param {IMarket[]} marketConfig
   * @param {IMarketLinks[]} optaLinks
   */
  private extendMarketsWithOptaLinks(markets: IMarket[], marketConfig, optaLinks: IMarketLinks[]): void {
    markets.forEach((market: IMarket) => {
      const marketName = this.isYourCallMarket(market) ? market.templateMarketName : market.name;
      market.marketOptaLink = optaLinks.find(optaLink => optaLink.marketName.toUpperCase() === marketName.toUpperCase());
    });
    marketConfig && marketConfig.forEach((market: IMarket) => {
      market.marketOptaLink = optaLinks.find(optaLink => optaLink.marketName.toUpperCase() === market.name.toUpperCase());
    });
  }

  private formAggregatedMarkets(){
    this.aggregatedMarketsGroup = [];
    this.filteredMarketGroup.forEach(market => {
      if(!market.isAggregated){
        this.aggregatedMarketsGroup.push(this.constructMarketTemplate(market));
      }
      else if(this.isMarketAdded(market)){
        this.associatedMarkets = this.getAssociatedMarkets(market);
        this.aggregatedMarketsGroup.push(this.constructMarketTemplate(market));
      }
    });
  }

  private isMarketAdded(market: IMarket): boolean {
    return market.marketMeaningMinorCode === 'HL' ? (this.aggregatedMarketsGroup.filter(aggregatedMarket => aggregatedMarket.marketIds.indexOf(market.id) > -1).length === 0)
     : (this.aggregatedMarketsGroup.findIndex(marketGroup => marketGroup.id === market.templateMarketId) === -1);
  }

  private constructMarketTemplate(market: IMarket){
    return {
      id: market.templateMarketId,
      marketIds: market.isAggregated ? _.pluck(this.associatedMarkets, 'id') : [market.id],
      eventId: market.eventId,
      name: market.isAggregated && this.associatedMarkets.length > 1 ? this.formatTemplateMarketName(market) : market.name,
      displayOrder: market.displayOrder,
      marketMeaningMinorCode: market.marketMeaningMinorCode,
      viewType: market.viewType,
      cashoutAvail: market.isAggregated ? this.checkForCashoutAvail() ? 'Y' : 'N' : market.cashoutAvail,
      drilldownTagNames: market.isAggregated ? this.checkForDrillDownTagNames() : market.drilldownTagNames
    };
  }

  private checkForCashoutAvail(): boolean {
    const isAnyCashoutAvailable = this.isPropertyAvailableService.isPropertyAvailable(
      this.cashOutLabelService.checkCondition.bind(this.cashOutLabelService));
    return isAnyCashoutAvailable(this.associatedMarkets, [{ cashoutAvail: 'Y' }]);
  }

  private checkForDrillDownTagNames(): string {
    const drilldownTagNames = [];
    this.associatedMarkets.forEach(market => {
      if(market.drilldownTagNames && market.drilldownTagNames != ''){
        drilldownTagNames.push(market.drilldownTagNames);
      }
    })
    return drilldownTagNames.length > 0 ? drilldownTagNames.join(',') : '';
  }

  private getAssociatedMarkets(market: IMarket): IMarket[] {
    const markets = [];
    if(market.marketMeaningMinorCode === 'HL'){
      this.filteredMarketGroup.forEach(m => {
        if(market.marketMeaningMinorCode === 'HL' && m.name.replace(m.rawHandicapValue, '') === market.name.replace(market.rawHandicapValue, '')){
          markets.push(m);
        }
      });
      return markets;
    }
    return this.filteredMarketGroup.filter(m => (m.templateMarketId === market.templateMarketId));
  }

  private formatTemplateMarketName(market: IMarket): string{
    if(market.rawHandicapValue && market.name.includes(market.rawHandicapValue)){
      const name = market.name.replace(market.rawHandicapValue, '').trim();
      return name.includes('+') ? name.replace('+', '').trim() : name;
    }
    return market.templateMarketName;
  }

  /**
   * Group your call markets to sub categories
   */
  private createPlayerStatsMarketsGroup(): void {
    const marketsGroup: any = {
      name: (this.sysConfig.yourCallPlayerStatsName && this.sysConfig.yourCallPlayerStatsName.name) || '',
      localeName: 'playerStats',
      marketsGroup: true,
      displayOrder: 0,
      markets: []
    };

    _.each(this.eventEntity.markets, marketEntity => {
      if (marketEntity.templateMarketName && marketEntity.templateMarketName.match(/(Player_Stats_)/i)) {
        marketsGroup.markets.push(marketEntity);
        marketEntity.hidden = true;
      }
    });

    marketsGroup.markets = _.sortBy(marketsGroup.markets, 'displayOrder');
    marketsGroup.displayOrder = marketsGroup.markets[0].displayOrder;

    if (!_.find(this.marketGroup, { localeName: 'playerStats' })) {
      this.marketGroup.push(marketsGroup);
    }
  }

  /**
   * Check for showing Player Stats markets
   * @return {boolean}
   */
  private isPlayerStatsMarketsPresent(): boolean {
    const playerStatsMarketPattern = /(Player_Stats_)/i;

    return this.marketGroup && this.marketGroup.some(market =>
      !!(market.templateMarketName && market.templateMarketName.match(playerStatsMarketPattern)));
  }

  /**
   * Invoke sport extension
   * @private
   */
  private invokeSportExtension(): void {
    if (this.isFootball) {
      this.footballExtension.eventMarkets(this);
    } else if (this.sportName === 'tennis') {
      this.sportsConfigSubscription = this.sportConfigService.getSport('tennis').subscribe((tennisInstance) => {
        this.tennisExtension.eventMarkets(this, tennisInstance.sportConfig);
      });
    }
  }

  private initOpenMarketTabs(market: IMarket | IMarketTemplate, index: number) {
    const keyName = this.isMTASport ? market.name : market.id;
    this.openedMarketTabsMap[keyName] = index < this.openedMarketTabsCountByDefault;
  }

  private insertCollapsedState(market: IMarket | IMarketTemplate, index: number) {
    const keyName = this.isMTASport ? market.name : market.id;
    if (this.openedMarketTabsMap[keyName] === undefined) {
      this.initOpenMarketTabs(market, index);
    }
  }

  private subscribeToEvents(): void {
    this.pubSubService.subscribe('sportEventPageCtrl', this.pubSubService.API.OUTCOME_UPDATED, () => {
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe('sportEventPageCtrl', this.pubSubService.API.MOVE_EVENT_TO_INPLAY, (ref: IReference) => {
      if (this.eventEntity && this.eventEntity.id === ref.id) {
        this.checkBybTabs();
      }
    });

    this.pubSubService.subscribe('sportEventPageCtrl', this.pubSubService.API.REMOVE_EDP_BYB_TABS, () => {
      this.removeBybTabs();
    });
  }

  private checkBybTabs(): void {
    const isLive = this.eventEntity.eventIsLive;
    const hasBybTabs = this.eventTabs && this.eventTabs.some((tab: ITab) => this.bybTabsRe.test(tab.id));
    const isQBShown = !!this.windowRefService.document.querySelector('quickbet-yourcall-wrapper');

    if (isLive && hasBybTabs && !isQBShown) {
      this.removeBybTabs();
    }
  }

  private removeBybTabs(): void {
    // redirect to all markets tab if active tab is byb or 5aside
    if (this.activeTab && this.bybTabsRe.test(this.activeTab.id)) {
      const redirectTab = this.eventTabs.find((tab: ITab) => tab.id === 'tab-all-markets');
      this.router.navigateByUrl(redirectTab.url);
      this.pubSubService.publish(this.pubSubService.API.REMOVE_BYB_STORED_EVENT, this.eventEntity.id);
    }

    // remove tabs
    this.eventTabs = this.eventTabs.filter((tab: ITab) => !this.bybTabsRe.test(tab.id));
  }

  /**
   * Validate Market on each tab change
   * @param event
   */
  private validateMarketTab(event: { id: string; tab: ITab }): void {
    if (event) {
      this.showBanner = false;
      const isAllMarketsTab: boolean = event.tab.id === this.allMarketsTab;
      if (isAllMarketsTab && (environment.brand === bma.brands.ladbrokes.toLowerCase())) {
        this.setFiveASideLauncher(event.tab);
      }
    }
  }

  /**
   * To Set Five a side Launcher
   * @param tab
   */
  private setFiveASideLauncher(tab: ITab | IMarketCollection): void {
    this.cmsService.getFeatureConfig(this.fiveASideLauncher).subscribe(
      (config: ISystemConfig) => {
        if (config && config.enabled) {
          this.fiveASideTitle = config.header;
          this.fiveASideTitle = this.fiveASideTitle.length > 23 ?
          `${this.fiveASideTitle.substring(0, 23)}...` : this.fiveASideTitle;
          this.fiveASideContent = config.description;
          this.fiveASideContent = this.fiveASideContent.length > 112 ?
          `${this.fiveASideContent.substring(0, 112)}...` : this.fiveASideContent;
          this.position = config.position;
          if (this.position > this.filteredMarketGroup.length) {
            this.position = this.filteredMarketGroup.length - 1;
          }
          const hasFiveASide = this.validateMarket(this.launcher);
          const isAllMarketsTab = tab.id === this.allMarketsTab;
          this.showBanner = hasFiveASide && isAllMarketsTab;
        }
      });
  }

  /**
   * To Check If it is correct market
   * @param market
   * @returns {boolean}
   */
  private validateMarket(market: string): boolean {
    return !!(this.eventTabs.find((tab:ITab) => tab.id === market));
  }

  private is2upMarketAvaialable(): boolean {
    const avail = this.filteredMarketGroup && this.filteredMarketGroup.some((market) => {
      return market.name && market.name.includes('2Up');
    });
    return avail;
  }

  appendDrillDownTagNames(market) {
    /* 
     * appending market name to drilldowntagname without modifying the main market 
       and passsing as args to promotion icon Component
    */
    return this.eventEntity.categoryId == '16' && market.name == this.twoUpMarketName ?
      market.drilldownTagNames ? market.drilldownTagNames + `${market.name},` : `${market.name},`
      : market.drilldownTagNames;
  }

  /**
* Statistical event handler
* @param  {ILazyComponentOutput} event
*/
  handleStatisticalEvents(event: ILazyComponentOutput): void {
    if (event.output === 'marketStatistical') {
      let cMarket = null;
      this.filteredMarketGroup.forEach((market, index) => {
        if (event.value.id === market.id || event.value.marketIds?.[0] === market.id) {
          cMarket = market;
          cMarket.isSCAvailable = event.value.isSCAvailable;
        }
      });
    }
  }

  isSingleMarketViewType(viewType: string): boolean {
    return MARKET_VIEWTYPE.WW === viewType || MARKET_VIEWTYPE.WDW === viewType ||
    MARKET_VIEWTYPE.HANDICAP_WDW === viewType || MARKET_VIEWTYPE.HANDICAP_WW === viewType ||
    MARKET_VIEWTYPE.LIST === viewType ;
  }
}
