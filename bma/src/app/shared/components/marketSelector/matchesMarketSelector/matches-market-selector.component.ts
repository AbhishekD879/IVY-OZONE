import {
  Component,
  EventEmitter,
  Input,
  OnChanges, OnDestroy,
  OnInit,
  Output
} from '@angular/core';
import * as _ from 'underscore';

import { FiltersService } from '@core/services/filters/filters.service';
import { MarketSelectorTrackingService } from '@shared/components/marketSelector/market-selector-tracking.service';
import { MarketSelectorStorageService } from '@shared/components/marketSelector/matchesMarketSelector/market-selector-storage.service';

import {
  IMarketSelectorConfig,
  ICouponMarketSelector
} from '../market-selector.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportConfigTab } from '@app/core/services/cms/models';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'matches-market-selector',
  templateUrl: 'matches-market-selector.component.html'
})
export class MatchesMarketSelectorComponent implements OnInit, OnChanges, OnDestroy {
  @Input() eventDataSection: ITypeSegment;
  @Input() multipleEventsDataSections: ITypeSegment[];
  @Input() isEnhancedSectionExpanded: boolean;
  @Input() marketFilter: string;
  @Input() selectorType: string;
  @Input() sportId: string;
  @Input() marketOptions?: ICouponMarketSelector[];
  @Input() dropDownCss: boolean;
  @Input() targetTab: ISportConfigTab;
  @Input() toggleTitle: string;
  @Input() isFromCoupon: boolean;

  @Output() readonly filterChange: EventEmitter<string> = new EventEmitter(true);
  @Output() readonly hideEnhancedSection?: EventEmitter<void> = new EventEmitter();

  sportName: string = 'football';
  selectOptions: ICouponMarketSelector[];
  marketFilterText: string;
  SELECTOR_DATA: IMarketSelectorConfig;
  readonly tag = 'MarketSelector';
  currentSportName = 'football';

  constructor(
    private pubSubService: PubSubService,
    private marketSelectorTrackingService: MarketSelectorTrackingService,
    private marketSelectorStorageService: MarketSelectorStorageService,
    private filtersService: FiltersService,
    protected route: ActivatedRoute
  ) { }

  /**
   *  Add listeners and initialize market selector
   * @private
   */
  ngOnInit(): void {
    this.currentSportName = this.route.snapshot.paramMap.get('sport');
    if ((this.targetTab && this.targetTab.marketsNames) || this.marketOptions) {
    this.SELECTOR_DATA = this.selectorData();
    this.pubSubService.subscribe(this.tag,
      [this.pubSubService.API.DELETE_EVENT_FROM_CACHE, this.pubSubService.API.DELETE_MARKET_FROM_CACHE],
      () => this.initData());
    this.initData();
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.tag);
  }

  ngOnChanges(changes: any): void {
    const isMultipleSectionChanges = changes.multipleEventsDataSections &&
      changes.multipleEventsDataSections.currentValue &&
      changes.multipleEventsDataSections.previousValue !== undefined &&
      (changes.multipleEventsDataSections.currentValue !== changes.multipleEventsDataSections.previousValue);
    const isOneSectionChanges = changes.eventDataSection
      && changes.eventDataSection.currentValue
      && changes.eventDataSection.previousValue !== undefined &&
      (changes.eventDataSection.currentValue !== changes.eventDataSection.previousValue);
    if (isMultipleSectionChanges || isOneSectionChanges) {
      this.initData();
    }
  }

  trackById(index: number, element: ICouponMarketSelector): string {
    return element.id ? `${index}${element.id}` : index.toString();
  }

  /**
   * Filtering data by market
   * @param {string} marketFilter
   */
  filterMarkets(marketFilter: string | string[]): void {
    if (this.selectorType === 'footballCoupons') {
      marketFilter = _.isString(marketFilter)
        ? marketFilter.split(',')
        : marketFilter;
      marketFilter = marketFilter[0];
    }
    const marketFilterArray = _.isString(marketFilter)
    ? [marketFilter]
      : marketFilter;
    const trackingOption = marketFilterArray[1] || marketFilterArray[0];
    this.filterChange.emit(marketFilterArray[0]);
    // show option text in wrapped market selector in separate block
    this.marketFilterText = this.setSelectedOptionText(this.selectOptions, marketFilterArray[0]);

    this.hideEnhancedSection.emit();
    this.marketSelectorStorageService.storeSelectedOption(this.currentSportName, marketFilterArray[0]);
    if (this.selectorType !== 'footballCoupons') {
      const trackingMarketName = this.SELECTOR_DATA.MARKETS_NAMES[marketFilterArray[1]] ||
        this.SELECTOR_DATA.MARKETS_NAMES[marketFilterArray[0]];
      this.marketSelectorTrackingService.pushToGTM(trackingMarketName, this.sportId);
    } else {
      this.marketSelectorTrackingService.pushToGTM(trackingOption, this.sportId);
    }
    if(this.sportId=='18'){
      this.marketSelectorTrackingService.sendGTMDataOnMarketSelctorChange(trackingOption,this.targetTab);
    }
  }

