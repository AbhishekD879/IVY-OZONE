import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { UserService } from '@core/services/user/user.service';

import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';

@Component({
  selector: 'bet-summary',
  templateUrl: 'bet-summary.component.html',
  styleUrls: ['bet-summary.component.scss']
})
export class BetSummaryComponent {
  @Input() maxPayOutValue: string;
  @Input() selection: IQuickbetSelectionModel;
  @Input() isLuckyDip?: boolean;
  @Output() readonly showMaxPayOutMessage: EventEmitter<boolean> = new EventEmitter();
  isUserLoggedIn: boolean;

  constructor(protected user: UserService,
              protected currencyPipe: CurrencyPipe,
              protected bppProviderService: BppProvidersService) {
  }

  /**
   * Formats total stake.
   * @returns {string}
   */
  getTotalStake(): string {
    const stake = (this.selection.isEachWay ? 2 : 1) * parseFloat(this.selection.stake);

    return this.currencyPipe.transform((stake || 0) + (this.selection.freebetValue || 0), this.user.currencySymbol, 'code');
  }

  getStake(): string {
    const stake = (this.selection.isEachWay ? 2 : 1) * parseFloat(this.selection.stake);
    const stakeValue = this.currencyPipe.transform((stake || 0), this.user.currencySymbol, 'code');
    return stakeValue;
  }

  /**
   * Formats potential payout.
   * @returns {string}
   */
  getPotentialPayout(): string {
    return Number.isNaN(+this.selection.potentialPayout) ? this.selection.potentialPayout
      : this.currencyPipe.transform(this.selection.potentialPayout, this.user.currencySymbol, 'code');
  }

  /**
   * @returns string
   */
  isCapped(): string {
    const potentialReturns = +this.selection.potentialPayout;
    const maxPayOutValue = +this.maxPayOutValue;
    if(potentialReturns > maxPayOutValue) {
      this.showMaxPayOutMessage.emit(true);
      return this.currencyPipe.transform(this.maxPayOutValue, this.user.currencySymbol, 'code');
    } else {
      this.showMaxPayOutMessage.emit(false);
      return this.getPotentialPayout();
    }
  }

}
