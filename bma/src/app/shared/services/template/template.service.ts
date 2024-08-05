import * as _ from 'underscore';
import { Injectable } from '@angular/core';

import { ISportEvent, ISportEventGroup } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { IOutcome } from '@core/models/outcome.model';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { ITemplate } from '@core/models/template.model';
import { IMarket } from '@core/models/market.model';
import { TimeService } from '@core/services/time/time.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISportCategory } from '@core/services/cms/models';
import { ISportViewTypes } from '@core/models/sports-view-types.model';

import { MARKETS_GROUP } from '@sharedModule/constants/markets-group.constant';
import { IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IQuickbetReceiptLegPartsModel } from '@app/quickbet/models/quickbet-receipt.model';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';

import { MARKETS_COLUMNS, UNDEFINED_SORTCODE,BOOST_MARKET } from './template.constant';
interface ISortOutcomesInterface {
  [key: number]: Function;
  [key: string]: Function;
}

@Injectable()
export class TemplateService {
  undefinedKeys: Array<Object> = Object.keys(UNDEFINED_SORTCODE);
  undefinedFlag: boolean = false;
  public popularScorer: boolean = false;
  public otherScorer: boolean = false;
  marketList: IMarket[];
  switcher : boolean;
  private popularMarkets: string[] = ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 Or More'];
  private otherMarkets: string[] =  ['Hat trick', 'Last Goalscorer'];
  private sortCode: string[] = ['2W','L2','BO'];
  private sortCode2: string[] = ['3W','L3'];
  private sortCodeList: string[] = ['2W','L2','BO','3W','L3'];


  private readonly SORT_OUTCOMES: ISortOutcomesInterface = {
    'FS,LS,HS,MG,AG': this.sortOutcomesByPrice,
    HL: this.sortByMeaningMinorCode,
    '2W,L2,BO': _.partial(this.addOutcomeMeaningMinorCode, 2),
    '3W,L3': _.partial(this.addOutcomeMeaningMinorCode, 3),
    CS: this.sortCS
  };

  constructor(
    private filter: FiltersService,
    private timeService: TimeService,
    private locale: LocaleService,
    private cmsProvider: CmsService,
    private windowRef: WindowRefService
  ) {
  }

  genericSportMarketsTemplate(): Object {
    return ((columns: any, method: Function) => {
      const marketsTemplate: Object = {};
      _.each(columns, (columnsNumber: string, marketMeaningMinorCode: string) => {
        marketsTemplate[marketMeaningMinorCode] = {
          columns: columnsNumber,
          SORT_OUTCOMES: method(marketMeaningMinorCode)
        };
      });
      return marketsTemplate;
    })(MARKETS_COLUMNS, this.findSortFunction.bind(this));
  }


  /**
   * Sort outcomes by price
   * @param outcomesArray {array}
   * @return {array}
   */
  sortOutcomesByPrice(outcomesArray: IOutcome[]): IOutcome[] {
    return outcomesArray.sort((a, b) => {
      if (a.prices && a.prices[0] && b.prices && b.prices[0]) {
        return Number(a.prices[0].priceDec) - Number(b.prices[0].priceDec);
      }
    });
  }

  sortByMeaningMinorCode(outcomesArray: IOutcome[]): IOutcome[] {
    return outcomesArray[0].isUS ? _.sortBy(outcomesArray, 'outcomeMeaningMinorCode') : outcomesArray;
  }

  /**
   * add Outcome Meaning Minor Code to outcomes
   * @param outcomesArray
   * @param columnsCount
   * @returns {Array|*}
   */
  addOutcomeMeaningMinorCode(columnsCount: number, outcomesArray: IOutcome[]): IOutcome[] {
    return outcomesArray.map((outcomeEntity: IOutcome, outcomeIndex: number) => {
      // eslint-disable-next-line no-mixed-operators
      outcomeEntity.outcomeMeaningMinorCode = (outcomeIndex % columnsCount + 1);
      return outcomeEntity;
    });
  }