  setSelectedOptionText(selectOptions: ICouponMarketSelector[], marketFilter: string): string {
    const selectedOption = selectOptions &&
    selectOptions.filter((option: ICouponMarketSelector) => option.templateMarketName.toLowerCase() === marketFilter.toLowerCase());
    return (selectedOption && selectedOption[0] && selectedOption[0].title) || '';
  }

  private initData(): void {
    let marketsNamesArray: string[];

    const initDynamically = (): void => {
      this.selectOptions = this.marketOptions;
      this.marketFilter = this.selectOptions && this.selectOptions.length ? this.selectOptions[0].templateMarketName : '';
      this.initActiveOption(this.gatherMultipleSectionsMarketNames(this.multipleEventsDataSections));
    };

    const initFromConfig = (): void => {
      marketsNamesArray = this.getMarketNamesArray();
      const sortedMarketNamesArray = this.makeUniqueSortedList(marketsNamesArray);

      this.initScope(sortedMarketNamesArray);
      this.initActiveOption(sortedMarketNamesArray);
    };

    this.selectorType === 'footballCoupons' ? initDynamically() : initFromConfig();
  }
  /**
   * init scope variables
   */
  private initScope(sortedMarketNamesArray: string[]): void {
    this.selectOptions = this.createOptionsList(sortedMarketNamesArray);
    this.marketFilter = this.getActiveOption(sortedMarketNamesArray);
  }

  /**
   * Restore or set default Active option
   * @param sortedMarketNamesArray
   */
  private initActiveOption(sortedMarketNamesArray: string[]): void {
    const storedSelectorOption = this.marketSelectorStorageService.restoreSelectedOption(this.currentSportName);

    if (storedSelectorOption && sortedMarketNamesArray.indexOf(storedSelectorOption) >= 0) {
      this.filterChange.emit(storedSelectorOption);
      this.hideEnhancedSection.emit();
      this.marketFilter = storedSelectorOption;
    } else {
      this.filterChange.emit(this.marketFilter);
      this.marketSelectorStorageService.storeSelectedOption(this.currentSportName, this.marketFilter);
    }
    // show option text in wrapped market selector in separate block
    this.marketFilterText = this.setSelectedOptionText(this.selectOptions, this.marketFilter);
  }

  /**
   * gather markets name from all events sections.
   * @returns {Array}
   */
  private getMarketNamesArray(): string[] {
    let namesArray = [];

    // for single section
    if (this.eventDataSection) {
      namesArray = this.gatherSectionMarketNames(this.eventDataSection);
    }

    // for multiple sections
    if (this.multipleEventsDataSections) {
      namesArray = this.gatherMultipleSectionsMarketNames(this.multipleEventsDataSections);
    }

    return namesArray;
  }

  /**
   * Get option to preselect it
   * @param {Array} optionsNamesArray
   * @returns {String}
   */
  private getActiveOption(optionsNamesArray: string[]): string {
    if (optionsNamesArray.indexOf(this.SELECTOR_DATA.DEFAULT_SELECTED_OPTION) >= 0) {
      return this.SELECTOR_DATA.DEFAULT_SELECTED_OPTION;
    }

    return optionsNamesArray[0];
  }

  /**
   * Sort names according to given order
   * @param {Array} order
   * @param {Array} uniq
   */
  private sortMarketNames(order: string[], uniq: string[]): string[] {
    uniq = uniq.map(market => market.toLowerCase());
    return order.filter(market => {
      const marketList = market.split(',');
      if(marketList.length > 1){
       let filteredList = [];
       filteredList = marketList.filter(marketName => uniq.indexOf(marketName.toLowerCase()) !== -1);
       return filteredList.length > 0;
      } else {
        return uniq.indexOf(market.toLowerCase()) !== -1;
      }
    });
  }

