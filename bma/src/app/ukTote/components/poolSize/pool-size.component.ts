import { Component, Input, ChangeDetectionStrategy } from '@angular/core';

import { UserService } from '@core/services/user/user.service';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { CurrencyCalculator } from '@core/services/currencyCalculatorService/currency-calculator.class';
import { DeviceService } from '@core/services/device/device.service';
import { CurrencyPipe } from '@angular/common';


@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'pool-size',
  templateUrl: './pool-size.component.html'
})
export class PoolSizeComponent {
  @Input() currentPool: IUkTotePoolBet;
  @Input() currencyCalculator: CurrencyCalculator;

  constructor(
    private user: UserService,
    protected deviceService: DeviceService,
    private coreToolsService: CoreToolsService,
    protected currencyPipe: CurrencyPipe
  ) {}

  /**
   * Return Formatted pool size according to user and pool currencies
   * @param {object} pool - pool object
   * @returns {String}
   */
  getFormattedPoolSize(): string | null {
    const pool = this.currentPool;
    const isLoggedIn = this.user.status;
    const userCurrency = this.user.currency;
    const userCurrencySymbol = this.user.currencySymbol;
    const poolSize = pool.poolValue;
    const poolCurrency = pool.currencyCode;
    const poolCurrencySymbol = this.coreToolsService.getCurrencySymbolFromISO(pool.currencyCode);
    const calculatedPoolSize = poolSize && this.currencyCalculator
      ? this.currencyCalculator.currencyExchange(poolCurrency, userCurrency, Number(poolSize))
      : null;

    if (!isLoggedIn || poolCurrency === userCurrency) {
      return poolSize ? `${this.getFormat(poolSize, poolCurrencySymbol)}` : null;
    }

    return poolSize
      ? `${this.getFormat(calculatedPoolSize, userCurrencySymbol)} / ${this.getFormat(poolSize, poolCurrencySymbol)}`
      : null;
  }
  isnotLegEvents () {
    return ["UWIN","UPLC"].includes(this.currentPool.poolType);
  }
  getFormat(price, symbol) {
    return this.currencyPipe.transform(price, symbol, 'code');
  }
}
