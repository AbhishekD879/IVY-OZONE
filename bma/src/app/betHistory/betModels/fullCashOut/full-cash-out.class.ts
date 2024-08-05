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
import { IBetHistoryBet, ICashoutError, ICashoutValue } from '../../models/bet-history.model';
import { PubSubService } from 'app/core/services/communication/pubsub/pubsub.service';
import { ClientUserAgentService } from 'app/core/services/clientUserAgent/client-user-agent.service';
import { CashoutBetsStreamService } from 'app/betHistory/services/cashoutBetsStream/cashout-bets-stream.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

export class FullCashOut extends CashOutCore {

  readonly cashoutConstants = cashoutConstants;
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
   deviceService: DeviceService,
   private cashoutBetsStreamService: CashoutBetsStreamService,
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
      (this.bet.isSettled === this.cashoutConstants.result.YES);
  }

  /**
   * Handler for for successful cash out action
   */
  handleSuccess(): void {
    this.pubsub.publish(this.pubsub.API.CASH_OUT_BET_PROCESSED, this.cashOutObj.betId);
    this.cashOutObj.handleSuccess();
    this.cashOutObj.panelMsg = {
      type: this.cashoutConstants.cashOutAttempt.SUCCESS,
      msg: ''
    };

    this.cashOutObj.setCashoutSuccessState(this.localeService.getString('bethistory.fullCashOutSuccess'));
    this.cashOutObj.setCashedOutState();

    this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, this.cashOutObj);
    this.pubsub.publish(this.pubsub.API.BETS_COUNTER_CASHOUT_BET);
    this.sendGTMSuccessCashout(this.cashoutConstants.cashOutType.FULL);
    this.awsCashOut('FullCashOut=>makeCashOut=>Success', this.cashoutConstants.cashOutAttempt.SUCCESS);
    this.cashoutBetsStreamService.updateCashedOutBet(this.cashOutObj);
  }

  /**
   * Handler for 'CASHOUT_VALUE_CHANGED' sub error code
   */
  cashOutChanged(): void {
    this.handleError(null, (<ICashoutValue>this.bet.cashoutValue).amount, this.cashoutConstants.decrease);
  }

  /**
   * Default handler for all other sub error codes
   * @param errorOpt {Object}
   */
  cashOutDefault(errorOpt): void {
    this.handleError(errorOpt, null, null);
  }

  /**
   * Final error handling with updating bet data
   * @param errorOpt {Object}
   * @param cashOutValue {string}
   * @param type {string}
   * @private
   */
  private handleError(errorOpt, cashOutValue: string, type: string) {
    const errorDictionary = this.getErrorMsgFromDictionary();
    this.cashOutObj.handleError(errorDictionary, cashOutValue, type);
    this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, this.cashOutObj);
    this.resetErrorStateAfter(this.cashoutConstants.tooltipTime);
    this.sendGTMFailureCashout(this.cashoutConstants.cashOutType.FULL);
    this.awsCashOut('FullCashOut=>makeCashOut=>Error', this.cashoutConstants.cashOutAttempt.ERROR,
      { errorCode: this.errorCode ? this.errorCode : errorOpt, errorDictionary } as ICashoutError);
    this.cashoutBetsStreamService.getCashoutBet([this.cashOutObj.betId])
      .subscribe(result => this.updateAfterError(result));
  }

  /**
   * Hide error message and clear error state of cashout (isDisable affects cashOutLiveServeUpdates subscription)
   */
  private resetErrorStateAfter(delay: number) {
    setTimeout(() => {
      this.cashOutObj.isCashOutBetError = false;
      this.cashOutObj.attemptPanelMsg = {};
      this.cashOutObj.isDisable = false;
      this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, this.cashOutObj);
    }, delay);
  }
  /**
   * Update bet with latest data after cash out attempt
   * @param result {Object}
   * @private
   */
  private updateAfterError(result) {
    if (!result) {
      return;
    }

    const updatedCashOutObj = result.length ? result[0] : result;
    const doesBetWorthNothing = this.cashoutConstants.betWorthNothing === updatedCashOutObj.cashoutValue;

    if (updatedCashOutObj.cashoutValue && (!Number(updatedCashOutObj.cashoutValue) || doesBetWorthNothing)) {
      if (this.isFilteredError(updatedCashOutObj) || doesBetWorthNothing) {
        this.cashOutObj.isConfirmed = false;
        if (doesBetWorthNothing) {
          updatedCashOutObj.currencySymbol = this.cashOutObj.currencySymbol;
          this.cashOutObj.panelMsg = this.cashOutErrorMessage.getErrorMessage(updatedCashOutObj);
        }

        this.makeCashOutUnavailable();
        this.enableCashOut();
      } else {
        const liveBetUpdateParams = {
          betId: this.cashOutObj.betId,
          prevCashoutStatus: this.cashOutObj.isCashOutUnavailable
        };
        this.pubsub.publish(this.pubsub.API.LIVE_BET_UPDATE, liveBetUpdateParams);
      }
    }
  }
}
