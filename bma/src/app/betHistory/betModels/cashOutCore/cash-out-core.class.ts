import * as _ from 'underscore';

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
import { IGtmCashOutEvent } from 'app/core/models/gtm.event.model';
import { PubSubService } from 'app/core/services/communication/pubsub/pubsub.service';
import { IBetTermsChange, ICashoutBetResponse } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { ClientUserAgentService } from 'app/core/services/clientUserAgent/client-user-agent.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

export abstract class CashOutCore {

  readonly cashoutConstants = cashoutConstants;
  /**
   * @member {string}
   */
  id: string;

  /**
   * @member {object}
   */
  reqData: any;

  /**
   * Location from which cash out attempt made
   * @member {String}
   */
  betLocation: string;

  /**
   * Certain cash out bet data
   * @member {Object}
   */
  cashOutObj: ICashoutBet;

  /**
   * bet id received after cash out bet response
   * @member {String}
   */
  responseId: string;

  /**
   * delay received after cashout pending
   * @member {Number}
   */
  cashoutDelay: number;

  /**
   * set if cashout pending
   * @member {Boolean}
   */
  withCashoutDelay: boolean;

  /**
   * Bet data received after readBet/CashOutBet requests
   * @member {Object}
   */
  bet: IBetHistoryBet;

  /**
   * Sub error code received in readBet/CashOutBet requests
   * @member {String}
   */
  errorCode: string;

  /**
   * Constant with path to locale dictionary with read bet errors
   * @member {Object}
   * @private
   */
  readonly errorDictionary = 'bethistory.cashoutBet.cashoutAttemptErrors';

  /**
   * Constant with cash out errors that should be handled with special handlers
   * @member {Object}
   * @private
   */
  private readonly cashOutErrorsDictionary = {
    // Old codes, needs to deleted after cashout 2.0 will be implemented
    CASHOUT_UNAVAILABLE_PRICE_CHANGE: 'cashOutChanged',
    // Cashout 2.0 codes
    CASHOUT_VALUE_CHANGE: 'cashOutChanged',
  };

  constructor(
    public filterService: FiltersService,
    public localeService: LocaleService,
    public cashOutMapService: CashOutMapService,
    public gtm: GtmService,
    public cashOutDataProviderService: CashoutDataProvider,
    public toolsService: CoreToolsService,
    public cashOutErrorMessage: CashoutErrorMessageService,
    public pubsub: PubSubService,
    public awsService: AWSFirehoseService,
    public liveServConnectionService: LiveServConnectionService,
    public clientUserAgentService: ClientUserAgentService,
    public deviceService: DeviceService,
  ) { }


  /**
   * make cash out request
   * @param reqData {Object} - cash out request data
   * @param id {String} - current bet id
   * @param location {String} - location from which cash out is made
   */
  makeCashOut(reqData, currentBet, location: string): void {
    this.id = currentBet.betId;
    this.reqData = reqData;
    this.betLocation = this.getGtmBetLocation(location);
    this.cashOutObj = currentBet;
    this.cashoutDelay = 0;
    this.withCashoutDelay = false;

    this.cashOutDataProviderService.makeCashOutRequest(this.reqData)
      .subscribe((res: ICashoutBetResponse) => {
        this.cashOutRequestHandler(res);
      },
        () => {
          console.warn('makeCashOut REJECT response');
          this.cashOutDefault('FAILED_CASHOUT_REQUEST');
        });
  }

  /** THESE METHODS SHOULD BE OVERRIDE BY SPECIFIC CASH OUT IMPLEMENTATIONS */

  /**
   * Check if bet cashed out successfully
   * @return {boolean}
   */
  abstract isCashOutSuccessful(): boolean;

  /**
   * Handler for for successful cash out action
   */
  abstract handleSuccess(res: ICashoutBetResponse): void;

  /**
   * Handler for 'CASHOUT_VALUE_CHANGED' sub error code
   */
  abstract cashOutChanged(res: ICashoutBetResponse): void;

  /**
   * Default handler for all other sub error codes
   * @param errorOpt {Object}
   */
  abstract cashOutDefault(errorOpt): void;

