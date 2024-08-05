import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { UserService } from '@core/services/user/user.service';
import { IQuickDepositChecklist } from '@betslip/services/quickDeposit/quick-deposit.models';
import { IBetslipDepositData } from '@betslip/models/betslip-deposit.models';

@Injectable({ providedIn: BetslipApiModule })
export class QuickDepositService {
  quickDepositCache: IBetslipDepositData;
  countDownCurrentValue: string;

  private readonly DEFAULT_QD_VALUE: string = '0.00';

  constructor(protected userService: UserService) {}

  /**
   * Check Quick deposit availability for BetSlip
   *
   * Quick deposit form will display on BetSlip if:
   * - user has at least one selection on BetSlip and
   *   (user balance === 0 || user balance < (total stake - free bet stake) in betSlip)
   *   and (totalStakeWithOutFreeBetStake !== 0) and
   *   user has at least one valid credit card and placeBets process is not in progress
   *
   * @param stake {String|Number} - totalStakeWithOutFreeBetStake
   * @param freeBetStake {String|Number} - freebet stake amount
   * @param bsSelections {Number} - betSlipSelections
   * @param balance {String|Number}
   * @param placeBetsPending {Boolean}
   * @param showQuickDepositForm {boolean}
   * @param isSelectionSuspended {Boolean}
   * @returns {object}
   */
  checkQuickDeposit(stake: number, freeBetStake: string | number, balance: string | number, bsSelections: number,
                    placeBetsPending: boolean, isSelectionSuspended = false, showQuickDepositForm?: boolean): IQuickDepositChecklist {
    const userBalanceAvailable = balance !== null;

    if (this.isUserAbleToDeposit(userBalanceAvailable, bsSelections, placeBetsPending)) {
      // if freebet stake is selected and user balance is higher or equal then entered stake - then do not show quick deposit form
      const userBalance: number = Number(balance) || 0;

      if (Number(freeBetStake) && userBalance >= stake) {
        return {
          showQuickDepositForm: false,
          neededAmountForPlaceBet: 0
        };
      }

      const neededAmountForPlaceBet = (!stake || stake <= userBalance) ?
        this.DEFAULT_QD_VALUE : (stake - userBalance).toFixed(2);

      return {
        quickDepositFormAllowed: true,
        showQuickDepositForm: true,
        neededAmountForPlaceBet
      };
    }

    return {
      showQuickDepositForm: showQuickDepositForm || isSelectionSuspended,
      neededAmountForPlaceBet: 0
    };
  }

  protected isUserAbleToDeposit(userBalanceAvailable: boolean, bsSelections: number, placeBetsPending: boolean): boolean {
    return userBalanceAvailable && bsSelections && !placeBetsPending && this.userService.status;
  }
}
