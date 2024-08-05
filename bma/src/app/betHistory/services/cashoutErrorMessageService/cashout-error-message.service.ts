import { Injectable } from '@angular/core';

import { ICashoutStatuses } from '../../models/bet-history-bet.model';
import { ICashOutBet } from '@app/betHistory/models/bet-history-cash-out.model';

import { LocaleService } from '@core/services/locale/locale.service';
import { cashoutConstants } from '../../constants/cashout.constant';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { RegularBetBase } from '@app/betHistory/betModels/regularBetBase/regular-bet-base.class';
import { IPanelMsg } from '@app/betHistory/models/bet-history-bet.model';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutErrorMessageService {

  readonly errorStatuses: ICashoutStatuses = {
    BET_WORTH_NOTHING: 'betWorthNothing'
  };

  readonly cashoutConstants = cashoutConstants;

  constructor(
    private locale: LocaleService
  ) {}

  /**
   * Function to get error message for all possible cashoutStatuses.
   * @param {string} requestType - type of requestType.
   * @param {object} bet - bet object from getBetDetail or getBetDetails.
   * @returns {string}
   */
  getErrorMessage(bet: RegularBetBase | ICashOutBet): IPanelMsg {
    let status;

    if (bet && bet.cashoutStatus) {
      const statusKey = `cashout${this.cashoutConstants.values.includes(bet.cashoutValue as string) ? 'Value' : 'Status'}`;
      status = this.errorStatuses[bet[statusKey].split(' ')[0]];
    } else if (bet && bet.cashoutValue) {
      const doesBetWorthNothing = this.cashoutConstants.betWorthNothing === bet.cashoutValue;
      status = doesBetWorthNothing ? this.errorStatuses.BET_WORTH_NOTHING : undefined;
    }

    const isSuspendedStatus = bet && this.cashoutConstants.cashoutSuspendedStatuses.includes(bet.cashoutValue as string);

    return {
      type: isSuspendedStatus ? this.cashoutConstants.cashOutAttempt.SUSPENDED : this.cashoutConstants.cashOutAttempt.ERROR,
      msg: isSuspendedStatus || !status ? '' : this.getParticularErrorMessage(status)
    };
  }

  /**
   * Function to get error message for known cashoutStatuses.
   * @param {object} bet - bet object.
   * @param {object/string} status - one of the available stasuses from errorStatuses.
   * @returns {string}
   */
  getParticularErrorMessage(status: string = 'default'): string {
    return this.locale.getString(`bethistory.cashoutBet.cashoutUnvailable.${status}`);
  }
}
