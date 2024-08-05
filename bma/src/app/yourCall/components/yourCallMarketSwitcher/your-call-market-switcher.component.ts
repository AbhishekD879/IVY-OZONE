import { IYourcallSelection } from '@yourcall/models/selection.model';
import { YourCallMarketGroupPlayer } from './../../models/markets/yourcall-market-group-player';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';

import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';

@Component({
  selector: 'yourcall-market-switcher',
  templateUrl: './your-call-market-switcher.component.html'
})
export class YourCallMarketSwitcherComponent implements OnInit {

  @Input() market: YourCallMarketGroupPlayer;
  @Input() limit: number;

  @Output() readonly marketLoaded = new EventEmitter<void>();

  length: number = 0;
  switchers: { value: number; title: string }[] = [];
  selectedGroup: number = 0;
  selections: IYourcallSelection[] = [];
  switcherSelections: IYourcallSelection[] = [];
  showMore: boolean;
  allShown: boolean;
  isMarketSelections: boolean;
  isInit: boolean;
  constructor(
    private yourCallMarketsService: YourcallMarketsService
  ) { }

  ngOnInit(): void {
    this.yourCallMarketsService.prepareMarket(this.market).then(() => {
      _.each(this.market.groups, group => {
        this.length = Math.max(this.length, this.market.getSelectionsForGroup(group.value).length);
      });
      this.switchers = this.market.groups;
      this.showMore = this.length > this.limit;
      this.allShown = !this.showMore;
      this.selectGroup(0);

      // Restore bets from storage functionality
      if (this.yourCallMarketsService.isRestoredNeeded(this.market.key)) {
        this.yourCallMarketsService.restoreBet(this.market);
      }

      // Modify market appearance according to restored values
      let index = this.switchers.length;
      _.each(this.market.selected, (s: any) => {
        index = Math.min(index, this.switchers.indexOf(_.findWhere(this.switchers, { value: s.group })));
        // If selected item index is more then limit, display all
        this.allShown = this.market.getSelectionsForGroup(s.group).indexOf(s) > this.limit || this.allShown;
      });
      if (index < this.switchers.length) {
        // Make active first group which has selections
        this.selectGroup(index);
      }
      if (this.market.selections.length) {
        this.isMarketSelections = true;
      }
      this.isInit = true;

      this.marketLoaded.next();
    });
  }

  /**
   * Check if group is selected
   * @param index
   * @returns {boolean}
   */
  isActiveGroup(index: number): boolean {
    return this.selectedGroup === index;
  }

  /**
   * Select team to display
   * @param index
   */
  selectGroup(index: number): void {
    this.selectedGroup = index;
    this.selections = this.market.getSelectionsForGroup(this.switchers[index].value);
    this.limitSelections();
  }

  trackBySelections(index: number, selection: IYourcallSelection): string {
    return `${index}${selection.id}${selection.title}`;
  }

  /**
   * Get selections limit to display
   * @returns {number|*}
   */
  get limitTo(): number {
    return this.allShown ? this.length : this.limit;
  }
  set limitTo(value:number){}

  /**
   * Show/hide all items
   */
  toggleShow(): void {
    this.allShown = !this.allShown;
    this.limitSelections();
  }

  /**
   * Action performed on button click
   * @param event
   */
  selectValue(value) {
    this.yourCallMarketsService.selectValue(this.market, value);
  }

  /**
   * Check if value is selected
   * @param value
   * @returns {boolean}
   */
  isSelected(value): boolean {
    return this.yourCallMarketsService.isSelected(this.market, value);
  }

  trackBySwitchers(index: number, switcher: { value: number; title: string }): string {
    return `${index}${switcher.value}`;
  }

  private limitSelections(): void {
    this.switcherSelections = [].concat(this.selections).splice(0, this.limitTo);
  }
}
