import * as _ from 'underscore';

import { IBetDetail, IBetTermsChange, IClaimedOffer } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryOutcome, IOutcome } from 'app/core/models/outcome.model';
import { IMarket } from 'app/core/models/market.model';

import { ISportEvent } from 'app/core/models/sport-event.model';
import { IBetHistoryLeg, IBetHistoryPart, IBetTags } from '../../models/bet-history.model';
import { IPanelMsg } from '@app/betHistory/models/bet-history-bet.model';
import { cashoutConstants } from '../../constants/cashout.constant';
import { CashoutErrorMessageService } from '@app/betHistory/services/cashoutErrorMessageService/cashout-error-message.service';

export class RegularBetBase {

  outcome: IBetHistoryOutcome[];
  market: string[];
  event: string[];

  inProgress: boolean;
  panelMsg: IPanelMsg;
  attemptPanelMsg: IPanelMsg;
  isConfirmed: boolean;
  isPartialActive: boolean;
  isPartialCashOutAvailable: boolean;
  isCashOutedBetSuccess: boolean;
  isCashOutBetError: boolean;
  isConfirmInProgress: boolean;
  isPriceDecrease: boolean;
  partialCashOutPercentage: number;
  cashoutValue: number | string;
  errorDictionary: any;
  totalStatus: string;
  isDisable: boolean;
  partialCashoutAvailable: string;
  partialCashoutStatus: string;
  valueToCashout?: string;
  betType: string;
  tokenValue?: number;
  tokenType?: string;
  betTags?: IBetTags;
  animating?: boolean;

  events: { [key: string]: ISportEvent };
  markets: { [key: string]: IMarket };
  outcomes: { [key: string]: IOutcome };

  lastTimeUpdate: number;
  currency: string;
  currencySymbol: string;
  time: number;
  date: string;
  betId: string;
  cashoutStatus: string;
  type?: string;
  id: string;
  receipt?: string;
  cashoutSuccessMessage?: string;
  betIsFullyCashedOut?: boolean;

  potentialPayout: number | string;
  isCashOutUnavailable: boolean;

  leg: IBetHistoryLeg[];
  legType?: string;

  minEventStartTimeStemp: number;
  settled?: string;
  allSilkNames?: string[];

  betTermsChange?: IBetTermsChange[];
  claimedOffers?: {
    claimedOffer: IClaimedOffer[]
  };

  accaHistory?: {
    isOriginal: boolean;
    isBoosted: boolean;
    isExpanded?: boolean;
    partialCashoutHistory: boolean;
    time: string;
    cashoutUsed: string;
    cashoutUsedMsg: string;
  };
  isAccaEdit?: boolean;
  hasFreeBet?: boolean;

  constructor(bet, betModelService, currency, currencySymbol,
              public cashOutMapIndex,
              public cashOutErrorMessage: CashoutErrorMessageService) {
    this.init(bet);

    this.outcome = [];
    this.market = [];
    this.event = [];

    this.outcomes = {};
    this.markets = {};
    this.events = {};

    this.lastTimeUpdate = Date.now();
    this.currency = currency;
    this.currencySymbol = currencySymbol;
    this.time = betModelService.getBetTimeString(this.date);

    this.isDisable = true;
    this.isCashOutUnavailable = true;

    this.leg = this.leg || [];
    this.leg = _.isArray(this.leg) ? this.leg : [this.leg];

    /**
     * on cashout tab bet has field tokenValue which contain free bet value
     * on my bets tab bet has totalStake with tokenValue
     */
    this.hasFreeBet = bet.tokenValue && Number(bet.tokenValue) > 0 || bet.stake && Number(bet.stake.tokenValue) > 0;

    this.minEventStartTimeStemp = _.min(_.map(this.leg, leg => {
      const startTime = leg.part[0].startTime || leg.part[0].outcome[0].event.startTime || '';
      const startTimeFormatted = new Date(Date.parse(startTime)).toUTCString();
      return new Date(startTimeFormatted).getTime();
    }));
  }

  /*
   * Suspended status by cashout status code
   */
  get isCashoutSuspendedState(): boolean {
    return this.isCashOutUnavailable && this.panelMsg
      && this.panelMsg.type === cashoutConstants.cashOutAttempt.SUSPENDED;
  }

  set isCashoutSuspendedState(value:boolean){}
  /**
   * Is bet Cashed Out
   */
  get isCashedOut(): boolean {
    return this.betIsFullyCashedOut || this.cashoutStatus === cashoutConstants.betSettledStatus;
  }

  set isCashedOut(value: boolean){}
  /**
   * This method should be called when bet is FULLY Cashed out,
   * it sets fully cash out state to true
   */
  setCashedOutState(): void {
    this.betIsFullyCashedOut = true;
  }

