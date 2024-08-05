import { Component, Input, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'betslip-deposit-error-container',
  templateUrl: './betslip-deposit-error-container.component.html',
  styleUrls: ['./betslip-deposit-error-container.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class BetslipDepositErrorContainerComponent {
  @Input() errorMsg: string;
  @Input() errorType: string;
  @Input() neededAmountForPlaceBet: string;

  /**
   * Check if needed amount for place bet to show appropriate error message
   */
  isAmountNeeded(): boolean {
    return Number(this.neededAmountForPlaceBet) > 0;
  }
}
