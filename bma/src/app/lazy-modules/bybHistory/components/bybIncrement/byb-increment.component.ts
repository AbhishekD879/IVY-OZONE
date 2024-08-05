import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { IYourcallBYBEventResponse } from '@app/yourCall/models/byb-events-response.model';
import { YourCallMarketGroup } from '@app/yourCall/models/markets/yourcall-market-group';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { IMapMarket, ISelectedMarketSelection } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';
import { IYourcallMarketSelectionsData } from '@app/yourCall/models/yourcall-api-response.model';
import { IYourcallSelection } from '@app/yourCall/models/selection.model';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'byb-increment',
  templateUrl: 'byb-increment.component.html',
  styleUrls: ['./byb-increment.component.scss'],
})

export class BybIncrementComponent implements OnInit, OnChanges {
  overMarkets: IYourcallSelection[] = [];
  underMarkets: IYourcallSelection[] = [];
  overMarketsMap = new Map<string, IMapMarket>();
  underMarketsMap = new Map<string, IMapMarket>();
  exactMapMarkets = new Map<string, IMapMarket>();
  showMarkets: Map<string, IMapMarket>;
  buttonState: string;
  initial: number;
  incrementer: number;
  incrementvalue: number = 0;
  incrementenable: boolean;
  marketRespData: IYourcallMarketSelectionsData[];
  iterativeIndex:any;
  isLoading: boolean;
  isCoral: boolean;
  @Input() market: YourCallMarketGroup;
  @Input() game: IYourcallBYBEventResponse;
  @Input() marketGroupName:string;
  @Output() readonly collapseLists = new EventEmitter();

  constructor(private yourCallMarketsService: YourcallMarketsService) { }

