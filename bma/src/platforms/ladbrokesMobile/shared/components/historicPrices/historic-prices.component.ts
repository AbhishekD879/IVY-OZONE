import { Component } from '@angular/core';
import { HistoricPricesComponent } from '@shared/components/historicPrices/historic-prices.component';

@Component({
  selector: 'historic-prices',
  templateUrl: 'historic-prices.component.html'
})
export class LadbrokesHistoricPricesComponent extends HistoricPricesComponent {

  outputRacingHistoricPrice(): string {
    const prices = this.outcome.prices;
    let historicPrices = [];

    if (prices && prices.length > 1) {
      // extract up to two last historic prices.
      historicPrices = prices.length === 2 ? prices.slice(-1) : prices.slice(-2).reverse();
    }
    const formatedPrices = this.formatHistoricPrices(historicPrices);

    return historicPrices.length > 0 ? `${formatedPrices}` : '';
  }
}
