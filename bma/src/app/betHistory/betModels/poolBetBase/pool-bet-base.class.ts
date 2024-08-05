import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { TimeService } from '@core/services/time/time.service';
import { BetHistoryMainService } from '../../services/betHistoryMain/bet-history-main.service';
import { CashoutMapIndexService } from '../../services/cashOutMapIndex/cashout-map-index.service';
import { IBetHistoryLeg, IBetHistoryPart, IBetHistoryPoolBet, IBetHistoryStake } from 'app/betHistory/models/bet-history.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { CurrencyPipe } from '@angular/common';

export default class PoolBetBase {
  date: string;
  id: number | string;
  status: string;
  lines: number;
  receipt: string;
  stake: string;
  totalStake: string;
  tokenValue: number;
  winLines: string;
  numLegs: number;
  currency: string;
  isSettled: boolean;
  totalReturns: string;
  showLegsNumberInTitle: boolean;
  showEstimatedReturns: boolean;
  showStakeAndLines: boolean;
  poolType: string;
  leg: IBetHistoryLeg[];
  outcome: string[];
  market: string[];
  event: string[];
  events: { [key: string]: ISportEvent };
  markets: { [key: string]: IMarket };
  outcomes: { [key: string]: IOutcome };

  constructor(public bet: IBetHistoryPoolBet,
              public betHistoryMainService: BetHistoryMainService,
              public userService: UserService,
              public locale: LocaleService,
              public timeService: TimeService,
              public cashOutMapIndex: CashoutMapIndexService,
              public currencyPipe: CurrencyPipe,
  ) {
    this.date = this.bet.date;
    this.id = this.bet.id;
    this.status = betHistoryMainService.getBetStatus(bet);
    this.currency = this.userService.currencySymbol;
    this.lines = +this.bet.numLines;
    this.receipt = this.bet.receipt;
    this.stake = ((this.bet.stake as IBetHistoryStake).value - ((this.bet.stake as IBetHistoryStake).tokenValue || 0)).toFixed(2);
    this.totalStake = this.addCurrency((this.bet.stake as IBetHistoryStake).poolStake, this.currency) as string;
    this.tokenValue = (this.bet.stake as IBetHistoryStake).tokenValue;
    this.winLines = this.bet.numLinesWin;
    this.numLegs = +this.bet.numLegs;
    this.isSettled = this.bet.settled === 'Y';
    this.totalReturns = this._getTotalReturns();
    this.showLegsNumberInTitle = false;
    this.showEstimatedReturns = true;
    this.showStakeAndLines = false;
    this.poolType = this.bet.poolType;
    this.leg = this.bet.poolLeg;
    this.event = [];
    this.outcome = [];
    this.market = [];
    this.events = {};
    this.markets = {};
    this.outcomes = {};

    this._renameProperties();
  }

  /**
   * Check if bet is suspended
   */
  get isSuspended(): boolean {
    return _.some(this.leg, (leg: IBetHistoryLeg) => leg.status === 'suspended');
  }
  set isSuspended(value:boolean) {}
  /**
   * Returns value depends on bet status
   * @param bet
   * @return {string}
   * @private
   */
  _getTotalReturns(): string {
    let totalReturns = null;

    if (this.isSettled) {
      totalReturns = this.status === 'void' ? this.bet.refund.value : this.bet.winnings.value;
    }

    return totalReturns ? this.addCurrency(totalReturns, this.currency) : totalReturns;
  }

  /**
   * Rename properties to mach regular bets and to be used for Live Updates
   * @private
   */
  _renameProperties(): void {
    _.forEach(this.leg, (leg: IBetHistoryLeg) => {
      leg.part = leg.poolPart;
      leg.startTime = this._normalizeDate(leg.startTime);
    });
  }

  /**
   * Rename properties to mach regular bets class and to be used for Live Updates
   * @private
   */
  _fillIdsProperties(): void {
    _.forEach(this.leg, (leg: IBetHistoryLeg) => {
      _.forEach(leg.part, (part: IBetHistoryPart) => {
        const outcome = part.outcome;

        part.eventId = leg.eventId = outcome.event.id.toString();
        part.toteEventId = leg.toteEventId = outcome.event.toteEventId && outcome.event.toteEventId.toString();
        part.marketId = leg.marketId = outcome.market.id;
        part.outcomeId = outcome.id;

        if (!_.contains(this.outcome, part.outcomeId)) {
          this.outcome.push(part.outcomeId);
        }

        if (!_.contains(this.event, part.eventId)) {
          this.event.push(part.eventId);
        }

        if (!_.contains(this.market, part.marketId)) {
          this.market.push(part.marketId);
        }
      });
    });
  }

  /**
   * Format date string to have correct TZD sign
   * @param  {String} dateString [String date - expected to be "2018-03-12 13:39:20",
   *                              without TZD signs]
   * @return {String}            [Correct date string with TZD signs]
   */
  _normalizeDate(dateString: string): string {
    return dateString.replace(' ', 'T');
  }

  /**
   * Update cashOutMapIndex service to be used for Live Updates
   * @param {Array} poolLegs - array of pool legs
   * @private
   */
  _updateCashoutMapIndex(poolLegs: IBetHistoryLeg[]): void {
    _.forEach(poolLegs, poolLeg => {
      const eventId = poolLeg.poolPart[0].outcome.event.id,
        marketId = poolLeg.poolPart[0].outcome.market.id;

      _.forEach(poolLeg.poolPart, poolPart => {
        const outcomeId = poolPart.outcome.id;
        this.cashOutMapIndex.create('outcome', outcomeId, this.id, this.isSettled);
      });
      this.cashOutMapIndex.create('event', eventId, this.id, this.isSettled);
      this.cashOutMapIndex.create('market', marketId, this.id, this.isSettled);
    });
  }

  private addCurrency(value: number | string, currencySymbol: string): string | number {
    return +value || +value === 0  ? this.currencyPipe.transform(value, currencySymbol, 'code') : value;
  }
}
