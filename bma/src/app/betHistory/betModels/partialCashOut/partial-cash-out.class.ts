import { CashOutCore } from '../cashOutCore/cash-out-core.class';

import { cashoutConstants } from '../../constants/cashout.constant';

import { LocaleService } from 'app/core/services/locale/locale.service';
import { CashOutMapService } from '../../services/cashOutMap/cash-out-map.service';
import { GtmService } from 'app/core/services/gtm/gtm.service';
import { CoreToolsService } from 'app/core/services/coreTools/core-tools.service';
import { FiltersService } from 'app/core/services/filters/filters.service';
import { CashoutErrorMessageService } from '../../services/cashoutErrorMessageService/cashout-error-message.service';
import { CashoutDataProvider } from '../../services/cashoutDataProvider/cashout-data.provider';

import { ICashoutBet } from '../../models/bet-history-bet.model';
import { IBetHistoryBet, ICashoutError } from '../../models/bet-history.model';
import {
   ICashoutBetResponse
} from 'app/bpp/services/bppProviders/bpp-providers.model';
import { PubSubService } from 'app/core/services/communication/pubsub/pubsub.service';
import { ClientUserAgentService } from 'app/core/services/clientUserAgent/client-user-agent.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import {
  IBet
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

export class PartialCashOut extends CashOutCore {

  readonly cashoutConstants = cashoutConstants;
  id: string;
  cashOutObj: ICashoutBet;
  bet: IBetHistoryBet;

  constructor(
   filterService: FiltersService,
   localeService: LocaleService,
   cashOutMapService: CashOutMapService,
   gtm: GtmService,
   cashOutDataProviderService: CashoutDataProvider,
   toolsService: CoreToolsService,
   cashOutErrorMessage: CashoutErrorMessageService,
   pubsub: PubSubService,
   awsService: AWSFirehoseService,
   liveServConnectionService: LiveServConnectionService,
   clientUserAgentService: ClientUserAgentService,
   deviceService: DeviceService
  ) {
    super(filterService, localeService, cashOutMapService,
      gtm, cashOutDataProviderService, toolsService,
      cashOutErrorMessage, pubsub, awsService, liveServConnectionService, clientUserAgentService, deviceService);
  }
  /**
   * Check if bet cashed out successfully
   * @return {boolean}
   */
  isCashOutSuccessful(): boolean {
    return this.bet && (this.bet.isCashedOut === this.cashoutConstants.result.YES) &&
        (this.bet.isSettled === this.cashoutConstants.result.NO);
  }

  /**
   * Handler for success partial cash out
   */
  handleSuccess(res: ICashoutBetResponse): void {
    this.sendGTMSuccessCashout(this.cashoutConstants.cashOutType.PARTIAL);

    this.cashOutObj.isPartialActive = false;
    this.cashOutObj.panelMsg = {};
    this.cashOutObj.partialCashOutPercentage = 100;
    this.cashOutObj.setCashoutSuccessState(this.localeService.getString('bethistory.partialCashOutSuccess'));

    this.awsCashOut('PartialCashOut=>makeCashOut=>Success', this.cashoutConstants.cashOutAttempt.SUCCESS);
    this.updatePartialCashOutBet(res);
  }

  /**
   * Handler for 'CASHOUT_VALUE_CHANGED' sub error code
   */
  cashOutChanged(res: ICashoutBetResponse): void {
    this.handleError(this.getErrorMsgFromDictionary(), res);
  }

  /**
   * Default handler for all other sub error codes
   * @param errorOpt {Object}
   */
  cashOutDefault(errorOpt): void {
    this.handleError(this.getErrorMsgFromDictionary(), errorOpt);
    this.rollbackPartialCashOutBetState(true);
  }

  /**
   * Final error handling with updating bet data
   * @param msg {string}
   * @param res {ICashoutBetResponse}
   * @private
   */
  private handleError(msg: string, res: ICashoutBetResponse): void {
    this.cashOutObj.isCashOutBetError = true;
    this.clearErrorStateAfter(this.cashoutConstants.tooltipTime);
    this.formAttemptPanelObj(msg, null);
    this.sendGTMFailureCashout(this.cashoutConstants.cashOutType.PARTIAL);
    this.awsCashOut('PartialCashOut=>makeCashOut=>Error', this.cashoutConstants.cashOutAttempt.ERROR,
      { errorCode: this.errorCode, errorDictionary: msg } as ICashoutError);
    this.updatePartialCashOutBet(res);
  }

