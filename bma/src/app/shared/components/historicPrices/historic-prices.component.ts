import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IOutcome } from '@core/models/outcome.model';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'historic-prices',
  templateUrl: 'historic-prices.component.html'
})
export class HistoricPricesComponent implements OnInit {
  @Input() outcome: IOutcome;
  @Input() hasWasLabel: boolean = false;

  setLongPriceStyle: boolean = false;
  hasHistoricPrice: boolean;

  constructor(
    public user: UserService,
    private localeService: LocaleService
  ) { }

  ngOnInit(): void {
    this.hasHistoricPrice = this.outcome.prices.length > 1;
  }

  /**
   * Return up to two previous racing prices in correct format fractional or decimal,
   * in order from older to newer previous price.
   * When price is live updated, save old price in cache and display it as previous.
   *
   * @params {object} outcome
   * @return {string}
   */
  outputRacingHistoricPrice(): string {
    const prices = this.outcome.prices;
    const wasLabel = this.hasWasLabel ? `${this.localeService.getString('sb.wasPrice')} ` : '';
    let historicPrices = [];

    if (prices && prices.length > 1) {
      // extract up to two last historic prices.
      historicPrices = prices.length === 2 ? prices.slice(-1) : prices.slice(-2).reverse();
      if(this.hasWasLabel) {
        historicPrices = this.checkWasPrice(prices[0], historicPrices);
      }
    }

    return historicPrices.length ? `${wasLabel}${this.formatHistoricPrices(historicPrices)}` : '';
  }
  
  /**
   * Return prices in correct format frac/dec or decimal.
   *
   * @params {array} prices
   * @return {string}
   */
  formatHistoricPrices(prices: IOutcomePrice[]): string {
    const historicPrices = _.map(prices, price => {
      return this.user.oddsFormat === 'frac' ? this.fracFn(price) : this.decimalFn(price);
    }).reverse()
      .join(' > ');

    if (historicPrices.length >= 12) {
      this.setLongPriceStyle = true;
    }

    return historicPrices;
  }

  /**
   * Return price fractional format.
   *
   * @params {object} price
   * @return {string}
   */
  fracFn(price: IOutcomePrice): string {
    return `${price.priceNum || price.livePriceNum}/${price.priceDen || price.livePriceDen}`;
  }

  /**
   * Return price decimal format.
   *
   * @params {object} price
   * @return {string}
   */
  decimalFn(price: IOutcomePrice): string {
    return Number(price.priceDec || price.livePriceDec).toFixed(2);
  }

  /**
   * 
   * @param currentOdd 
   * @param historicPrices 
   * @returns IOutcomePrice
   */
  private checkWasPrice(currentOdd:IOutcomePrice, historicPrices:IOutcomePrice[]):IOutcomePrice[] {
    const wasPrice = historicPrices.find((hprice: IOutcomePrice) => Number(currentOdd.priceNum) / Number(currentOdd.priceDen) >
      Number(hprice.livePriceNum) / Number(hprice.livePriceDen));
    return wasPrice ? [wasPrice] : [];
  }
}
