import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { YourcallDashboardService } from '@app/yourCall/services/yourcallDashboard/yourcall-dashboard.service';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { Added, AddTo, IMapMarket } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { IYourcallSelection } from '@app/yourCall/models/selection.model';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'byb-counter',
  templateUrl: 'byb-counter.component.html',
  styleUrls: ['./byb-counter.component.scss'],
})

export class BybCounterComponent implements OnInit, OnChanges {
  @Input() initial: string;
  @Input() incrementvalue: number;
  @Input() selectedMap: Map<string, IMapMarket>;
  @Input() buttonState: string;
  @Output() readonly selectedSelection = new EventEmitter();
  @Output() readonly collapseLists = new EventEmitter();
  index: number = 0;
  myMapArr: [string, IMapMarket][] = [];
  addToSlipText : string = AddTo;
  isCoral: boolean;
  constructor(private yourCallMarketsService: YourcallMarketsService,
    private yourcallDashboardService: YourcallDashboardService) {
  }

  /**
   * to detect changes on input changes
   * @returns {void}
   */
  ngOnChanges(changes: SimpleChanges): void {
    this.selectValue();
    this.index = 0;
    this.addToSlipText = AddTo;
  }

  /**
   * to Init values
   * @returns {void}
   */
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.initial = '0';
  }

  /**
   * to set default values when parent selections are changed
   * @returns {void}
   */
  selectValue(): void {
    if(!this.selectedMap) return;
    this.myMapArr =  [...this.selectedMap];
    this.initial = this.myMapArr[0][0];
  }

  /**
   * to change curr selection when counter is changed
   * @param {number} changedVal
   * @returns {void}
   */
  rotate(changedVal: number): void {
    this.addToSlipText = AddTo;
    this.index += changedVal;
    if(this.index >= this.myMapArr.length)  {
      this.index = 0;
    } else if(this.index < 0) {
      this.index = this.myMapArr.length-1;
    }
    this.displayVal();
  }

  /**
   * to update initial val
   * @param {number} changedVal
   * @returns {void}
   */
  displayVal(): void {
    this.initial = this.myMapArr[this.index][0];
  }

  /**
   * when add to bb is clicked
   * @returns {void}
   */
  selectedValue(): void {
    const selectedSelectionsSet = this.selectedMap.get(this.initial);
    if(!this.yourCallMarketsService.selectedSelectionsSet.has(selectedSelectionsSet.selection?.id)) {
      this.yourCallMarketsService.selectedSelectionsSet.add(selectedSelectionsSet.selection?.id);
      this.addToSlipText = Added;
      this.selectedSelection.emit(this.selectedMap.get(this.initial));
      this.updateSelectionSet();
    } else {
      this.yourCallMarketsService.selectedSelectionsSet.delete(selectedSelectionsSet.selection.id);
      this.yourCallMarketsService.selectValue(selectedSelectionsSet.market as YourCallMarketGroupItem, selectedSelectionsSet.selection as IYourcallSelection);
    }
  }

  /**
   * update selection set in any operation
   * @returns {void}
   */
  updateSelectionSet(): void {
    this.yourCallMarketsService.selectedSelectionsSet = new Set();
    this.yourcallDashboardService.items.forEach(combinationSelection => {
      if(combinationSelection.selection && combinationSelection.selection.id)
        this.yourCallMarketsService.selectedSelectionsSet.add(combinationSelection.selection.id);
    });
  }

  /**
   * remove a selection when deleted
   * @returns {void}
   */
  removeSelection(): void {
    const selectionDetails = this.selectedMap.get(this.initial);
    this.yourCallMarketsService.selectValue(selectionDetails.market as YourCallMarketGroupItem, selectionDetails.selection as IYourcallSelection);
  }

  /**
   * check what txt needs to display on betbuilder button
   * @returns {void}
   */
  checkCurrentStatus(): boolean {
    if(this.yourCallMarketsService.removeAllMarkets) {
      this.yourCallMarketsService.selectedSelectionsSet = new Set();
      this.yourCallMarketsService.removeAllMarkets = false;
    }
    if (this.yourCallMarketsService.lastRemovedMarket && this.yourCallMarketsService.lastRemovedMarket === this.selectedMap?.get(this.initial)?.selection?.id) {
      this.yourCallMarketsService.lastRemovedMarket = -1;
    }
    this.addToSlipText = this.yourCallMarketsService.selectedSelectionsSet.has(this.selectedMap?.get(this.initial)?.selection?.id) ? Added: AddTo;
    return true;
  }
}