  sortCS(outcomesList: IOutcome[]): IOutcome[] {
    function getCorrectedOutcomesForCorrectScoreMarkets(outcomesArray) {
      for (let i = 0, outcomesLength = outcomesArray.length; i < outcomesLength; i++) {
        if (outcomesArray[i].outcomeMeaningScores) {
          const scores = outcomesArray[i].outcomeMeaningScores.split(',').slice(0, -1);
          outcomesArray[i].csOutcomeOrder = Number(scores[1]);
          outcomesArray[i].outcomeMeaningMinorCode = 3;
          if (Number(scores[0]) > Number(scores[1])) {
            outcomesArray[i].outcomeMeaningMinorCode = 1;
            outcomesArray[i].csOutcomeOrder = Number(scores[0]);
          } else if (Number(scores[0]) === Number(scores[1])) {
            outcomesArray[i].csOutcomeOrder = Number(scores[0]);
            outcomesArray[i].outcomeMeaningMinorCode = 2;
          }
        }
      }

      return outcomesArray;
    }
    return _.sortBy(getCorrectedOutcomesForCorrectScoreMarkets(_.sortBy(outcomesList, 'name')), 'csOutcomeOrder');
  }

  findSortFunction(marketMeaningMinorCode: string): Function {
    let sortOutcomesFunc: Function;
    _.each(this.SORT_OUTCOMES, (sortFunction, key) => {
      if (key.toString().indexOf(marketMeaningMinorCode) !== -1) {
        sortOutcomesFunc = sortFunction;
      }
    });
    // eslint-disable-next-line
    return sortOutcomesFunc || function (outcomesArray: IOutcome[]) {
      return outcomesArray;
    };
  }

  isOutrightSport(code: string): boolean {
    return _.indexOf(OUTRIGHTS_CONFIG.outrightsSports, code) !== -1;
  }

  getPopularScorer(){
    return this.popularScorer;
  }

  getOtherScorer(){
    return this.otherScorer;
  }

  /**
   * Get the template type and name from event.
   *
   * Usage:
   * variable.template = getTemplate(evt);
   *
   * @param event
   * @returns {{type: number, name: string}}
   */
  getTemplate(event: ISportEvent): ITemplate {
    const template: ITemplate = {
      type: 2, // default
      name: ''
    };

    if (this.windowRef.nativeWindow.location.href.includes('fanzone')) {
      template.type = 1;
      template.name = 'Regular';
    } else {
      if (event.typeName === 'Enhanced Multiples') {
          template.name = 'Enhanced Multiples';
        } else if (!event.markets.length) {
          template.name = 'Outrights';
        } else if (OUTRIGHTS_CONFIG.sportSortCode.indexOf(event.eventSortCode) !== -1 ||
          (event.eventSortCode === 'MTCH' && this.isOutrightSport(event.categoryCode)) ||
          (event.eventSortCode === 'MTCH' && event.categoryCode.toLowerCase() === environment.CATEGORIES_DATA.golfSport
            && (environment.CATEGORIES_DATA.specialMarkets.includes(event.typeName) ||
              (event.drilldownTagNames && event.drilldownTagNames.includes(environment.CATEGORIES_DATA.specialTagCode))))) {
          template.name = event.outcomeId ? 'outrightsWithSelection' : 'Outrights';
          if(this.switcher) {
            template.name = event.categoryId === '18' ? 'Regular' : template.name;
          }
        } else if (OUTRIGHTS_CONFIG.sportSortCode.indexOf(event.eventSortCode) === -1) {
          const marketMeaningMinorCode = event.markets[0].marketMeaningMinorCode;
          if (event.markets[0].outcomes.length > 1 && !event.outcomeStatus) {
            template.type = 1;
            if (marketMeaningMinorCode && (['HH', 'MR'].indexOf(marketMeaningMinorCode) !== -1)) {
              template.name = 'Regular';
            } else {
              template.name = 'Two or three ways';
            }
          } else {
            template.name = 'One way';
          }
        } else {
          template.name = 'Enhanced Multiples';
        }
    }
    return template;
  }

  /**
   * get Generic Sport Markets view Template For Exceptions (By Outcomes Count)
   *
   * @param outcomesCount
   * @returns {*}
   */
  getMarketsColumnsNumberForExceptions(outcomesCount: number): string {
    if (outcomesCount == 1) {
      return 'List';
    }
    if (outcomesCount == 2) {
      return 'WW';
    }
    if (outcomesCount == 3) {
      return 'WDW';
    }
    if (outcomesCount >= 4) {
      return 'List';
    }
  }