  /**
   * Reset cashout suspended state
   */
  resetCashoutSuspendedState(): void {
    this.isCashOutUnavailable = false;
    this.panelMsg = {
      type: undefined,
      msg: undefined
    };
  }

  /**
   * Set cashed out state both Partial or Full
   * @param cashoutSuccessMessage - success message
   */
  setCashoutSuccessState(cashoutSuccessMessage: string): void {
    this.cashoutSuccessMessage = cashoutSuccessMessage;
  }

  /**
   * Reset cashed out state both Partial or Full
   */
  resetCashoutSuccessState(): void {
    this.cashoutSuccessMessage = '';
  }

  initializeItemsArrays(legItem: IBetHistoryLeg): void {
    _.forEach(legItem.part, (part: IBetHistoryPart) => {
      const outcomeId = _.isString(part.outcome) ? part.outcome :
        part.outcomeId || part.outcome[0].id;

      if (!_.contains(this.outcome, outcomeId)) {
        this.outcome.push(outcomeId);
      }
    });

    const eventId = legItem.part[0].eventId || legItem.part[0].outcome[0].event.id;
    if (!_.contains(this.event, eventId)) {
      this.event.push(eventId);
    }

    const marketId = legItem.part[0].marketId || legItem.part[0].outcome[0].market.id;
    if (!_.contains(this.market, marketId)) {
      this.market.push(marketId);
    }
  }

  initializeCashOutMap(legItem: IBetHistoryLeg, isBetSettled: boolean = false): void {
    this.cashOutMapIndex.create('event', legItem.part[0].eventId, this.betId, isBetSettled);
    _.forEach(legItem.part, part => {
      const outcomeId = _.isString(part.outcome) ? part.outcome : part.outcomeId;
      this.cashOutMapIndex.create('outcome', outcomeId, this.betId, isBetSettled);
    });
    this.cashOutMapIndex.create('market', legItem.part[0].marketId, this.betId, isBetSettled);
  }


  handleError(msg: string, cashOutValue: number, type: string): void {
    const errorHandlerName = type || 'defaultType';
    this.inProgress = false;
    this.isCashOutBetError = true;

    this.errorDictionary[errorHandlerName](this, cashOutValue);
    this.attemptPanelMsg = {
      type: 'error',
      msg
    };
  }

  handleSuccess(): void {
    this.inProgress = false;
    this.isCashOutedBetSuccess = true;
    this.isCashOutBetError = false;
    this.isDisable = false;
    this.attemptPanelMsg = {
      type: undefined,
      msg: undefined
    };
    this.totalStatus = 'cashed out';

    setTimeout(() => {
      this.isCashOutBetError = false;
      this.attemptPanelMsg = {};
    }, cashoutConstants.displaySuccess);
  }

  protected setCashoutProperties(bet): void {
    this.errorDictionary = {
      decrease(betObj, cashOutValue) {
        betObj.cashoutValue = parseFloat(cashOutValue);
        betObj.isDisable = false;
        betObj.isPriceDecrease = true;
        betObj.isConfirmed = false;

        setTimeout(() => {
          betObj.isCashOutBetError = false;
          betObj.attemptPanelMsg = {};
        }, cashoutConstants.tooltipTime);
      },
      defaultType(betObj) {
        betObj.isDisable = true;
      }
    };

    this.panelMsg = {
      type: undefined,
      msg: undefined
    };
    this.attemptPanelMsg = {
      type: undefined,
      msg: undefined
    };

    this.partialCashOutPercentage = 100;
    this.isCashOutUnavailable = !(bet.cashoutValue && Number(bet.cashoutValue));
    this.isConfirmed = false;
    this.isPartialActive = false;
    this.isCashOutedBetSuccess = false;
    this.isCashOutBetError = false;
    this.isDisable = false;
    this.isConfirmInProgress = false;
    this.inProgress = false;
    this.isPriceDecrease = false;
    this.betIsFullyCashedOut = false;

    if (this.isCashOutUnavailable) {
      if (isNaN(this.cashoutValue as number)) {
        this.cashoutStatus = `${this.cashoutValue}`;
      }
      this.panelMsg = this.cashOutErrorMessage.getErrorMessage(this);
    }

    this.isPartialCashOutAvailable = bet.partialCashoutAvailable === 'Y';

    _.each(this.leg, legItem => {
      // item.isEventEntity; - call (for get event object by eventId from SS) will create and assign
      // (true/false) value for isEventEntity variable
      legItem.cashoutId = this.betId;
      this.initializeCashOutMap(legItem);
    });
  }

  /**
   * Initializes bet properties
   * @param bet
   * @private
   */
  private init(bet: IBetDetail[]): void {
    _.each(bet, (propValue, propKey) => {
      this[propKey] = propValue;
    });
  }
}
