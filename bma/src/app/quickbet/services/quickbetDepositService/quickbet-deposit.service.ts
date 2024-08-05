import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';

import { IQuickbetDepositModel } from '@app/quickbet/models/quickbet-deposit.model';

@Injectable({ providedIn: 'root' })
export class QuickbetDepositService {
  quickDepositModel: IQuickbetDepositModel = {
    neededAmountForPlaceBet: undefined
  };

  constructor(
    private quickbetNotificationService: QuickbetNotificationService,
    private user: UserService,
    private pubsub: PubSubService) {
  }

  /**
   * Init quickbet deposit
   * @param {boolean} isBeforePlaceBet
   * @returns {boolean}
   */
  init(isBeforePlaceBet: boolean = false): boolean {
    if (!this.user.status) {
      return false;
    }

    if (isBeforePlaceBet) {
      this.pubsub.publish(this.pubsub.API.PAYMENT_ACCOUNTS_PASSED);
    }
  }

  /**
   * Update info panel and extend quickDepositModel
   * @param {string} stake
   * @param {boolean} isEachWay
   */
  update(stake: string, isEachWay: boolean = false): void {
    const totalStake: number = isEachWay ? Number(stake) * 2 : Number(stake);
    if (this.user.status && (totalStake > Number(this.user.sportBalance))) {
      const message = this.user.getUserDepositMessage(totalStake, false);
      const messageType = 'deposit';

      // Update deposit error message if stake was increased
      this.quickbetNotificationService.saveErrorMessage(message, messageType, 'quick-deposit');

      const neededAmount: string = this.user.getUserDepositNeededAmount(totalStake, false);
      _.extendOwn(this.quickDepositModel, { neededAmountForPlaceBet: neededAmount });
    } else {
      // Clear deposit message and quickDepositModel when:
      // 1. User does't have at least one card
      // 2. User is not logged in
      // 3. Stake < user balance
      // 4. Quick deposit notification is shown
      // 5. Stake < min bet
      const config = this.quickbetNotificationService.config;
      const isStakeTooLow = config.errorCode === 'STAKE_TOO_LOW';
      if (config.location === 'quick-deposit' || isStakeTooLow) {
        this.quickbetNotificationService.clear('quick-deposit');
      }

      _.extendOwn(this.quickDepositModel, { neededAmountForPlaceBet: '' });
    }
  }

  /**
   * Clear quickbet quickDeposit model
   */
  clearQuickDepositModel(): void {
    this.quickDepositModel.neededAmountForPlaceBet = undefined;
  }
}
