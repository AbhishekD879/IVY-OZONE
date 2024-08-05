import { Component, OnInit, Input, OnChanges, SimpleChanges, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

import { TimeService } from '@core/services/time/time.service';
import environment from '@environment/oxygenEnvConfig';
import { EventService } from '@sb/services/event/event.service';
import { mediaDrillDownNames } from '@shared/constants/media-drill-down-names';
import { ICategoriesData } from '@shared/models/categories-data.model';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TemplateService } from '@shared/services/template/template.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { ISportConfig } from '@core/services/cms/models';
import { IEventMarketConfig } from '@app/core/models/event-market-config.model';
import { handicapTemplateMarketName } from '@app/shared/constants/odds-card-constant';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ILazyComponentOutput } from '../lazy-component/lazy-component.model';
@Component({
  selector: 'odds-card-component',
  templateUrl: 'odds-card.component.html'
})

export class OddsCardComponent implements OnInit, OnChanges {

  @Input() event: ISportEvent;
  @Input() showLocalTime?: string | boolean;
  @Input() eventType?: string;
  @Input() selectedMarket?: string;
  @Input() widget?: string;
  @Input() featured?: { isSelection: boolean };
  @Input() limitSelections?: boolean | number;
  @Input() isFilterByTemplateMarketName?: boolean;
  @Input() gtmModuleTitle?: string;
  @Input() sportConfig?: ISportConfig;
  @Input() isMarketSwitcherConfigured?: boolean;
  @Input() isFootballCoupon?:boolean;
  @Input() showBoard?:boolean;
  @Input() couponIndex?:any;
  @Input() eventIndex?:any;
  @Input() dateIndex?:any;
  @Input() eventQuickSwitch: boolean;
  @Output() readonly expand?: EventEmitter<ISportEvent> = new EventEmitter<ISportEvent>();

  @Output() readonly goToEventCallback: EventEmitter<number> = new EventEmitter<number>();
  @Output() readonly marketUndisplayed: EventEmitter<IMarket> = new EventEmitter<IMarket>();

  eventTime: string;
  eventFirstName: string;
  eventSecondName: string;
  eventThirdName: string;
  racingData: ICategoriesData;

  isEnhancedMultiplesCard: boolean;
  isSpecialCard: boolean;
  isOutrightsCard: boolean;
  isListTemplate: boolean = false;
  isMultiMarketTemplate: boolean = false;
  isStream: boolean;
  eventName: string;
  nameOverride: string;
  selectedMarketObject: any;
  startTime: any;
  isRacing: boolean;
  localTime: string;
  sportType: string;
  eventStartedOrLive: boolean;
  isEnhancedMultiples: boolean;
  template: any;

  displayMarketConfig: IEventMarketConfig;

  private matchResultMarket: IMarket;
  private readonly MEDIA_DRILL_DOWN_NAMES: Array<string> = mediaDrillDownNames;
  private readonly FOOTBALL_ID: string = environment.CATEGORIES_DATA.footballId;

  constructor(
    private eventFactory: EventService,
    private marketTypeService: MarketTypeService,
    private timeService: TimeService,
    private filters: FiltersService,
    private routingHelper: RoutingHelperService,
    private templateService: TemplateService,
    private router: Router,
    private sportsConfigHelperServive: SportsConfigHelperService,
    private seoDataService: SeoDataService,
    private gtmService: GtmService
  ) {
    this.racingData = environment.CATEGORIES_DATA.racing;
  }

  callGoToEventCallback() {
    this.goToEventCallback.emit();
  }

