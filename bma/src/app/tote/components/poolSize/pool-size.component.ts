import { Component, Input } from '@angular/core';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { ToteBetSlipService } from './../../services/toteBetSlip/tote-bet-slip.service';

import { IPool } from './../../models/tote-event.model';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'pool-size',
  templateUrl: './pool-size.component.html'
})
export class PoolSizeComponent {
  @Input() pools: IPool[];
  @Input() currencyCalculator: any;
  @Input() poolType: string;

  constructor(
    private user: UserService,
    private toteBetSlip: ToteBetSlipService,
    protected currencyPipe: CurrencyPipe
  ) {
  }

  getPoolSize(): string {
    const currentPool = _.find(this.pools, pool => {
      return pool.poolType === this.poolType;
    });
    if (!currentPool) {
      return '';
    }
    return this.formatPoolSize(currentPool);
  }

  /**
   * Formats pool size according to user and pool currencies
   * @param {object} pool - pool object
   * @returns {String}
   */
  private formatPoolSize(pool: IPool): string {
    const userCurrency = this.user.currency,
      userCurrencySymbol = this.user.currencySymbol,
      poolSize = pool.poolValue,
      poolCurrency = pool.currencyCode,
      calculatedPoolSize = poolSize && this.currencyCalculator
        ? this.currencyCalculator.currencyExchange(poolCurrency, userCurrency, poolSize) : null,
      poolCurrencySymbol = this.toteBetSlip.getCurrency(pool.currencyCode);
    if (poolCurrency === userCurrency) {
      return poolSize ? `${this.getFormat(poolSize, userCurrencySymbol)}` : undefined;
    }

    return poolSize ? `${this.getFormat(calculatedPoolSize, userCurrencySymbol)} / ${this.getFormat(poolSize, poolCurrencySymbol)}`
      : undefined;
  }
  getFormat(price, symbol) {
    return this.currencyPipe.transform(price, symbol, 'code');
  }
}
