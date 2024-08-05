/**
 * @class Race market controller To Finish, Top Finish, Place Insurance
 */
import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RacingService } from '@coreModule/services/sport/racing.service';
import environment from '@environment/oxygenEnvConfig';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RacingGaService } from '@racing/services/racing-ga.service';

@Component({
  selector: 'race-market-component',
  templateUrl: 'race-market.component.html',
  styleUrls: ['race-market.scss']
})
export class RaceMarketComponent implements OnInit, OnDestroy, OnChanges {
  @Input() isGreyhoundEdp?: boolean;
  @Input() eventEntity: ISportEvent;
  @Input() sortBy: string;
  @Input() expandedSummary: boolean[][];
  @Input() sm: string;
  @Input() hideSilk: boolean;
  @Input() market: IMarket;
  @Input() sortOptionsEnabled: boolean;
  @Input() isInfoHidden: {'info':boolean};
  @Input() isCoralDesktopRaceControls: boolean;
  isCoralDesktop: boolean = false;
  spinner = {
    isActive: false
  };
  groupedMarket: IMarket[];
  isGenericSilk: Function;
  isGreyhoundSilk: Function;
  isNumberNeeded: Function;
  raceMarketOrder: string[] = horseracingConfig.RACE_MARKET_ORDER;
  getSilkStyle: Function;
  allowFlexTabs: boolean;
  marketEntity: IMarket;
  uniqOutcomes: IOutcome[];
  isNotRacingSpecials: boolean;
  isSilkLoaded: boolean = false;
  spriteUrl: string | boolean;
  showRaceControls: boolean;
  private config;
  private readonly IMAGES_RACE_ENDPOINT: string = environment.IMAGES_RACE_ENDPOINT;

  constructor(
    // private location: Location,
    protected raceOutcomeData: RaceOutcomeDetailsService,
    protected filterService: FiltersService,
    protected locale: LocaleService,
    protected pubsubService: PubSubService,
    protected sbFiltersService: SbFiltersService,
    protected racingService: RacingService,
    protected gtmService: GtmService,
    protected racingGaService: RacingGaService
  ) {}

  ngOnInit(): void {
    this.config = horseracingConfig;
    /**
     * Check generic silk needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isGenericSilk = this.raceOutcomeData.isGenericSilk.bind(this.raceOutcomeData);

    /**
     * Check GH silk needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isGreyhoundSilk = this.raceOutcomeData.isGreyhoundSilk.bind(this.raceOutcomeData);

    /**
     * Check runner number needed
     * @param {Object} event
     * @param {Object} outcome
     * @returns {Boolean} true or false
     */
    this.isNumberNeeded = this.raceOutcomeData.isNumberNeeded.bind(this.raceOutcomeData);

    /**
     * Get Silk Image Style
     * @param {object} raceData
     * @param {object} outcomeEntity
     * @returns {string}
     */
    this.getSilkStyle = this.raceOutcomeData.getSilkStyle.bind(this.raceOutcomeData);

    /**
     * Max amount of markets tabs to use flex-tabs style
     * @member {number}
     */
    this.allowFlexTabs = this.config.MARKET_FLEX_TABS;

    /**
     * Grouped race market order
     * @member {Array}
     */
    this.raceMarketOrder = this.config.RACE_MARKET_ORDER;

    this.isNotRacingSpecials = !this.racingService.isRacingSpecials(this.eventEntity);

    this.marketEntity = this.getRaceMarkets(this.eventEntity.markets).length && this.getRaceMarkets(this.eventEntity.markets)[0];
    if (this.marketEntity) {
      this.uniqOutcomes = this.getUniqueOutcomes(this.marketEntity);

      _.each(this.uniqOutcomes, (outcome: IOutcome) => {
        this.setOutcomeFavourite(outcome);
        this.expandedSummary.push([false]);
      });
    }
    this.pubsubService.subscribe('RaceMarketComponent', this.pubsubService.API.OUTCOME_UPDATED, () => {
      this.updateEventMarkets();
    });
    this.pubsubService.subscribe(
        'RaceMarketComponent',
        [this.pubsubService.API.DELETE_EVENT_FROM_CACHE, this.pubsubService.API.DELETE_MARKET_FROM_CACHE],
        (marketId: string) => {
          this.updateEventMarkets();
          const sortedMarkets = _.find(this.eventEntity.sortedMarkets,
              (markets: IMarket) => markets.label === this.sm);

          if (!sortedMarkets) {
            return;
          }
          sortedMarkets.header = [];
          sortedMarkets.markets.forEach((market) => {
            if (market.id === marketId) {
              const marketIndex = _.findIndex(sortedMarkets.markets, { id: marketId });
              sortedMarkets.markets.splice(marketIndex, 1);
            } else {
              this.racingService.setGroupedMarketHeader(sortedMarkets, market);
            }
          });
        });
    this.showRaceControls = this.isCoralDesktopRaceControls?false:true;
    this.spriteUrl = this.getSprites();
  }