  /**
   * Initializes all variables (private and public)
   * @private
   */
  ngOnInit(): void {
    this.init();
    if (this.sportConfig) {
      this.sportType = this.sportConfig.config.path;
      this.updateDisplayMarket(this.sportConfig);
    } else {
      this.sportsConfigHelperServive.getSportPathByCategoryId(Number(this.event.categoryId))
        .subscribe((sportPath: string) => {
          this.sportType = sportPath;
        });
    }
  }
  init(): void {
    this.matchResultMarket = this.event.markets.length && _.find(this.event.markets, { name: 'Match Result' });
    this.templateService.switcher = this.isMarketSwitcherConfigured;
    this.template = this.templateService.getTemplate(this.event);
    this.isEnhancedMultiples = this.templateService.isMultiplesEvent(this.event);
    this.localTime = this.timeService.getLocalHourMin(this.event.startTime);
    this.eventStartedOrLive = (this.event.isStarted || this.event.eventIsLive);

    this.isEnhancedMultiplesCard = (this.template.name === 'Enhanced Multiples') &&
      !this.event.hideEvent && this.isEnhancedMultiples;
    this.isSpecialCard = this.eventType === 'specials' && !this.isEnhancedMultiples;
    this.isStream = this.isStreamAvailable();
    this.eventName = this.event.nameOverride || this.event.name;
    this.nameOverride = this.event.nameOverride;
    this.selectedMarketObject = this.getSelectedMarket();
    this.isOutrightsCard = this.template.name === 'Outrights' && !this.eventType;
    this.startTime = new Date(this.event.startTime);

    this.isRacing = !!(_.find(this.racingData, (sport: any) => Number(sport.id) === Number(this.event.categoryId)));

    // Stream event
    _.extend(this.event, this.eventFactory.isLiveStreamAvailable(this.event));

    // Event start time
    this.eventTime = this.timeService.getEventTime(`${this.startTime}`);

    if (this.eventName) {
      // Event Teams Name
      this.eventFirstName = this.filters.getTeamName(this.eventName, 0);
      this.eventSecondName = this.filters.getTeamName(this.eventName, 1);
      this.eventThirdName = this.filters.getTeamName(this.eventName, 2);
    }
    this.checkTemplateType();
  }
  
  eventDisplayed(market: IMarket): boolean {
    return market.isResulted || !!market.outcomes.length;
  }

  onExpand(): void {
    this.expand.emit(this.event);
    const gtmData = {
      "event": "trackEvent",
      "eventAction": "click",
      "eventCategory": "coupon stats widget",
      "eventLabel": this.showBoard ? 'hide stats' : 'show stats',
      "categoryID": this.event.categoryId,
      "typeID": this.event.typeId,
      "eventID": this.event.id
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.event || changes.selectedMarket) {
      this.watchHandler();
    }
  }

  /**
   * Checks if odds card is sport one
   * @param market
   * @returns {boolean}
   */
  isSportCard(market: any): boolean {
    return ((!!this.featured || this.isSelectedMarket(market))
      && !this.isEnhancedMultiplesCard
      && (this.template.name !== 'Outrights')
      && !this.isSpecialCard);
  }

  /**
   * Check if it Selected Market
   * @param {IMarket} market
   * @returns {boolean}
   */
  isSelectedMarket(market: IMarket): boolean {
    if (this.selectedMarket) {
      const marketFilterList = this.selectedMarket.toLowerCase().split(',');
      return marketFilterList.indexOf(market.templateMarketName.toLowerCase()) !== -1
        || marketFilterList.indexOf(market.name.toLowerCase()) !== -1;
    }

    return true;
  }

  /**
   * Checks if event is live
   * @returns {boolean}
   */
  get isLive(): boolean {
    return this.eventStartedOrLive;
  }
  set isLive(value:boolean){}

  /**
   * Redirects to event details page
   * @param justReturn
   * @param event
   * @returns {*}
   */
  goToEvent(justReturn: boolean, event?: any): string | boolean {
    const edpUrl: string = this.routingHelper.formEdpUrl(this.event);

    if (!justReturn && !this.isEnhancedMultiples && !this.event.isFinished) {
      this.callGoToEventCallback();
      this.router.navigateByUrl(edpUrl);
    }

    return edpUrl;
  }

  goToSeo(): void {
    const edpUrl: string = this.routingHelper.formEdpUrl(this.event);
    this.seoDataService.eventPageSeo(this.event, edpUrl);
  }
  /**
   * CHecks if stream is available
   * @returns {boolean}
   * @private
   */
  isStreamAvailable(): boolean {
    return this.event.liveStreamAvailable && this.showStreamIcon();
  }

