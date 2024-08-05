import { Component, OnInit, Input } from '@angular/core';

import { IYourcallSelection } from '../../models/selection.model';
import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { IYourCallMarket } from '@app/core/services/cms/models';

@Component({
  selector: 'yourcall-market-buttons',
  templateUrl: './your-call-market-buttons.component.html'
})
export class YourCallMarketButtonsComponent implements OnInit {

  @Input() market: IYourCallMarket;
  @Input() cols: number;
  @Input() rows: number;

  allShown: boolean = false;

  constructor(
    private yourCallMarketsService: YourcallMarketsService
  ) { }

  ngOnInit(): void {
    this.rows = 3;
    this.cols = this.market && this.market.cols ? this.market.cols : 2;

    if (this.market && this.yourCallMarketsService.isRestoredNeeded(this.market.key)) {
      this.yourCallMarketsService.restoreBet(this.market as any);
    }
  }

  trackBySelections(index: number, selection: IYourcallSelection): string {
    return `${index}${selection.odds}`;
  }

  /**
   * Check if display show more link
   * @returns {boolean}
   */
  get showMore(): boolean {
    return this.market.selections.length / this.cols > this.rows;
  }
  set showMore(value:boolean){}

  /**
   * Get selections display limit
   * @returns {number}
   */
  get limit(): number {
    return this.allShown ? this.market.selections.length : this.cols * this.rows;
  }
  set limit(value:number){}

  /**
   * Get actual selections array
   * @returns {*[]}
   */
  get selections(): IYourcallSelection[] {
    return this.market.selections.slice(0, this.limit);
  }
  set selections(value:IYourcallSelection[]){}

  /**
   * Toggle show all state
   */
  toggleShow(): void {
    this.allShown = !this.allShown;
  }

  /**
   * get css class
   * @returns {string}
   */
  get cssClass(): string {
    return `cols-${this.cols}`;
  }

  set cssClass(value: string){}

  /**
   * Action performed on button click
   * @param value {object}
   */
  selectValue(value: IYourcallSelection): void {
    this.yourCallMarketsService.selectValue(this.market as any, value);
  }

  /**
   * Check if value is selected
   * @param value {object}
   * @returns {boolean}
   */
  isSelected(value: IYourcallSelection): boolean {
    return this.yourCallMarketsService.isSelected(this.market as any, value);
  }
}