  /**
   * set OutcomeMeaningMinorCode For Exceptions (By Outcomes Count)
   *
   * @param outcomesArray
   * @param markets
   * @returns {*}
   */
  setOutcomeMeaningMinorCodeForExceptions(outcomesArray: IOutcome[], markets: IMarket[]): IOutcome[] {
    const columnsCount: number = outcomesArray.length < 24 ? 2 : 3;
    const marketsArray: IMarket[] = _.flatten(_.map(markets, (market: IMarket) => {
      return _.filter(market.outcomes, (outcome: IOutcome) => !!(outcome && outcome.outcomeMeaningMinorCode));
    }));
    _.each(outcomesArray, (outcome: IOutcome, index) => {
      const minorCode: IMarket = _.findWhere(marketsArray, { name: outcome.name });
      // eslint-disable-next-line no-mixed-operators
      outcome.outcomeMeaningMinorCode = minorCode ? minorCode.outcomeMeaningMinorCode : (index % columnsCount + 1);
      outcome.outcomeMeaningMinorCode = this.getCorrectedOutcomeMeaningMinorCode(outcome);
    });
    return outcomesArray;
  }

  /**
   * sorts outcomes By Price and Name
   *
   * @param outcomesArray
   * @returns {*}
   */
  sortOutcomesByPriceAndName(outcomesArray: IOutcome[]): IOutcome[] {
    return _.sortBy((_.sortBy(outcomesArray, 'prices[0].priceDec')), 'name');
  }
  sortOutcomesByPriceAndDisplayOrder(outcomesArray: IOutcome[]): IOutcome[] {
    return _.sortBy(this.sortOutcomesByPrice(outcomesArray), 'displayOrder');
  }

  /**
   * returns market With Sorted Outcomes
   *
   * @param marketEntity
   * @param markets
   * @returns {*}
   */
  getMarketWithSortedOutcomes(marketEntity: IMarket, markets?: IMarket[]): IOutcome[] {
    let outcomesArray: IOutcome[] = marketEntity.outcomes;
    if (_.has(marketEntity, 'marketMeaningMinorCode')) {
      if (_.has(outcomesArray[0], 'outcomeMeaningMinorCode')) {
        outcomesArray = outcomesArray.map((outcomeEntity: IOutcome) => {
          outcomeEntity.originalOutcomeMeaningMinorCode = outcomeEntity.outcomeMeaningMinorCode as string;
          outcomeEntity.outcomeMeaningMinorCode = this.getCorrectedOutcomeMeaningMinorCode(outcomeEntity);
          return outcomeEntity;
        });
        outcomesArray = _.sortBy(outcomesArray, 'outcomeMeaningMinorCode');
      }
      else {
        outcomesArray = _.sortBy(outcomesArray, 'displayOrder');
      }
      if(this.sortCode.includes(marketEntity.dispSortName)){
        this.addOutcomeMeaningMinorCode(2,outcomesArray);
      }
      if(this.sortCode2.includes(marketEntity.dispSortName)){
        this.addOutcomeMeaningMinorCode(3,outcomesArray);
      }
      if (marketEntity.marketMeaningMinorCode !== '--' && !this.undefinedFlag) {
        outcomesArray = this.genericSportMarketsTemplate()[marketEntity.marketMeaningMinorCode].SORT_OUTCOMES(outcomesArray);
      }
      if ((marketEntity.marketMeaningMinorCode === '--' && !this.sortCodeList.includes(marketEntity.dispSortName)) || (this.undefinedFlag && !this.sortCodeList.includes(marketEntity.dispSortName))) {
        outcomesArray = this.setOutcomeMeaningMinorCodeForExceptions(this.sortOutcomesByPriceAndName(outcomesArray), markets);
      }
      if(this.getMarketViewType(marketEntity) === 'List') {
        outcomesArray = _.sortBy(_.sortBy(outcomesArray, 'name'), 'displayOrder');
      }
      if(this.isGetAPriceMarket(marketEntity)) {
        outcomesArray = this.sortOutcomesByPriceAndDisplayOrder(outcomesArray);
      }
    } else {
      outcomesArray = this.setOutcomeMeaningMinorCodeForExceptions(this.sortOutcomesByPriceAndName(outcomesArray), markets);
    }
    return outcomesArray;
  }