  /**
   * Get error message depends on subErrorCode and error dictionary
   * @param opt {Object}
   * @return {String}
   * @protected
   */
  protected getErrorMsgFromDictionary(): string {
    if (!this.errorCode) {
      return this.localeService.getString(`${this.errorDictionary}.DEFAULT`);
    }

    const errorMsg = this.localeService.getString(`${this.errorDictionary}.${this.errorCode}`);
    if (errorMsg !== 'KEY_NOT_FOUND') {
      return errorMsg;
    }

    return this.localeService.getString(`${this.errorDictionary}.DEFAULT`);
  }

  /**
   * Should activate spinner if cashoutMap doesn't have bet objects
   * @returns {boolean}
   */
  protected spinnerActive(): boolean {
    return this.cashOutMapService.isEmptyObj(this.cashOutMapService.cashoutBetsMap);
  }

  /**
   * Get potential payout for cash out bet object
   * @param bet {object}
   * @returns {*}
   */
  protected getPotentialPayout(bet: IBetHistoryBet) {
    const potentialPayout = Number(bet.potentialPayout);

    const lastTermsPotentialPayout = _.last(bet.betTermsChange)?.potentialPayout;
    if (bet.betTermsChange && lastTermsPotentialPayout) {
      return lastTermsPotentialPayout.value || lastTermsPotentialPayout;
    }

    return potentialPayout || potentialPayout === 0 ? bet.potentialPayout : this.cashoutConstants.result.MISSED;
  }

  /**
   * Enable cash out for certain bet and updated appropriate statuses
   * @protected
   */
  protected enableCashOut(): void {
    this.cashOutObj.isDisable = false;
    this.cashOutObj.inProgress = false;
  }

  /**
   * Define cash out object as not available
   * @protected
   */
  protected makeCashOutUnavailable(): void {
    this.cashOutObj.isCashOutUnavailable = true;
    this.cashOutObj.isPartialCashOutAvailable = false;
  }

  /**
   * Check whether error is filtered by proxy
   * @param updatedCashOutObj {Object}
   * @return {boolean}
   * @protected
   */
  protected isFilteredError(updatedCashOutObj): boolean {
    return (updatedCashOutObj.cashoutStatus && this.cashoutConstants.status
      .some(value => updatedCashOutObj.cashoutStatus.indexOf(value) > -1)) ||
      _.contains(this.cashoutConstants.values, updatedCashOutObj.cashoutValue);
  }

  /**
   * send GTM tracking when cashout is successful
   * @param cashOutType {string}
   */
  protected sendGTMSuccessCashout(cashOutType: string): void {
    this.gtm.push(this.cashoutConstants.cashOutGtm.EVENT, _.extend({
      eventLabel: this.cashoutConstants.cashOutGtm.SUCCESS,
      successMessage: this.getGtmMsg(
        this.localeService.getString(cashOutType === this.cashoutConstants.cashOutType.PARTIAL ?
          'bethistory.partialCashOutSuccess' : 'bethistory.fullCashOutSuccess'), this.cashOutObj.panelMsg)
    }, this.getCashOutGtmObject(cashOutType)));
  }

  /**
   * send GTM tracking when cashout is failed
   * @param cashOutType {string}
   */
  protected sendGTMFailureCashout(cashOutType: string): void {
    this.gtm.push(this.cashoutConstants.cashOutGtm.EVENT, _.extend({
      eventLabel: this.cashoutConstants.cashOutGtm.FAILURE,
      errorMessage: this.getGtmMsg(
        this.localeService.getString('bethistory.cashoutBet.unsuccessCashout'), this.cashOutObj.attemptPanelMsg
      ),
      errorCode: this.changeStringFormat(this.errorCode)
    }, this.getCashOutGtmObject(cashOutType)));
  }

  /**
   * get partial Cashout offer value
   * @returns {number}
   */
  protected getPartialCashoutOffer(): number {
    return this.toolsService.roundDown(this.cashOutObj.cashoutValue / 100 * this.cashOutObj.partialCashOutPercentage, 2);
  }

