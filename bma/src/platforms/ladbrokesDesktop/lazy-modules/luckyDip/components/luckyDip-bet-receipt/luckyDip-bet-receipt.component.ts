import { Component } from '@angular/core';
import { QuickbetReceiptLdComponent } from '@app/quickbet/components/quickbetReceiptLuckyDip/quickbet-receipt-ld/quickbet-receipt-ld.component';
import { LUCKY_DIP_CONSTANTS } from '@app/lazy-modules/luckyDip/constants/lucky-dip-constants';


@Component({
  selector: 'lucky-dip-bet-receipt',
  templateUrl: './luckyDip-bet-receipt.component.html',
  styleUrls: ['luckyDip-bet-receipt.component.scss']
})

export class LadsDeskLuckyDipBetReceiptComponent extends QuickbetReceiptLdComponent {

  /**
    * Function call on go betting button press(done button)
    * @returns {void}
    */
  done(): void {
    this.pubsub.publish(LUCKY_DIP_CONSTANTS.LD_BET_PLACED, false);
  }

  /**
   * Method to fetch your bets string counter value
   * @returns {string}
   */
  buildBetsCounterText(): string {
    return LUCKY_DIP_CONSTANTS.YOUR_BETS;
  }

  ngOnDestroy(): void {
    this.pubsub.publish(LUCKY_DIP_CONSTANTS.LD_BET_PLACED, false);
  }
}