  /**
   * Returns correct view for market
   *
   * @returns {string}
   */
  getMarketViewType(marketEntity: IMarket, sportName?: string): string {
    const footballSportName = 'football';
    this.undefinedFlag = false;
    let marketColumnsCount: string | number;
    if (marketEntity.marketMeaningMinorCode) {
      if (marketEntity.marketMeaningMinorCode === 'CS') {
        return 'Correct Score';
      }
      if (marketEntity.marketMeaningMinorCode === '--' && (BOOST_MARKET.includes(marketEntity.templateMarketName))) {
        return 'List';
      }
      if(this.isGetAPriceMarket(marketEntity)){
        return 'List';
      }
      for (const key of this.undefinedKeys) {
        if (key === marketEntity.marketMeaningMinorCode) {
          this.undefinedFlag = true;
          break;
        } else {
          this.undefinedFlag = false;
        }
      }
      if (!this.undefinedFlag && marketEntity.marketMeaningMinorCode !== '--') {
        marketColumnsCount = this.genericSportMarketsTemplate()[marketEntity.marketMeaningMinorCode].columns;
      }
      if (this.undefinedFlag || marketEntity.marketMeaningMinorCode === '--') {
        marketColumnsCount = this.getMarketsColumnsNumberForExceptions(marketEntity.outcomes.length);
      }
    } else {
      marketColumnsCount = this.getMarketsColumnsNumberForExceptions(marketEntity.outcomes.length);
    }
    // Set correct ViewType to marketsGroup
    this.checkGoalScorerMarket();
    const newMarketGroup = MARKETS_GROUP.filter(market => {
      return !((market.name === 'Popular Goalscorer Markets' && !this.popularScorer)
        || (market.name === 'Other Goalscorer Markets' && !this.otherScorer));
    });
    const marketsGroup: string[] = _.flatten(_.map(newMarketGroup, (market: IMarket) => {
      return market.periods ? _.pluck(market.periods, 'marketsNames') : market.marketsNames;
    }));
    if ((sportName && sportName === footballSportName) &&
      _.contains(marketsGroup, marketEntity.templateMarketName)) {
      return 'marketsGroup';
  }
    return `${marketColumnsCount}`;
  }

  getSportViewTypes(sportName): ISportViewTypes {
    // TODO: fill with all sport names, according to competition naming rules
    const sportsWithClassNames = ['football', 'basketball', 'icehockey', 'baseball', 'tvspecials', 'politics',
      'handball', 'aussierules', 'bowls', 'volleyball', 'badminton', 'hockey', 'motorsports', 'gaa'],
      sportsWithOutrights = ['formula1', 'cycling', 'movies', 'politics', 'tvspecials', 'motorsports'],
      sportsViewTypes = { className: false, outrights: false };

    if (sportsWithClassNames.indexOf(sportName) !== -1) {
      sportsViewTypes.className = true;
    }
    if (sportsWithOutrights.indexOf(sportName) !== -1) {
      sportsViewTypes.outrights = true;
    }
    return sportsViewTypes;
  }

  /**
   * adds icons to events
   *
   * @param eventsArray
   */
  addIconsToEvents(eventsArray: ISportEvent[]): Observable<void> {
    function addIcons(items: ISportCategory[]): void | PromiseLike<void> {
      _.each(eventsArray, eventEntity => {
        if (items[eventEntity.categoryId]) {
          eventEntity.svgId = items[eventEntity.categoryId].svgId;
        }
      });
    }
    return this.cmsProvider.getMenuItems().pipe(map(addIcons) as never);
  }

  /**
   * Get sport icon
   *
   * @param {number} sportId
   */
  getIconSport(sportId: number | string): Observable<ISportCategory> {
    return this.cmsProvider.getMenuItems()
      .pipe(map((items: ISportCategory[]) => {
        return _.find(items, (item, key) => {
          return key === sportId;
        });
      }));
  }

  /**
   * [getEventCorectedDay description]
   * @param  {[type]} eventStartTime [description]
   * @return {[type]}                [description]
   */
  getEventCorectedDay(eventStartTime: string): string {
    // ToDo check how it will work with gf
    if (this.timeService.determineDay(eventStartTime, false) === 'today') {
      return this.locale.getString('sb.today');
    }

    if (this.timeService.determineDay(eventStartTime, false) === 'tomorrow') {
      return this.filter.date(eventStartTime, 'EEE');
    }

    return this.filter.date(eventStartTime, 'd MMM');
  }

  /**
   * [getEventCorectedDays description]
   * @param  {[type]} eventStartTime [description]
   * @return {[type]}                [description]
   */
  getEventCorectedDays(eventStartTime: string): string {
    const day = this.timeService.determineDay(eventStartTime, false);
    if (day === 'today') {
      return this.locale.getString('sb.today');
    }

    if (day === 'tomorrow') {
      return this.locale.getString('sb.tomorrow');
    }

    return this.filter.date(eventStartTime, 'd MMM');
  }

  /**
   * Returns array of events without Enhanced Multiples
   * @param events {array}
   * @return {array}
   */
  filterMultiplesEvents(events: ISportEvent[]): ISportEvent[] {
    return _.reject(events, event => this.isMultiplesEvent(event));
  }

