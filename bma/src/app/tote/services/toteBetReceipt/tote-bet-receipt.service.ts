import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';

import { IToteEvent } from './../../models/tote-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IPoolBet } from './../../models/pool-bet.model';
import { IBetReceipt } from './../../models/bet-receipt.model';
import { IBetReceiptBuilder, IFailedAndSuccessBets } from './../../models/bet-receipt-builder.model';

@Injectable()
export class ToteBetReceiptService {
  constructor(
    private locale: LocaleService
  ) {}

  /**
   * Build bet receipt for tote
   * @param {object} eventEntity
   * @param {object[]|object} betPlacementRespond
   * @return {object}
   */
  betReceiptBuilder(eventEntity: IToteEvent, betPlacementRespond: IPoolBet[]): IBetReceiptBuilder {
    // betsReceipt variable, extended with all needed data by private functions
    let betsReceipt = [],
      totalStake = 0,
      unsuccessfulBetReceiptMsg,
      successfulBetReceiptMsg;
    const betsData = this.checkAndExcludeFailedBets(betPlacementRespond);
    if (betsData.successBets.length) {
      betsReceipt = this.addBetDetails(betsData.successBets, betsReceipt);
      betsReceipt = this.addLegDetails(betsReceipt, eventEntity);
      totalStake = this.calculateTotalStake(betsReceipt);
      // build unsuccessful msg
      if (betsData.failedBets.length) {
        unsuccessfulBetReceiptMsg = this.addUnsuccessfulMsg(betsReceipt, betsData.failedBets);
      } else {
        successfulBetReceiptMsg = this.getSuccessfulMsg(betsReceipt);
      }
    }
    return {
      successBets: betsReceipt,
      failedBets: betsData.failedBets,
      totalStake,
      unsuccessfulBetReceiptMsg,
      successfulBetReceiptMsg
    };
  }

  /**
   * Extend betsReceipt with legs details
   * @param {object[]} betsReceipt
   * @param {object} eventEntity
   * @return {object} extended betsReceipt
   */
  addLegDetails(betsReceipt: IBetReceipt[], eventEntity: IToteEvent): IBetReceipt[] {
    betsReceipt.forEach(receipt => {
      _.extend(receipt, {
        leg: `${eventEntity.localTime} ${eventEntity.name}`
      });
      this.addSelectionsNames(receipt, eventEntity.markets[0].outcomes);
    });
    return betsReceipt;
  }

  /**
   * Exclude failed bets from response, and divide into failed and success bets
   * @params {object[]} bets
   * @return {object}
   */
  checkAndExcludeFailedBets(bets: IPoolBet[]): IFailedAndSuccessBets {
    const failedBets = [],
      successBets = [];
    // in case if returned data is Array - Win bets
    if (bets.constructor === Array) {
      bets.forEach(bet => {
        if (_.has(bet, 'betError')) {
          return failedBets.push(bet);
        }
        return successBets.push(bet);
      });
      return { failedBets, successBets };
    }
    // in case if returned data is Object - Execta, Trifecta bets
    if (_.has(bets, 'betError') || _.has(bets, 'error')) {
      failedBets.push(bets);
    } else {
      successBets.push(bets);
    }
    return { failedBets, successBets };
  }

  /**
   * Extend betsReceipt with names of the selections
   * @param {object[]} outcomes
   * @param {object[]} betsReceipt
   */
  addSelectionsNames(betsReceipt: IBetReceipt, outcomes: IOutcome[]): void {
    betsReceipt.legParts.forEach((part, index) => {
      outcomes.forEach(outcome => {
        if (outcome.id === part.outcomeRef.id) {
          _.extend(part, {
            outcomeName: betsReceipt.legParts.length > 1 ? `(${index + 1}) ${outcome.name}` : outcome.name
          });
        }
      });
    });
  }

  /**
   * Extend betsReceipt with bet details
   * @param {object[]} bets
   * @param {object[]} betsReceipt
   */
  addBetDetails(bets: IPoolBet[], betsReceipt: IBetReceipt[]): IBetReceipt[] {
    // Handled the structure of bets from win & place bets and Execta & Trifecta bets
    bets.forEach((bet: IPoolBet) => {
      if (bet.hasOwnProperty('bet')) {
        betsReceipt.push(this.buildBetReceipt(bet));
      } else {
        const betSlips = Object.entries(bet);
        betSlips.forEach((betSlip: object) => {
          if(betSlip[1].constructor === Object) {
            betsReceipt.push(this.buildBetReceipt(betSlip[1]));
          }
        });
      }
    });
    return betsReceipt;
  }

  /**
   * @param {string} poolName
   * @returns {string}
   */
  generatePoolTitle(poolName: string): string {
    return `Tote ${this.locale.getString(`tt.${poolName}`)}`;
  }

  /**
   * @return {number} totalStake
   * @param {object[]} betsReceipt
   */
  calculateTotalStake(betsReceipt: IBetReceipt[]): number {
    let total = 0;
    betsReceipt.forEach(bet => {
      total += Number(bet.stakeAmount);
    });
    return total;
  }

  /**
   * Create msg used if failed and successful bets are present
   * @param {object[]} successBets
   * @param {object[]} failedBets
   * return {string}
   */
  addUnsuccessfulMsg(successBets: IPoolBet[], failedBets: IPoolBet[]): string {
    return this.locale.getString('tt.unsuccessfulBetReceiptMsg', [successBets.length, successBets.length + failedBets.length]);
  }
  /**
   * Create msg used if one or more successful bets are present
   * @param {object[]} successBets
   * return {string}
   */
  getSuccessfulMsg(successBets: IPoolBet[]): string {
    return successBets.length > 1 ? this.locale.getString('tt.successBetsReceiptMsg') : this.locale.getString('tt.successBetReceiptMsg');
  }
  /**
   * @param {object} bet
   * return {object}
   * @private
   */
  private buildBetReceipt(bet: IPoolBet): IBetReceipt {
    return {
      poolTitle: this.generatePoolTitle(bet.bet[0].betTypeRef.id),
      outcomeId: bet.bet[0].leg[0].poolLeg.legPart[0].outcomeRef.id,
      stakeAmount: `${bet.betslip.stake.amount}`,
      currency: bet.betslip.stake.currencyRef.id,
      betId: bet.bet[0].receipt,
      legParts: bet.bet[0].leg[0].poolLeg.legPart
    };
  }
}

