import { Injectable } from '@angular/core';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { IPanelStateConfig } from '@app/betHistory/models/cashout-panel.model';
import { ICashOutData } from '@app/betHistory/models/cashout-section.model';
import * as _ from 'underscore';
import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { cashoutConstants } from '../../constants/cashout.constant';
import { CashOutMapService } from '../../services/cashOutMap/cash-out-map.service';
import { CashOutService } from '../../services/cashOutService/cash-out.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { StorageService } from '@app/core/services/storage/storage.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutPanelService {

  private timer: number;

  constructor(private cashOutMapService: CashOutMapService,
              private cashOutService: CashOutService,
              private localeService: LocaleService,
              private windowRef: WindowRefService,
              private toolsService: CoreToolsService,
              private pubsub: PubSubService,
              private editMyAccaService: EditMyAccaService,
              public storageService: StorageService) {}

  /**
   * Does full or partial cash out for bet
   * @param {Object} cashoutData
   * @param {string} location
   * @param {Object} bet
   * @param {string} type - shows what btn was clicked
   * @returns {function}
   */
  doCashOut(cashoutData: ICashOutData[], location: string, bet: CashoutBet, type: string): void {
    bet.gtmCashoutValue = bet.cashoutValue;
    bet.resetCashoutSuccessState();
    this.editMyAccaService.removeSavedAcca(bet.id);
    if (type === 'full' && this.isPartialActive(bet)) {
      this.setPartialState(bet, false);
    } else if (type === 'partial' && !this.isPartialActive(bet)) {
      this.setPartialState(bet, true);
    } else {
      this.triggerCashOut(cashoutData, location, bet);
    }
  }

  /**
   * Check if cashout button should be shown
   * @param {Object} bet data
   * @param {String} betLocation
   * return Boolean
   */
  isButtonShown(bet: CashoutBet, betLocation: string): boolean {
    return betLocation === 'myBetsTab' ? bet.type !== 'placedBetsWithoutCashoutPossibility' : true;
  }

  /**
   * Get current button state
   * Order of statements metters
   *
   * @param bet {object}
   * @returns {string}
   */
  getButtonState(bet: CashoutBet): string {
    //  ______________________________________________________________________________________________________________`
    // |                               |                           |                        |       |       | depreca- |
    // |       button state            |  key in cash out bet      |     button text        | color | disa- | ted case?|
    // |_______________________________|_________object____________|________________________|_______|_bled?_|__________|
    // |base                           |                           |               CASH OUT |ORANGE |  NO   |          |
    // |isPartial                      | isPartialActive           |               CASH OUT |ORANGE |  NO   |          |
    // |unavailable (suspend)          | isCashOutUnavailable      |      UNAVAILABLE + msg |ORANGE |  YES  |*CovOnView|
    // |in progress (do cash out)      | inProgress                |                spinner | GREEN |  YES  |          |
    // |success                        | isCashOutedBetSuccess     |                SUCCESS | GREEN |  NO   |*CovOnView|
    // |decrease (price decrease)      | isPriceDecrease           |               CASH OUT |  BLUE |  NO   |    YES?  |
    // |error                          | isCashOutBetError         | Error msg or UNSUCCESS | GREEN |  NO   |          |
    // |confirm cash out               | isConfirmInProgress       |       CONFIRM CASH OUT | GREEN |  NO   |
    // |_______________________________|___________________________|________________________|_______|_______|__________|

    if (this.isUnsuccessful(bet)) {
      return 'error';
    }
    if (this.isSuccessful(bet)) {
      return 'success';
    }
    if (this.isBetInProgress(bet)) {
      return 'progress';
    }
    if (this.isUnavailable(bet)) {
      return 'unavailable';
    }
    if (this.isConfirmInProgress(bet)) {
      return 'confirm';
    }
    if (this.isPartialActive(bet)) {
      return 'partial';
    }
    return 'base';
  }

  /**
   * Get config with text and value for all states
   * @param bet {object}
   * @returns {Object}
   */
  getStateConfig(bet: CashoutBet): IPanelStateConfig {
    return {
      error: {
        text: '',
        value: _.noop
      },
      success: {
        text: '',
        value: () => this.addCurrency(bet.valueToCashout, bet)
      },
      progress: {
        text: '',
        value: _.noop
      },
      confirm: {
        text: this.localeService.getString('bethistory.cashoutBet.confirmCashOut'),
        value: () => this.addCurrency(this.getCashOutValueWithPartial(bet), bet)
      },
      unavailable: {
        text: this.localeService.getString('bethistory.cashoutBet.cashOutBetSuspended'),
        value: _.noop
      },
      partial: {
        text: this.localeService.getString('bethistory.partialCashoutButton.cashout'),
        value: () => this.getCashOutValueWithPartial(bet)
      },
      base: {
        text: this.localeService.getString('bethistory.cashoutBet.cashOut'),
        value: () => this.addCurrency(this.getCashOutValue(bet), bet)
      }
    };
  }

  /**
   * Check if partial cashout available
   * @param {Object} bet - data
   * @returns {boolean}
   */
  isPartialAvailable(bet: CashoutBet): boolean {
    return bet.isPartialCashOutAvailable;
  }

  setPartialState(bet: CashoutBet, value: boolean): void {
    const fullCashOutPercentage = 100;
    bet.isPartialActive = value;
    if (value) {
      bet.partialCashOutPercentage = 0;
      bet.animating = true;
      this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, bet);

      this.windowRef.nativeWindow.setTimeout(() => {
        bet.partialCashOutPercentage = fullCashOutPercentage / 2;
        this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, bet);

        this.windowRef.nativeWindow.setTimeout(() => { // remove animation effects after this timeout
            bet.animating = false;
            this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, bet);
          }, cashoutConstants.partialFinishAnimating);
      }, cashoutConstants.partialAnimatingTime);
    } else {
      bet.partialCashOutPercentage = fullCashOutPercentage;

      this.windowRef.nativeWindow.clearTimeout(this.timer);
      this.cancelCashout(bet);
    }
  }

  /**
   * Sets params to choose strategy and for cashout
   * @param currentBet {object}
   * @returns {object}
   */
  private doCashOutParamsSetting(currentBet: CashoutBet) {
    const partialData = {
      partialCashOutAmount: null,
      partialCashOutPercentage: null
    }, reqData = {
      betId: currentBet.betId,
      cashOutAmount: currentBet.cashoutValue,
      currency: currentBet.currency
    }, isPartial = currentBet.partialCashOutPercentage && currentBet.partialCashOutPercentage !== 100;
    currentBet.isDisable = false;
    // store value that will be cashouted
    currentBet.valueToCashout = <string>this.getCashOutValueWithPartial(currentBet);

    if (isPartial) {
      partialData.partialCashOutAmount = this.toolsService.roundDown(Number(currentBet.cashoutValue) /
        100 * currentBet.partialCashOutPercentage, 2);
      partialData.partialCashOutPercentage = currentBet.partialCashOutPercentage;
    }

    return {
      partialData,
      reqData,
      isPartial
    };
  }

  /**
   * Decides what strategy to use and runs it
   * @param {object}
   */
  private runStrategy({ currentBet, reqData, partialData, isPartial, location }) {
    currentBet.inProgress = true;
    if (!isPartial) {
      this.cashOutService.createFullCashOut().makeCashOut(reqData, currentBet, location);
        /**
     * delete the bet id from local storage when we do the cashout 
     */
      const signPostData = this.storageService.get('myBetsSignPostingData');
      if(signPostData){
        currentBet.event.forEach((eventId: any) => {
          const eventIdIndex = signPostData.findIndex(eventData => Number(eventData.eventId) === Number(eventId));
          if(eventIdIndex > -1) {
            const betIndex = signPostData[eventIdIndex].betIds.findIndex(betId => Number(betId) === Number(currentBet.betId))
              if (betIndex > -1) {
                signPostData[eventIdIndex].betIds.splice(betIndex, 1);
              }
          }
      });
        this.storageService.set('myBetsSignPostingData', signPostData);
      }
    } else {
      this.cashOutService.createPartialCashOut().makeCashOut(_.defaults(reqData, partialData), currentBet, location);
    }
  }

  /**
   * Does full or partial cash out for bet
   * @param {Object} cashoutData
   * @param {string} location
   * @param {string} id - betId
   * @returns {function}
   */
  private triggerCashOut(cashoutData: ICashOutData[], location: string, currentBet: CashoutBet) {
    const
      initialData = this.doCashOutParamsSetting(currentBet),
      {
        partialData,
        reqData,
        isPartial
      } = initialData;

    if (!this.cashOutMapService.cashoutBetsMap.mapState.isUserLogOut) {
      if (currentBet.isConfirmInProgress) {
        currentBet.isConfirmInProgress = false;
        // cancel timeout for confirm cashout
        this.windowRef.nativeWindow.clearTimeout(this.timer);
        currentBet.isDisable = true;
        // check full cashout or partial
        this.runStrategy({ currentBet, reqData, partialData, isPartial, location });
      } else {
        currentBet.isConfirmInProgress = true;
        // time out cashout
        this.timeOutCashout(currentBet);
      }
    }
  }

  /**
   * Retrieves data about successful cashout status
   * @param {Object} bet data
   * return Boolean
   */
  private isSuccessful(bet: CashoutBet) {
    return bet.panelMsg && (bet.panelMsg.type === 'success') &&
      !bet.isCashOutUnavailable && !bet.isCashOutBetError &&
      bet.type !== 'placedBetsWithoutCashoutPossibility';
  }

  /**
   * Check if cashout bet has error when attempting to do cash out for certain bet
   * @param {Object} bet data
   * return Boolean
   */
  private isUnsuccessful(bet: CashoutBet): boolean {
    return bet.isCashOutBetError;
  }

  /**
   * If we have placedBets (we are on my Bets tab) we check to show error if current bet's cashout is unavailable
   * and type of bet is not 'placedBetsWithoutCashoutPossibility'
   * otherwise when we are on full cashout tab we check only cashout status
   * Retrieves data about whether bet has a cashout
   * @param {Object} bet data
   * @returns {Boolean}
   */
  private isUnavailable(bet: CashoutBet): boolean {
    return bet.isCashOutUnavailable;
  }

  /**
   * Get cashout value
   * @param {Object} bet - data
   * @returns {string}
   */
  private getCashOutValue(bet: CashoutBet): number | string {
    return bet.cashoutValue;
  }

  /**
   * Get cashout value, taking to account partial
   * @param {Object} bet - data
   * @returns {string}
   */
  private getCashOutValueWithPartial(bet: CashoutBet) {
    return bet.partialCashOutPercentage === 100 ? bet.cashoutValue
      : this.toolsService.roundDown((Number(bet.cashoutValue) / 100 * bet.partialCashOutPercentage), 2).toFixed(2);
  }

  /**
   * Time out confirm cashout after set time
   * @param {object} currentBet
   */
  private timeOutCashout(currentBet: CashoutBet) {
    this.timer = this.windowRef.nativeWindow.setTimeout(() => { this.cancelCashout(currentBet); }, cashoutConstants.flashingTime);
  }

  private cancelCashout(bet: CashoutBet) {
    bet.isDisable = false;
    bet.isConfirmInProgress = false;

    this.pubsub.publish(this.pubsub.API.UPDATE_CASHOUT_BET, bet);
    this.pubsub.publish(this.pubsub.API.CASHOUT_COUNTDOWN_TIMER, null);
  }

  /**
   * Check whether full or partial cashout are in progress
   * @param {Object} bet
   */
  private isBetInProgress(bet: CashoutBet): boolean {
    return bet.inProgress;
  }

  /**
   * Check if confirm state
   * @param {Object} bet - data
   * @returns {boolean}
   */
  private isConfirmInProgress(bet: CashoutBet): boolean {
    return bet.isConfirmInProgress;
  }

  /**
   * Check if partial cashout activated
   * @param {Object} bet - data
   * @returns {boolean}
   */
  private isPartialActive(bet: CashoutBet): boolean {
    return bet.isPartialActive;
  }

  /**
   * Add currency symbol to value
   * @param value {(string|number)}
   * @param bet {object}
   * @returns {string}
   */
  private addCurrency(value: string | number, bet: CashoutBet) {
    return `${bet.currencySymbol}${_.isNumber(value) ? Number(value).toFixed(2) : value}`;
  }
}