  /**
   * Rules to handle right Markets filtering
   * @param market
   * @param event
   * @returns {*}
   */
  private modifyMarket(market: IMarket, event: ISportEvent): IMarket {
    market.templateMarketName = market.templateMarketName.replace(/\|/g, '');

    if (market.templateMarketName === 'Match Betting' && this.selectorType !== 'footballCoupons') {
      // markets 'Match betting' and 'Match Result' are the same markets
      // and we should display only 'Match Result' in the market list
      market.templateMarketName = 'Match Result';
    }

    if (market.rawHandicapValue && !/[0-9]/.test(market.templateMarketName) && event.categoryName.toLowerCase() === this.sportName) {
      market.templateMarketName = `${market.templateMarketName} ${market.rawHandicapValue}`;
    }

    // For wrong generated market we clear names to not show in in the list
    if (market.templateMarketName === 'To Qualify' &&
      market.outcomes.length === 2 &&
      this.isDifferentOutcomesName(market, event)) {
      market.templateMarketName = '';
      market.name = '';
    }

    return market;
  }

  /**
   * for "To Qualify" market
   * Compare outcome names and event names
   * @param {Object} market - single Market object
   * @param {Object} event - single Event object
   * @returns {Boolean}
   * @private
   */
  private isDifferentOutcomesName(market: IMarket, event: ISportEvent) {
    const eventHomeName = this.filtersService.getTeamName(event.name, 0).toLowerCase();
    const eventAwayName = this.filtersService.getTeamName(event.name, 1).toLowerCase();
    const outcomeHomeName = market.outcomes[0].name.toLowerCase();
    const outcomeAwayName = market.outcomes[1].name.toLowerCase();

    return eventHomeName !== outcomeHomeName ||
      eventAwayName !== outcomeAwayName;
  }

  /**
   * gather all markets names from one or more sections
   * @param {Array} eventsSectionsData
   * @returns {Array}
   */
  private gatherMultipleSectionsMarketNames(eventsSectionsData: ITypeSegment[]): string[] {
    let marketNamesList = [];

    _.each(eventsSectionsData, (eventSection: ITypeSegment) => {
      marketNamesList = marketNamesList.concat(this.gatherSectionMarketNames(eventSection));
    });

    return marketNamesList;
  }

  /**
   * gather market names from one section
   * @param {Object} eventSection
   * @returns {Array}
   */
  private gatherSectionMarketNames(eventSection: ITypeSegment): string[] {
    const marketNamesList = [];

    _.each(eventSection.events, (event: ISportEvent) => {
      _.each(event.markets, (market: IMarket) => {
        const modifiedMarket = this.modifyMarket(market, event);

        marketNamesList.push(modifiedMarket.templateMarketName);
      });
    });

    return marketNamesList;
  }

  /**
   * Delete all duplicate data from array and sort all array
   * @param {Array} marketNamesList
   * @returns {Array}
   * @private
   */
  private makeUniqueSortedList(marketNamesList: string[]): string[] {
    return this.sortMarketNames(this.SELECTOR_DATA.MARKETS_NAME_ORDER, _.uniq(marketNamesList));
  }

  /**
   * Create data for Selector Options
   * @returns {Array}
   * @param {Array} marketNamesArray
   */
  private createOptionsList(marketNamesArray: string[]): ICouponMarketSelector[] {
    return marketNamesArray.map((elem: string) => {
      return {
        templateMarketName: elem,
        title: this.SELECTOR_DATA.MARKETS_NAMES[elem]
      };
    });
  }
  /**
   * @returns IMarketSelectorConfig
   */
  private selectorData(): IMarketSelectorConfig {
    const marketNames = {};
    const marketNamesOrder = [];
    if (this.targetTab && this.targetTab.marketsNames && this.targetTab.marketsNames.length) {
      this.targetTab.marketsNames.forEach(element => {
        marketNames[element.templateMarketName.trim()] = element.title.trim();
        marketNamesOrder.push(element.templateMarketName.trim());
      });
      return {
        DEFAULT_SELECTED_OPTION: this.targetTab.marketsNames[0].templateMarketName.trim(),
        MARKETS_NAMES: marketNames,
        MARKETS_NAME_ORDER: marketNamesOrder
      }
    }
    return null;
  }
}
