import * as _ from 'underscore';

import PoolBetBase from '../poolBetBase/pool-bet-base.class';
import { TimeService } from 'app/core/services/time/time.service';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from 'app/core/services/locale/locale.service';
import { BetHistoryMainService } from '../../services/betHistoryMain/bet-history-main.service';
import { CashoutMapIndexService } from '../../services/cashOutMapIndex/cashout-map-index.service';
import { IPoolBetDetailLegPart } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { IOutcomeResult } from 'app/core/models/outcome.model';
import { IBetHistoryLeg, IFootballJackpotBet } from '../../models/bet-history.model';
import { CurrencyPipe } from '@angular/common';

export default class FootballJackpotBet extends PoolBetBase {
  legs: any[];
  isFootballJackpotBetModel: boolean;
  betTitle: string;
  showLegsNumberInTitle: boolean;
  showEstimatedReturns: boolean;
  showStakeAndLines: boolean;

  constructor(
     bet: IFootballJackpotBet,
     betHistoryMainService: BetHistoryMainService,
     userService: UserService,
     locale: LocaleService,
     timeService: TimeService,
     cashOutMapIndex: CashoutMapIndexService,
     currencyPipe: CurrencyPipe,
  ) {
    super(
      bet,
      betHistoryMainService,
      userService,
      locale,
      timeService,
      cashOutMapIndex,
      currencyPipe
  );

    const legArr = bet.leg || bet.poolLeg;
    this.isFootballJackpotBetModel = true;
    this.betTitle = locale.getString('bethistory.footballJackpot');
    this.showLegsNumberInTitle = true;
    this.legs = [];
    this.showEstimatedReturns = false;
    this.showStakeAndLines = true;

    _.each(legArr, (leg: IBetHistoryLeg): void => {
      const legPart = leg.part || leg.poolPart;
      _.each(legPart, (part: IPoolBetDetailLegPart) => {
        const legObj = {
          name: leg.name,
          type: this.setSelection(part.outcome.name),
          adjustedResult: this.getAdjustedResult(part.outcome.name, leg.name),
          startTime: leg.startTime,
          isResulted: this._isResulted(part.outcome.result),
          outcomeResult: part.outcome.outcomeResult,
          outcomeClass: this._getOutcomeClass(part.outcome.outcomeResult),
          isVoid: part.outcome.outcomeResult === 'V'
        };
        this.legs.push(legObj);
      });
    });
  }
  /**
   * Outcome class depending on leg status(Won, Lost), used to show x-mark or check mark
   * @returns {boolean}
   */
  _getOutcomeClass(outcomeResult: string): string {
    return {
      W: 'check-mark',
      L: 'x-mark'
    }[outcomeResult];
  }

  /**
   * resulted flag
   * @returns {boolean}
   */
  _isResulted(result: IOutcomeResult): boolean {
    return result.confirmed && result.confirmed === 'Y';
  }

  /**
   * Check if outcome is Home Draw or Away and set appropriate name for it
   * Home: home team name will be used
   * Draw: 'Draw'
   * Away: away team name will be used
   * @returns {boolean}
   */
  getAdjustedResult(outcomeName: string, legName: string) {
    const type = this.setSelection(outcomeName),
      result = {
        H: this._getTeamName(legName, type),
        D: `Draw`,
        A: this._getTeamName(legName, type)
      }[type];
    return result;
  }

  _getTeamName(legName: string, type: string): string {
    const teamNames = legName.split(' v ');
    return type === 'H' ? teamNames[0] : teamNames[1];
  }

  setSelection(val: string): string {
    return {
      1: 'H',
      2: 'D',
      3: 'A'
    }[val];
  }
}
