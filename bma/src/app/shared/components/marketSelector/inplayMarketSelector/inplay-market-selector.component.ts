import {
  Component,
  EventEmitter,
  Input, OnChanges,
  OnInit,
  Output, SimpleChanges
} from '@angular/core';
import * as _ from 'underscore';

import { MarketSelectorConfigService } from '@sharedModule/components/marketSelector/market-selector-config.service';
import { MarketSelectorTrackingService } from '@sharedModule/components/marketSelector/market-selector-tracking.service';

import {
  IMarketSelectorConfig,
  IMarketSelectorOption,
  IReloadData
} from '../market-selector.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { MarketSelectorStorageService } from '@shared/components/marketSelector/matchesMarketSelector/market-selector-storage.service';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';

@Component({
  selector: 'inplay-market-selector',
  templateUrl: 'inplay-market-selector.component.html'
})
export class InplayMarketSelectorComponent implements OnInit, OnChanges {
  @Input() marketSelectorOptions: string[];
  @Input() eventDataSection: ITypeSegment;
  @Input() selectorType: string;
  @Input() sportId: number;
  @Input() resetDropdown: boolean;

  @Output() readonly reloadData: EventEmitter<IReloadData> = new EventEmitter();
  @Output() readonly selectedMarketName: EventEmitter<string> = new EventEmitter();

  SELECTOR_DATA: IMarketSelectorConfig;

  marketFilter: string;
  marketFilterText: string;
  selectOptions: IMarketSelectorOption[];
  currentSport: string;
  topMarkets = [];
  protected sportsConfigSubscription: Subscription;

  constructor(
    private marketSelectorConfigService: MarketSelectorConfigService,
    private marketSelectorTrackingService: MarketSelectorTrackingService,
    private marketSelectorStorageService: MarketSelectorStorageService,
    protected sportsConfigService: SportsConfigService,
    protected route: ActivatedRoute
  ) { }

  /**
   *  Add listeners and initialize market selector
   * @private
   */
  ngOnInit(): void {
    this.currentSport = this.route.snapshot.paramMap.get('sport');
    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.currentSport).subscribe(data => {
      this.topMarkets = data.sportConfig.config.request.aggregatedMarkets;
    });
    this.SELECTOR_DATA = this.selectorData();
    this.initSelectorOptions();
    const storedSelectorOption = this.marketSelectorStorageService.restoreSelectedOption(this.currentSport);
    let storedSelectorOptionValue = this.isMarketAvailable(storedSelectorOption) ?
              storedSelectorOption : this.marketSelectorOptions[0];
    if (this.resetDropdown) {
      storedSelectorOptionValue = this.marketSelectorOptions[0];
    }
    if (this.eventDataSection?.marketSelector && this.marketSelectorOptions) {
      this.filterMarkets(storedSelectorOptionValue, true);
    }
    this.marketFilter = (this.marketFilter && this.marketFilter.length > 0) ? this.marketFilter : this.marketSelectorOptions[0];
    this.marketFilterText = this.setSelectedOptionText(this.selectOptions, this.marketFilter);
    this.selectedMarketName.emit(this.marketFilter);
  }

  ngOnDestroy(): void {
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  ngOnChanges(changes: SimpleChanges): void  {
    const isChanges = changes.eventDataSection.currentValue && changes.eventDataSection.previousValue !== undefined &&
      (changes.eventDataSection.currentValue.marketSelector !== changes.eventDataSection.previousValue.marketSelector);
    const isMarketChanged = changes.eventDataSection.currentValue && changes.eventDataSection.previousValue !== undefined &&
      (changes.eventDataSection.currentValue.marketSelector !== changes.eventDataSection.previousValue.marketSelector);
    if (isMarketChanged) {
      this.marketFilter = changes.eventDataSection.currentValue.marketSelector;
      this.selectedMarketName.emit(this.marketFilter);
      // show option text in wrapped market selector in separate block
      this.marketFilterText = this.setSelectedOptionText(this.selectOptions, this.marketFilter);
    }
    if (isChanges) {
      this.initSelectorOptions();
    }
  }

  trackByIndex(index: number): string {
    return index.toString();
  }
  isMarketAvailable(option) {
    return this.marketSelectorOptions.includes(option);
  }
  setSelectedOptionText(selectOptions: IMarketSelectorOption[], marketFilter: string): string {
    const selectedOption = selectOptions &&
      selectOptions.filter((option: IMarketSelectorOption) => option.name === marketFilter);
    return (selectedOption && selectedOption[0] && selectedOption[0].text) || '';
  }

  /**
   * Apply new filter and reload sports data from server.
   * @param {string} templateMarketName
   */
  filterMarkets(templateMarketName: string, onMarketSelectorInit?: boolean): void {
    this.marketFilter = templateMarketName;
    this.marketSelectorStorageService.storeSelectedOption(this.currentSport, this.marketFilter);
    if (this.resetDropdown) {
      this.marketFilter = this.marketSelectorOptions[0];
    }
    const trackingMarketName = this.SELECTOR_DATA.MARKETS_NAMES[templateMarketName];
    this.reloadData.emit({
      useCache: false,
      additionalParams : {
        marketSelector: templateMarketName
      }
    });
    this.selectedMarketName.emit(this.marketFilter);
    if (!onMarketSelectorInit) {
      this.resetDropdown = false;
      this.marketSelectorTrackingService.pushToGTM(trackingMarketName, this.sportId);
    }
  }

  /**
   * init/reinit options data to build select element
   * @private
   */
  private initSelectorOptions(): void {
    this.selectorData();
    const sortedMarketNamesArray = this.marketSelectorOptions;

    if (this.selectOptions && !sortedMarketNamesArray) {
      return;
    }

    if (this.marketFilter && this.marketSelectorOptions.indexOf(this.marketFilter) === -1) {
      this.marketFilter = this.marketSelectorOptions[0];
      this.filterMarkets(this.marketFilter);
      this.selectedMarketName.emit(this.marketFilter);
      return;
    }

    this.selectOptions = this.createOptionsList(sortedMarketNamesArray);
  }

  /**
   * Create data for Selector Options
   * @returns {Array}
   * @param {Array} marketNamesArray
   */
  private createOptionsList(marketNamesArray: string[]): IMarketSelectorOption[] {
    return marketNamesArray.map(elem => {
      return {
        name: elem,
        text: this.SELECTOR_DATA.MARKETS_NAMES[elem]
      };
    });
  }
  /**
   * @returns IMarketSelectorConfig
   */
  private selectorData(): IMarketSelectorConfig {
    this.SELECTOR_DATA = this.marketSelectorConfigService[this.selectorType]?.length > 0 ?
      this.marketSelectorConfigService[this.selectorType].filter(item => item.SPORT_ID === this.sportId)[0] : null;
      this.topMarkets && [...this.topMarkets].reverse().forEach(element => {
        let isremovedFromMSL = false
        element.titleName.split(',').forEach(market => {
          const index = this.marketSelectorOptions.indexOf(market);
          if(index > -1){
            isremovedFromMSL = true;
            this.marketSelectorOptions.splice(index, 1);
          }
        });
        if(isremovedFromMSL) {
          this.SELECTOR_DATA.MARKETS_NAMES[element.titleName] = element.marketName;
          this.SELECTOR_DATA.MARKETS_NAME_ORDER.push(element.titleName);
          this.marketSelectorOptions.unshift(element.titleName);
        }
      });
    this.marketSelectorOptions = _.uniq(this.marketSelectorOptions);
    return this.SELECTOR_DATA;
  }
}