  /**
   *  track aws event for cash out
   * @params {actionName} string
   * @params {error} Object of ICashoutError type
   * @params {status} string
   * @returns void
   */
  protected awsCashOut(actionName: string, status: string, error?: ICashoutError): void {
    const analyticsParams = {
      liveServConnectionStatus: this.liveServConnectionService.isConnected() ? 'active' : 'down',
      userAgent: this.deviceService.parsedUA.ua,
      route: this.betLocation,
      agent: this.clientUserAgentService.getId(),
      status: status,
      errorCode: error && error.errorCode,
      errorDictionary: error && error.errorDictionary,
      cashoutDelay: this.cashoutDelay,
      withCashoutDelay: this.withCashoutDelay,
      betId: this.id,
    };
    if (this.bet) {
      Object.assign(analyticsParams, {
        cashoutStatus: typeof (this.bet.cashoutValue) === 'string' ? null : (this.bet.cashoutValue as ICashoutValue).status,
        cashoutValue: typeof (this.bet.cashoutValue) === 'string' ? this.bet.cashoutValue : (this.bet.cashoutValue as ICashoutValue).amount,
        betId: this.bet.id,
        cashoutBetDelayId: this.bet.cashoutBetDelayId,
      });
    }
    this.awsService.addAction(actionName, analyticsParams);
  }

  /**
   * Handle cash out request response
   * @param res {Object}
   * @private
   */
  private cashOutRequestHandler(res: ICashoutBetResponse): void {
    this.bet = this.getBetFromResponse(res);

    // when cashOutObj is undefined do not proceed with stategy
    if (!this.cashOutObj) {
      // one of the case is when user is logged out from another tab or session expires
      console.warn('The attempted cashout failed because cashOutObj is not available.');
      return;
    }

    if (this.getErrorCode(res)) {
      if (this.errorCode === this.cashoutConstants.pending) {
        this.cashOutPending(res);
        return;
      }

      this.cashOutObj.isCashOutBetError = true;
      this[(this.cashOutErrorsDictionary[this.errorCode] || 'cashOutDefault')](res);
    } else if (this.isCashOutSuccessful()) {
      this.handleSuccess(res);
    } else {
      this.cashOutDefault(null);
    }
  }

  /**
   * Make read bet request to check cash out possibility
   * @private
   */
  private makeReadBet(): void {
    this.cashOutDataProviderService.makeReadBetRequest(this.responseId, this.reqData)
      .subscribe(res => this.readBetRequestHandler(res), () => {
        console.warn('makeReadBetRequest REJECT response');
        this.cashOutDefault('FAILED_READBET_REQUEST');
      });
  }

  /**
   * Update cashOutObj with response bet payout
   */
  private updateCashOutObjPayout() {
    if (this.bet.payout) {
      const payout = this.bet.payout[0];
      this.cashOutObj.cashoutValue = payout.winnings || this.cashOutObj.cashoutValue;
      this.cashOutObj.potentialPayout = payout.potential || this.cashOutObj.potentialPayout;
      this.cashOutObj.bonus = payout.bonus || this.cashOutObj.bonus;
      this.cashOutObj.refund = payout.refunds || this.cashOutObj.refund;
    }
  }

  /**
   * Handle read bet request response
   * @param res {Object}
   * @private
   */
  private readBetRequestHandler(res): void {
    this.bet = this.getBetFromResponse(res);

    // check if bet cashed out successfully
    if (this.isCashOutSuccessful()) {
      this.updateCashOutObjPayout();
      this.handleSuccess(res);
      return;
    }

    // handle sub error if received
    if (this.getErrorCode(res)) {
      if (this.errorCode === this.cashoutConstants.pending) {
        // make additional makeReadBet request after 2 seconds, because last one return CASHOUT_PENDING
        // ( although this flow is similar to cashOutPending(),
        //   the solution with hardcoded delay 2sec for secondary pending flow refers to legacy code from 2017,
        //   so won't include countdown that relies on cashoutDelay )
        setTimeout(() => {
          this.makeReadBet();
        }, this.cashoutConstants.readBetTime);
        return;
      }

      this.cashOutObj.isCashOutBetError = true;
      this[(this.cashOutErrorsDictionary[this.errorCode] || 'cashOutDefault')](res);
      return;
    }

    // handler for response without sub error code
    this.cashOutDefault(null);
  }

  /**
   * Handler for pending cash out action
   * @param res {Object}
   * @private
   */
  private cashOutPending(res): void {
    const
      betError = res.betError,
      delay = (betError && +betError.cashoutDelay) || 0;

    this.responseId = betError && betError.cashoutBetDelayId; // bet id from makeCashOut Response
    this.cashoutDelay = delay;
    this.withCashoutDelay = true;

    // delay before make Read Bet request
    this.pubsub.publishSync(this.pubsub.API.CASHOUT_COUNTDOWN_TIMER, delay);
    setTimeout(() => {
      this.makeReadBet();
    }, delay * 1000);
  }

