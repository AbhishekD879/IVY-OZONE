import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { Goals } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'byb-timeline',
  templateUrl: 'byb-timeline.component.html',
  styleUrls: ['./byb-timeline.component.scss'],
})

export class BybTimelineComponent implements OnInit, OnChanges {
  @Output() readonly collapseLists: EventEmitter<void> = new EventEmitter();
  @Input() bybmarketName?: string;
  @Input() eachMarketGroup?: any;//YourCallMarketGroup | YourCallMarketGroupItem;
  @Input() marketGroupName: string;
  selectedEachMarket: YourCallMarketGroupItem;
  selectedMarket: number = -1;
  goalsText: string;
  switchers: { name: string }[] = [];
  isCoral:boolean;
  constructor() { }

  /**
   * detect input changes
   * @param {changes} changes
   * @returns {void}
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes) {
      this.selectedMarket = -1;
      this.isActiveGroup(-1);
      this.selectedEachMarket = null;
      this.switchers = [];
      this.populateMarketGroupNames();
    }
  }

  /**
   * Initial logic on compoenent generation
   * @returns {void}
   */
  ngOnInit(): void {
    this.goalsText = Goals[this.marketGroupName];
    this.isCoral = environment && environment.brand === 'bma';
    this.bybmarketName = 'TotalGoals';
  }

  /**
   * populateMarketGroupNames
   * @returns {void}
   */
  populateMarketGroupNames(): void {
    if (this.switchers.length)
      return;
    this.eachMarketGroup?.markets.forEach((market, index) => {
      this.switchers.push({ name: this.parseTitle(index) || market.key });
    });
  }

  parseTitle(index: number): string {
    if (this.eachMarketGroup && this.eachMarketGroup.markets) {
      let name = '';
      if (this.eachMarketGroup.markets[index].key.search('1ST HALF TOTAL') != -1) {
        name = '1st Half';
      } else if (this.eachMarketGroup.markets[index].key.search('2ND HALF TOTAL') != -1) {
        name = '2nd Half';
      } else {
        name = '90 Minutes';
      }
      return name.replace(/(\w)(\w*)/g,
        (g0, g1, g2) => { return g1.toUpperCase() + g2.toLowerCase(); });
    }
  }
  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
  trackByFn(index: number): number {
    return index;
  }
  trackBySwitchers(index: number): number {
    return index;
  }

  /**
   * Select team to display
   * @param index
   */
  selectGroup(index: number): boolean {
    if (index === this.selectedMarket) {
      this.reset();
      return false;
    }
    this.selectedMarket = index;
    this.selectedEachMarket = this.eachMarketGroup?.markets[index];
    return true;
  }

  /**
   * Check if group is selected
   * @param index
   * @returns {boolean}
   */
  isActiveGroup(index: number): boolean {
    return this.selectedMarket === index;
  }

  get displaySwitchers(): boolean {
    if (this.switchers.length == 0) {
      this.populateMarketGroupNames();
    }
    return this.eachMarketGroup?.markets?.length > 0;
  }
  set displaySwitchers(value: boolean) { }
  reset() {
    this.switchers = [];
    this.selectedMarket = -1;
    this.selectedEachMarket = null;
  }

  fncollapseLists() {
    this.reset();
    this.collapseLists.emit();
  }
}