  /**
   * Hide error message and clear error state of cashout
   */
  private clearErrorStateAfter(delay: number) {
    setTimeout(() => {
      this.cashOutObj.isPartialActive = false;
      this.cashOutObj.isCashOutBetError = false;
      this.cashOutObj.attemptPanelMsg = {};
      this.cashOutObj.partialCashOutPercentage = 100;
      this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, this.cashOutObj);
    }, delay);
  }

  /**
   * Generate object for cash out attempt panel
   * @param msg {string}
   * @param type {string}
   * @private
   */
  private formAttemptPanelObj(msg: string, type: string): void {
    this.cashOutObj.attemptPanelMsg = {
      type: type || this.cashoutConstants.cashOutAttempt.ERROR,
      msg
    };
  }

  /**
   * Rollback partial cash out bet state
   * @param isPartialCashOutUnavailable {Boolean}
   */
  private rollbackPartialCashOutBetState(isPartialCashOutUnavailable: boolean): void {
    this.enableCashOut();

    if (isPartialCashOutUnavailable) {
      this.cashOutObj.isPartialCashOutAvailable = false;
    }
  }

  /**
   * Update cash out object after partial cashed out
   * @param updatedCashOutObj {Object}
   */
  private setPartialCashOutParameters(updatedCashOutObj): void {
    updatedCashOutObj.currencySymbol = this.cashOutObj.currencySymbol;
    this.cashOutObj.stake = updatedCashOutObj.stake.amount;
    this.cashOutObj.stakePerLine = updatedCashOutObj.stake.stakePerLine;
    this.cashOutObj.cashoutValue = updatedCashOutObj.cashoutValue;
    this.cashOutObj.potentialPayout = this.getPotentialPayout(updatedCashOutObj);
    this.cashOutObj.isPartialCashOutAvailable = updatedCashOutObj.partialCashout.available === this.cashoutConstants.result.YES;
  }

  /**
   * Check cash out status ('cashoutStatus') after partial cashed out
   * @param updatedCashOutObj {Object}
   */
  private checkPartialCashOutStatus(updatedCashOutObj) {
    const doesBetWorthNothing = this.cashoutConstants.betWorthNothing === updatedCashOutObj.cashoutValue;
    updatedCashOutObj.currencySymbol = this.cashOutObj.currencySymbol;

    // Check if filtered error received after getBetDetail for bet;
    if (this.isFilteredError(updatedCashOutObj) || doesBetWorthNothing) {
      this.cashOutObj.panelMsg = this.cashOutErrorMessage.getErrorMessage(updatedCashOutObj);

      this.enableCashOut();
      this.makeCashOutUnavailable();
      this.cashOutObj.isConfirmed = false;
    } else {
      const liveBetUpdateParams = { betId: this.cashOutObj.betId, prevCashoutStatus: this.cashOutObj.isCashOutUnavailable };
      this.pubsub.publish(this.pubsub.API.LIVE_BET_UPDATE, liveBetUpdateParams);
    }
  }

  /**
   * Use CashoutBet response to receive latest data
   */
  private updatePartialCashOutBet(result: ICashoutBetResponse): void {
    if (!result) {
      this.cashOutObj.setCashedOutState();
      return;
    }

    const updatedCashOutObj: IBet = Array.isArray(result.bet) ? result.bet[0] : result.bet;
    this.cashOutObj.lastTimeUpdate = Date.now();
    this.cashOutObj.betTermsChange = updatedCashOutObj && updatedCashOutObj.betTermsChange;
    this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, this.cashOutObj);

    this.rollbackPartialCashOutBetState(false);

    if (!updatedCashOutObj) {
      return;
    }

    if (Number(updatedCashOutObj.cashoutValue)) {
      this.setPartialCashOutParameters(updatedCashOutObj);
    } else {
      updatedCashOutObj.cashoutStatus = updatedCashOutObj.cashoutValue && updatedCashOutObj.cashoutValue.status;
      this.checkPartialCashOutStatus(updatedCashOutObj);
    }
  }
}