  /**
   * Verifies whether it is an enhanced multiples event
   * @param eventEntity {object}
   * @return {boolean}
   */
  isMultiplesEvent(eventEntity: ISportEvent): boolean {
    return eventEntity.typeName === 'Enhanced Multiples';
  }

  getCorrectedOutcomeMeaningMinorCode(outcomeEntity: IOutcome): number {
    let outcomeMeaningMinorCode: string | string[] | number = outcomeEntity.outcomeMeaningMinorCode;
    if (_.isNaN(parseInt(`${outcomeMeaningMinorCode}`, 10))) {
      // eslint-disable-next-line default-case
      switch (outcomeMeaningMinorCode) {
        case 'H':
          outcomeMeaningMinorCode = outcomeEntity.isUS ? 3 : 1;
          break;
        case 'D':
        case 'N':
        case 'L':
          outcomeMeaningMinorCode = 2;
          break;
        case 'A':
          outcomeMeaningMinorCode = outcomeEntity.isUS ? 1 : 3;
          break;
        case 'O':
          outcomeMeaningMinorCode = 2;
          break;
      }
      if (outcomeEntity.outcomeMeaningMajorCode === 'HL' && outcomeEntity.outcomeMeaningMinorCode === 'L') {
        outcomeEntity.isUS ? outcomeMeaningMinorCode = 1 : outcomeMeaningMinorCode = 3;
        // outcomeMeaningMinorCode = 3;
      }

      // checking for outcome from 'Both teams to score market'
      if (outcomeEntity.outcomeMeaningMajorCode === '--' && outcomeEntity.name === 'Yes') {
        outcomeMeaningMinorCode = 1;
      }
      if (outcomeEntity.outcomeMeaningMajorCode === '--' && outcomeEntity.name === 'No') {
        outcomeMeaningMinorCode = 3;
      }
    }
    if (outcomeEntity.outcomeMeaningMajorCode === 'OE' && outcomeEntity.outcomeMeaningMinorCode === '2') {
      outcomeMeaningMinorCode = 3;
    }
    return Number(outcomeMeaningMinorCode);
  }

  genClass(eventEntity: ISportEvent): string {
    const eventClass: string = eventEntity.racingFormEvent && eventEntity.racingFormEvent.class;
    return eventClass ? this.locale.getString('sb.class', { class: eventClass }) : '';
  }

  /**
   * Generate terms
   *
   * @param marketEntity
   * @returns {string}
   */
  genTerms(marketEntity: IMarket, label: string = 'sb.oddsAPlaces'): string {
    return this.locale.getString(label, {
      num: marketEntity.eachWayFactorNum,
      den: marketEntity.eachWayFactorDen,
      arr: this.genEachWayPlaces(marketEntity, true)
    });
  }

  genEachWayPlaces(marketEntity: IQuickbetReceiptLegPartsModel | IMarket | IBetDetailLegPart, newTerms: boolean = false): string {
    let oddsString: string = '',
      i = 0;
    const eachWayPlaces = Number(marketEntity.eachWayPlaces);

    // 5 -> '1,2,3,4,5'
    while (i < eachWayPlaces) {
      if (newTerms) {
        oddsString += (++i >= eachWayPlaces) ? i : `${i}-`;
      } else {
        oddsString += (++i >= eachWayPlaces) ? i : `${i},`;
      }
    }

    return oddsString;
  }

  /**
   * Group events by type name
   * @param {Boolean} isTote - true if we need to group tote events
   * @param array
   *        events array for certain day
   *        e.g. 'tomorrow', 'today', 'future'
   *
   * @returns {obj}
   *          e.g. {Ascot: [51], Cork: [18]}
   *          for Tote country will be included :
   *          {Ascot USA: [51], Cork South Africa: [18]}
   */
  groupEventsByTypeName(sportEvents: ISportEvent[], isTote?: boolean): ISportEventGroup {
    const groups: ISportEventGroup = {};

    sportEvents.forEach((event: ISportEvent) => {
      const groupName: string = isTote ? `${event.typeName} ${event.country}` : event.typeName;

      groups[groupName] = groups[groupName] || [];
      groups[groupName].push(event);
    });
    return groups;
  }