  /**
   * Parse readBet/CashOutBet requests responses and get bet data
   * @param res {Object}
   * @return {Object}
   * @private
   */
  private getBetFromResponse(res): IBetHistoryBet {
    return (res && res.bet) ? this.getBetObject(res.bet) : null;
  }

  /**
   * Get subErrorCode property from readBet/CashOutBet requests responses
   * @param res {Object}
   * @private
   */
  private getErrorCode(res): string {
    let errorCode;
    const subErrorCode = res && res.betError && res.betError.subErrorCode;
    if (subErrorCode) {
      errorCode = subErrorCode;
    } else {
      // Case when error code received after BiR counter
      const betFromResponse = this.getBetFromResponse(res),
        cashoutAmountValue = betFromResponse && betFromResponse.cashoutValue
          && (betFromResponse.cashoutValue as ICashoutValue).amount;
      errorCode = cashoutAmountValue && isNaN(Number(cashoutAmountValue)) ? cashoutAmountValue : null;
    }

    this.errorCode = errorCode;
    return this.errorCode;
  }

  /**
   * Return bet object
   * @param bet {Object|Array}
   * @returns {Object|Boolean}
   */
  private getBetObject(bet: IBetHistoryBet): IBetHistoryBet {
    if (_.isArray(bet)) {
      return bet[0];
    }

    if (!!bet && bet.constructor.toString().indexOf('Object') > 0) {
      return bet;
    }

    return null;
  }

  /**
   * Modify message for appropriate pattern
   * @param message {string}
   * @return {string}
   * @private
   */
  private changeStringFormat(message: string): string {
    return message ? message.toLowerCase().replace(/_/g, ' ') : null;
  }

  /**
   * Form basic GTM for cash out attempt
   * @return {Object}
   * @private
   */
  private getCashOutGtmObject(cashOutType: string): IGtmCashOutEvent {
    const gtmObject: IGtmCashOutEvent = {
      eventCategory: this.cashoutConstants.cashOutGtm.CATEGORY,
      eventAction: this.cashoutConstants.cashOutGtm.ACTION,
      location: this.betLocation,
      cashOutOffer: Number(this.cashOutObj.gtmCashoutValue),
      oddsBoost: this.isCashoutBetBoosted() ? 'yes' : 'no',
      cashOutType
    };

    // add additional properties for partial cash out attempt
    if (this.cashOutObj.partialCashOutPercentage && this.cashOutObj.partialCashOutPercentage !== 100) {
      gtmObject.partialPercentage = this.cashOutObj.partialCashOutPercentage;
      gtmObject.cashOutOffer = this.getPartialCashoutOffer();
    }
     // add additional properties for Lucky Bonus Types
    if(['L15', 'L31', 'L63'].includes(this.cashOutObj.betType) && this.cashOutObj.availableBonuses && this.cashOutObj.availableBonuses.availableBonus){
     gtmObject['component.EventDetails'] = (this.cashOutObj.betType.replace(/L/g,"Lucky ")) + " - bonuses";
    }
    return gtmObject;
  }

  private isCashoutBetBoosted(): boolean {
    return this.cashOutObj.betTermsChange ?
      _.some(this.cashOutObj.betTermsChange, (betTerms: IBetTermsChange) => betTerms.reasonCode === 'ODDS_BOOST') : false;
  }

  /**
   * Get message for cash out attempt
   * @param attemptMsg {string}
   * @param attemptPanelObj {Object}
   * @return {string}
   * @private
   */
  private getGtmMsg(attemptMsg: string, attemptPanelObj): string {
    return this.changeStringFormat(attemptPanelObj.msg
      ? `${attemptMsg}, ${attemptPanelObj.msg}` : attemptMsg);
  }

  /**
   * get bet location for GTM tracking
   * @param location {string} 'cashOutSection' or 'myBetsTab'
   * @returns {string}
   */
  private getGtmBetLocation(location: string): string {
    return location === this.cashoutConstants.betLocation.CASH_OUT_SECTION
      ? this.cashoutConstants.gtmBetLocation.CASH_OUT_SECTION : this.cashoutConstants.gtmBetLocation.MY_BETS;
  }
}
