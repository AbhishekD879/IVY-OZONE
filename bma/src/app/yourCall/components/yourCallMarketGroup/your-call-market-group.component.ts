import { YourCallMarketGroupItem } from './../../models/markets/yourcall-market-group-item';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';

import { YourCallMarketGroup } from '../../models/markets/yourcall-market-group';
import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { IYourcallBYBEventResponse } from '@yourcall/models/byb-events-response.model';

@Component({
  selector: 'yourcall-market-group',
  templateUrl: './your-call-market-group.component.html',
  styleUrls: ['./your-call-market-group.component.scss']
})
export class YourCallMarketGroupComponent implements OnInit {

  @Input() market: YourCallMarketGroup;
  @Input() game: IYourcallBYBEventResponse;

  @Output() readonly marketLoaded = new EventEmitter<void>();

  switchers: { name: string }[] = [];
  length: number = 0;
  selectedMarket;
  selectedGroup: number = 0;
  selectRestored: boolean;

  constructor(
    private yourCallMarketsService: YourcallMarketsService
  ) {}

  ngOnInit(): void {
    this.yourCallMarketsService.loadMarket(this.market).then((data) => {
      _.each(this.markets, market => {
        this.switchers.push({ name: market.getShortTitle() });
      });
      this.selectedMarket = this.markets[this.selectedGroup];
      _.each(this.markets, (market: YourCallMarketGroupItem, index) => {
        if (this.yourCallMarketsService.isRestoredNeeded(market.key)) {
          this.yourCallMarketsService.restoreBet(market);
          // make active first child market which selection was restored
          this.selectRestored = this.selectRestored || this.selectGroup(index);
        }
      });

      this.marketLoaded.next();
    });
  }

  get markets(): YourCallMarketGroupItem[] {
    return this.market.markets;
  }
  set markets(value:YourCallMarketGroupItem[]){}

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
  selectGroup(index: number): boolean {
    this.selectedGroup = index;
    this.selectedMarket = this.markets[index];
    return true;
  }

  /**
   * Check if need display switchers. Do not display if only one folded market
   * @returns {boolean}
   */
  get displaySwitchers(): boolean {
    return this.markets.length > 1;
  }
  set displaySwitchers(value:boolean){}

  trackBySwitchers(index: number, switcher: { name: string }): string {
    return `${index}${switcher.name}`;
  }
}