  /**
   * Filter Events Without Markets and Outcomes
   * USABLE ONLY for events with ONE market! Removing events without markets and markets without outcomes
   * @param eventsArray
   * @returns Array
   */
  filterEventsWithoutMarketsAndOutcomes(eventsArray: ISportEvent[]): ISportEvent[] {
    const filteredEvents = [];
    for (let i = 0, eventsLength = eventsArray.length; i < eventsLength; i++) {
      if ((eventsArray[i].markets.length) && (eventsArray[i].markets[0].outcomes.length)) {
        filteredEvents.push(eventsArray[i]);
      }
    }
    return filteredEvents;
  }
  /**
   * Removes events and markets without isMarketBetInRun attribute
   * @param events {array}
   * @return {array}
   */
  filterBetInRunMarkets(events: ISportEvent[]): ISportEvent[] {
    return _.filter(events, (eventEntity: ISportEvent) => {
      if (_.has(eventEntity, 'isStarted')) {
        eventEntity.markets = _.filter(eventEntity.markets, market => _.has(market, 'isMarketBetInRun'));
      }
      return eventEntity.markets.length > 0;
    });
  }

  /**
   * Sets correct price type, terms and icons, sorts outcomes
   * used only to display events in the raceCard directive
   * @params {object} eventsArray
   * @params {boolean} isFeaturedTab
   * @returns {array}
   */
  setCorrectPriceType(eventsArray: ISportEvent[], isFeaturedTab?: boolean, isNextRaces?: boolean): ISportEvent[] {
    _.each(eventsArray, (eventEntity: ISportEvent) => {
      if (!eventEntity || !eventEntity.markets) {
        return;
      }
      const nextFourMarket = eventEntity.markets[0];

      /**
       * terms calculated on ms for featured tab if terms empty no need to process
       * if not featured tab we should genTerms;
       */
      if (!isFeaturedTab && !isNextRaces) {
        nextFourMarket.terms = this.genTerms(nextFourMarket);
      }

      if (isNextRaces) {
        nextFourMarket.terms = this.genTerms(nextFourMarket, 'sb.newOddsAPlaces');
      }

      if (nextFourMarket) {
        if (nextFourMarket.isSpAvailable && !nextFourMarket.isLpAvailable) {
          nextFourMarket.correctPriceTypeCode = 'SP';
          nextFourMarket.outcomes = _.sortBy(nextFourMarket.outcomes, 'name');
        } else {
          nextFourMarket.correctPriceTypeCode = 'LP';
          nextFourMarket.outcomes = _.sortBy((_.sortBy(nextFourMarket.outcomes, 'prices[0].priceDec')));
        }

        _.each(nextFourMarket.outcomes, (outcomeEntity: IOutcome) => {
          if ((nextFourMarket.isSpAvailable && !nextFourMarket.isLpAvailable) ||
            (nextFourMarket.isSpAvailable && nextFourMarket.isLpAvailable && !outcomeEntity.prices[0])) {
            outcomeEntity.correctPriceType = 'SP';
          }

          if ((nextFourMarket.isLpAvailable) && (outcomeEntity.prices[0])) {
            outcomeEntity.correctPriceType = 'LP';
          }
          // sets icon to display correct silks
          outcomeEntity.icon = !!outcomeEntity[eventEntity.categoryId === '21' ? 'racingFormOutcome' : 'runnerNumber'];
        });
      }
    });

    return eventsArray.sort(
      (event1: ISportEvent, event2: ISportEvent) => Number(event1.startTime) - Number(event2.startTime)
    );
  }

  isListTemplate(selectedMarket: string): boolean {
    const templates = oddsCardConstant.LIST_TEMPLATES.map(name => name.toLowerCase());
    return selectedMarket ? templates.indexOf(selectedMarket.toLowerCase()) !== -1 : false;
  }
  
  isMultiMarketTemplate(selectedMarket: string): boolean {
    return selectedMarket ? selectedMarket.split(',').length > 1 : false;
  }

  /**
   * Check For GoalScorer Market
   * @param markets
   */
   private checkGoalScorerMarket (): void {
    if(this.marketList){
    const result = this.marketList.map(a => a.templateMarketName.toUpperCase());
    this.popularScorer = this.popularMarkets.every(value => {
      return result.includes(value.toUpperCase());
    });
    this.otherScorer = this.otherMarkets.every(value => {
      return result.includes(value.toUpperCase());
    });
    }
   }
    /**
   * check for get a price market
   * @returns boolean
   */
  private isGetAPriceMarket(market): boolean {
    const getAPrice = /(#GetAPrice)/i;
    return !!(market.templateMarketName && market.templateMarketName.match(getAPrice));
  }
}