  /**
    * onchanges to trigger change
    * @param {SimpleChanges} changes
    * @return {YourCallMarketGroupItem[]}
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.market) {
      this.yourCallMarketsService.loadSelectionData(this.market).then((data) => {
        this.marketRespData = data;
        this.buttonState = '';
        this.seperate(this.market);
      }
      );
    }
  }

  /**
    * getter to get allmarkets
    * @return {YourCallMarketGroupItem[]}
   */
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.yourCallMarketsService.loadSelectionData(this.market).then((responseData: IYourcallMarketSelectionsData[]) => {
      this.marketRespData = responseData;
      this.seperate(this.market);
      this.isLoading = true;
    });
    this.callExactMarkets();
  }

  /**
    * getter to get allmarkets
    * @return {YourCallMarketGroupItem[]}
   */
  get markets(): YourCallMarketGroupItem[] {
    return this.market.markets;
  }
  set markets(value: YourCallMarketGroupItem[]) { }

  /**
    * to replace boilerplate text
    * @param {YourCallMarketGroup} market
    * @return {void}
   */
  seperate(market: YourCallMarketGroup): void {
    if (!this.marketRespData) return;
    this.marketRespData[0].selections.forEach((item: IYourcallSelection) => item.title = item.title.replace('OVER', 'Over').
      replace('UNDER', 'Under').replace('GOALS', 'Goals'));
    this.overMarkets = this.marketRespData[0].selections.filter((item: IYourcallSelection) => String(item.title).split(' ')[0] === 'Over');
    this.overMarketsMap.clear();
    this.underMarketsMap.clear();
    this.overMarkets.forEach(element => {
      this.overMarketsMap.set(element.bettingValue1, {'market': market, 'selection': element});
    });
    this.underMarkets = this.marketRespData[0].selections.filter((item: IYourcallSelection) => String(item.title).split(' ')[0] === 'Under');
    this.underMarkets.forEach(element => {
      this.underMarketsMap.set(element.bettingValue1, {'market': market, 'selection': element});
    });
    this.incrementenable = false;
  }

  /**
    * to show counter based on values
    * @param {string} clickedState
    * @return {void}
   */
  displayIncrement(clickedState: string): void {
    this.buttonState = this.buttonState === clickedState ? '' : clickedState;
    this.showMarkets = this.buttonState == 'over' ? this.overMarketsMap :this.underMarketsMap;
    this.initial = Number(this.overMarkets.length && this.overMarkets[0].bettingValue1);
    this.incrementer = 0;
    if(this.overMarkets[1]?.bettingValue1) {
      this.incrementvalue = Number(this.overMarkets[1].bettingValue1) - Number(this.overMarkets[0].bettingValue1);
    }
    this.incrementenable = true;
    this.iterativeIndex = this.showMarkets.entries();
    this.initial = this.iterativeIndex.next().value && this.iterativeIndex.next().value[0];
  }

  /**
    * to change the counter on increment or decrement
    * @param {number} valueChange
    * @return {void}
   */
  rotate(valueChange: number): void {
    this.initial = this.iterativeIndex.next().value[0];
    this.incrementer += valueChange;
    if (this.incrementer < 0) {
      this.incrementer += this.showMarkets.size;
    }
    this.incrementer %= this.showMarkets.size;
    this.yourCallMarketsService.isSelected(this.market as any,this.showMarkets[this.incrementer]);
  }

  /**
    * to call exact markets
    * @param {ISelectedMarketSelection} selectedMarketAndSelection
    * @return {void
   */
  selectValue(selectedMarketAndSelection: ISelectedMarketSelection): void {
    this.yourCallMarketsService.selectedSelectionsSet.add(selectedMarketAndSelection.selection.id);
    this.isSelected(selectedMarketAndSelection);
    this.yourCallMarketsService.selectValue(selectedMarketAndSelection.market, selectedMarketAndSelection.selection);
  }

  /**
    * to call exact markets
    * @param {ISelectedMarketSelection} selectedMarketAndSelection
    * @return {boolean}
   */
  isSelected(selectedMarketAndSelection: ISelectedMarketSelection): boolean {
    const val = this.yourCallMarketsService.isSelected(selectedMarketAndSelection.market, selectedMarketAndSelection.selection);
    return val;
  }

  /**
    * to call exact markets
    * @param {number} index
    * @return {number}
   */
  callExactMarkets(): void {
    if (this.market?.groupName == 'Total Goals') {
      this.yourCallMarketsService.markets.forEach((market, index) => {
        if (market.groupName == 'Exact Total Goals') {
          this.yourCallMarketsService.loadSelectionData(market).then((data) => {
            this.marketRespData = data;
            this.marketRespData[0].selections.forEach(item => item.title =
              item.title.replace('EXACT', 'Exactly').replace('GOALS', 'Goals').replace('GOAL', 'Goal'));
            this.marketRespData[0].selections.forEach(item => {
              this.exactMapMarkets.set(item.title[0], { 'market': market, 'selection': item });
            });
            if(this.marketRespData[0].selections[1]) {
              this.incrementvalue = (+this.marketRespData[0].selections[1].title[0]) - (+this.marketRespData[0].selections[0].title[0]);
            }
          });
        }
      });
    }
  }

  /**
    * to populate exact markets
    * @return {void}
   */
  exactMarkets(): void {
    this.buttonState = this.buttonState === 'exact' ? '' : 'exact';
    this.showMarkets = this.exactMapMarkets;
    this.incrementenable = true;

    this.iterativeIndex = this.showMarkets.entries();
    const exactMapValues = [];
    this.showMarkets.forEach((key,val) => {
      exactMapValues.push(+val);
    });
    if(exactMapValues.length > 0) {
      this.initial = exactMapValues[0];
      this.incrementvalue = exactMapValues.length > 1 ? exactMapValues[1]-exactMapValues[0] : 0;
    }
  }

  /**
    * to collapse accordions from child to parent
    * @return {void}
   */
  fncollapseLists(): void {
    this.collapseLists.emit();
  }
}