  changeCardView(changedMarket: IMarket): void {
    if (!changedMarket.isDisplayed) {
      if (this.sportConfig.config.request.categoryId !== this.FOOTBALL_ID) {
        this.event.markets = this.event.markets.filter(market => market.id !== changedMarket.id);
      }
      this.updateDisplayMarket(this.sportConfig);
      this.marketUndisplayed.emit(changedMarket);
    }
  }
  handleOutput(output: ILazyComponentOutput) {
    output.output === 'goToEventCallback' ? this.callGoToEventCallback() : this.changeCardView(output.value);
  }
  private updateDisplayMarket(sportConfig: ISportConfig): void {
    if ((!environment.CATEGORIES_DATA.categoryIds.includes(this.sportConfig.config.request.categoryId) || !this.isMarketSwitcherConfigured)
      && (sportConfig.config.request.categoryId !== this.FOOTBALL_ID)) {
        let marketNames = this.marketTypeService.extractMarketNameFromEvents([JSON.parse(JSON.stringify(this.event))], this.isFilterByTemplateMarketName);
        const marketNamesList = this.marketTypeService.extractMarketNameFromEvents([JSON.parse(JSON.stringify(this.event))],true);
        marketNames = _.uniq(marketNames.concat(marketNamesList));
        if (marketNames && marketNames.includes('Match Result')) { 
          (marketNames).push('Match Betting'); 
        }
        const config = sportConfig.config;
        const isGolfOutright = (config.request.categoryId === environment.CATEGORIES_DATA.golfId && config.oddsCardHeaderType === '' && config.isOutrightSport);
        const intersects = isGolfOutright ? marketNames.join(',') : config.request.marketTemplateMarketNameIntersects;
        if (isGolfOutright) {
        this.event.marketsCount = this.event.markets.length;
      }
      this.displayMarketConfig = this.marketTypeService.getDisplayMarketConfig(
        intersects, this.event.markets);
      this.isOutrightsCard = this.isOutrightsCard || this.displayMarketConfig.displayMarketName === handicapTemplateMarketName;
      const hasMarket = this.selectedMarket ? _.intersection(this.selectedMarket.split(','), marketNames).length > 0 : false;
      if (!hasMarket) {
        this.selectedMarket = this.displayMarketConfig.displayMarketName;
        this.selectedMarketObject = this.displayMarketConfig.displayMarket;
      }
        this.checkTemplateType();
    }
  }

  /**
   * Watcher for necessary variables
   */
  private watchHandler(): void {
    this.init();
  }

  /**
   * Gets selected market object
   * @returns {*}
   * @private
   */
  private getSelectedMarket(): IMarket {
    if (this.matchResultMarket && !this.selectedMarket) {
      this.selectedMarket = 'Match Result';
    }
    return this.event.markets[this.marketIndex(this.event.markets)];
  }

  /**
   * Get Market Index
   * @param markets
   * @returns {number}
   */
  private marketIndex(markets: IMarket[]): number {
    const index: number = _.findIndex(markets, market => this.isSelectedMarket(market));
    return (index === -1) ? 0 : index;
  }

  /**
   * Checks if in drilldownTagNames property of event are two or more providers
   * @returns {boolean}
   * @private
   */
  private showStreamIcon(): boolean {
    const eventDrilldownTagNames = this.event.drilldownTagNames ? this.event.drilldownTagNames.split(',') : [];
    return _.intersection(eventDrilldownTagNames, this.MEDIA_DRILL_DOWN_NAMES).length > 0;
  }

/**
 * Check for ListTemplate
 * @private
 */
  private checkTemplateType(): void {
    this.isMultiMarketTemplate = false;
    if(!(this.event.markets.length ? this.event.markets[0].dispSortName : '')){
      this.isListTemplate = false;
    }
    if (this.selectedMarket) {
      this.isListTemplate = this.isMarketSwitcherConfigured ? this.templateService.isListTemplate(this.selectedMarket) : false;
      this.isMultiMarketTemplate = this.templateService.isMultiMarketTemplate(this.selectedMarket);
    }
  }
}