  getSprites(): string | boolean {
    if(this.marketEntity && this.marketEntity.outcomes){
    const racingIds = this.marketEntity.outcomes.filter(outcome => outcome.racingFormOutcome && outcome.racingFormOutcome.silkName)
      .map((outcome) => outcome.racingFormOutcome.silkName.split('.')[0]);
    return racingIds.length ? `${this.IMAGES_RACE_ENDPOINT}/${[...racingIds].sort((a, b) => a < b ? -1 : a > b ? 1 : 0)}` : this.isSilkLoaded = true;
    }
  } 

  toggleShowOptions(expandedSummary: Array<Array<boolean>>, showOption: boolean): void {
    if (expandedSummary && expandedSummary[0]) {
      for (let i = 0; i < expandedSummary[0].length; i++) {
        expandedSummary[0][i] = showOption;}
      }
  }

  onExpandSection(expandedSummary: boolean[][], oIndex: number): void {
    expandedSummary[0][oIndex] = !expandedSummary[0][oIndex];
    const hideInfoChecker: boolean = expandedSummary[0].every((v: boolean) => v === false);
    this.isInfoHidden = { 'info': !hideInfoChecker };
    const gtmData = {
      event: "trackEvent",
      eventAction: "race card",
      eventCategory: this.isGreyhoundEdp?'greyhounds':'horse racing',
      eventLabel: expandedSummary[0][oIndex] ? 'show more':'show less',
      categoryID:this.eventEntity.categoryId,
      typeID:this.eventEntity.typeId,
      eventID:  this.eventEntity.id
    }
    this.gtmService.push(gtmData.event,gtmData);
  }
  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  trackById(index, value) {
    return value.id;
  }

  getFilteredName(name: string): string {
    return this.filterService.removeLineSymbol(name);
  }

  nameWithoutNonRunner(name: string): string {
    return this.filterService.removenNonRunnerFromHorseName(name);
  }

  ngOnChanges(changes: SimpleChanges) {
    const isSortByChanged = changes.sortBy && changes.sortBy.currentValue !== changes.sortBy.previousValue;
    if (changes.eventEntity || changes.sm || isSortByChanged) {
      this.updateEventMarkets();
    }
  }

  ngOnDestroy () {
    this.pubsubService.unsubscribe('RaceMarketComponent');
  }

  getDefaultSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
    return !outcomeEntity.racingFormOutcome && eventEntity.sportId === horseracingConfig.config.request.categoryId;
  }

  /**
   * Display race markets
   * @param {Array} markets
   * @return {Boolean}
   */
  getRaceMarkets(markets: IMarket[]): IMarket[] {
    this.groupedMarket = markets.filter( (market: IMarket) => this.displayMarketPanel(market));
    this.groupedMarket = this.filterService.orderBy(this.groupedMarket, this.raceMarketOrder);

    return this.groupedMarket;
  }

  /**
   * Display market panel
   * @param {Object} marketEntity
   * @return {Boolean}
   */
  displayMarketPanel(marketEntity: IMarket): boolean {
    const isSelected = this.sm === marketEntity.label,
      isTopFinishSelected = this.sm === this.locale.getString('sb.topFinishMarkets') &&
        marketEntity.isTopFinish && !marketEntity.collapseMarket,
      isToFinishSelected = this.sm === this.locale.getString('sb.toFinishMarkets') &&
        marketEntity.isToFinish && !marketEntity.collapseMarket,
      insuranceSelected = this.sm === this.locale.getString('sb.insuranceMarkets') &&
        marketEntity.insuranceMarkets && !marketEntity.collapseMarket,
      isOtherSelected = this.sm === this.locale.getString('sb.otherMarkets') &&
        marketEntity.isOther && !marketEntity.collapseMarket,
      isWOSelected = this.sm === this.locale.getString('sb.bettingWithout') &&
        marketEntity.isWO && !marketEntity.collapseMarket;

    return isSelected || isTopFinishSelected ||
      isToFinishSelected || insuranceSelected ||
      isOtherSelected || isWOSelected;
  }

  /**
   * Get all groupped markets outcomes
   * @return {Array}
   */
  getUniqueOutcomes(raceMarket: IMarket): IOutcome[] {
    let outcomesMap = [];
    const sortedMarkets = _.sortBy(this.groupedMarket, 'customOrder');

    _.each(sortedMarkets, (market: IMarket) => {
      outcomesMap = outcomesMap.concat(market.outcomes);
    });

    const uniqueOutcomes = _.uniq(outcomesMap, outcome => {
      return outcome.name;
    });

    return this.sortOutcomes(uniqueOutcomes, raceMarket.isLpAvailable);
  }

  /**
   * Find if market is grouped
   * @params {object} market
   * @return {object}
   */
  isGroupedRaceMarket(market: IMarket): string {
    return _.find(this.config.GROUPED_MARKETS_NAME, (marketName: string) => {
      return marketName === market.name;
    });
  }

  /**
   * Get and sort related grouped markets header
   * @param {object} market
   * @param {object} eventEntity
   * @returns {array}
   */
  getHeader(market: IMarket, eventEntity: ISportEvent) {
    if (market.isTopFinish || market.insuranceMarkets || market.isToFinish) {
      const groupedMarket: IMarket = _.find(eventEntity.sortedMarkets,
        (markets: IMarket) => markets.name === this.sm);
      if (groupedMarket) {
        return _.sortBy(groupedMarket.header);
      }
    }
    return null;
  }

  /**
   * Get market price type SP/LP
   * @param {array} outcomes
   * @param {string} name
   * @returns {object}
   */
  getOutcomeForRaceMarket(outcomes: IOutcome[], name: string) {
    return _.find(outcomes, outcome => outcome.name === name);
  }

  /**
   * Get market price type SP/LP
   * @param {object} marketEntity
   * @param {object} outcomeEntity
   * @param {boolean} isFavourite
   * @returns {string}
   */
  definePriceType(marketEntity: IMarket, outcomeEntity: IOutcome, isFavourite: boolean): string {
    return (marketEntity.isSpAvailable &&
      (!marketEntity.isLpAvailable ||
        (marketEntity.isLpAvailable && !outcomeEntity.prices.length))) ||
    isFavourite ? 'SP' : 'LP';
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

  /**
   * @param {Object} marketEntity
   * @param {Object} outcomeEntity
   * @return {Boolean}
   */
  isHistoricPrices(marketEntity: IMarket, outcomeEntity: IOutcome): boolean {
    return !this.getOutcomeForRaceMarket(marketEntity.outcomes, outcomeEntity.name).isFavourite &&
      this.definePriceType(marketEntity, outcomeEntity, outcomeEntity.isFavourite) !== 'SP';
  }

  /**
   * Define price type
   * @param {Object} marketEntity
   * @param {Object} outcomeEntity
   * @return {String}
   */
  defPriceType(marketEntity: IMarket, outcomeEntity: IOutcome): string {
    const outcome = this.getOutcomeForRaceMarket(marketEntity.outcomes, outcomeEntity.name);
    return this.definePriceType(marketEntity, outcome, outcome.isFavourite);
  }

  /**
   * @param {Object} outcomeEntity
   * @return {Boolean}
   */
  isNumber(outcomeEntity: IOutcome): boolean {
    return this.isNumberNeeded(this.eventEntity, outcomeEntity) && !outcomeEntity.isFavourite;
  }

  private sortOutcomes(outcomes: IOutcome[], isLpAvailable: boolean): IOutcome[] {
    const isByPrice = this.sortBy === 'Price';
    const isByNumber = !isLpAvailable || this.sortBy === 'Racecard';
    const isHasPrice = isLpAvailable && isByPrice;
    return this.sbFiltersService.orderOutcomeEntities(outcomes, isHasPrice, true, isByNumber, false,
      false, this.eventEntity.categoryCode === 'GREYHOUNDS');
  }

  private updateEventMarkets(): void {
    this.marketEntity = this.getRaceMarkets(this.eventEntity.markets)[0];
    this.uniqOutcomes = this.marketEntity ? this.getUniqueOutcomes(this.marketEntity) : [];
  }
  /**
  * Updates GTMservice with greyhound data
  * @param showOption:  option
  */
 public toggleShowOptionsGATracking(showOption: boolean): void {
  this.racingGaService.toggleShowOptionsGATracking(this.eventEntity, showOption, this.isGreyhoundEdp);
}
}
