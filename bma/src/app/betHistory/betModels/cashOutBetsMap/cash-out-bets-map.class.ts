import * as _ from 'underscore';

import { CashoutBet } from '../cashoutBet/cashout-bet.class';

import { cashoutConstants } from '../../constants/cashout.constant';
import { CashoutErrorMessageService } from '../../services/cashoutErrorMessageService/cashout-error-message.service';
import { BetModelService } from '../../services/betModelService/bet-model.service';

import { IBetHistoryBet } from '../../models/bet-history.model';
import { IBetDetail } from 'app/bpp/services/bppProviders/bpp-providers.model';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { LocaleService } from '@app/core/services/locale/locale.service';

interface IUpdatedMap { [key: string]: CashoutBet; }

export interface IMapState {
  isEmpty: boolean;
  isSpinnerActive: boolean;
  isUserLogOut: boolean;
}

export class CashOutBetsMap {

  readonly cashoutConstants = cashoutConstants;
  userCurrency: string;
  userCurrencySymbol: string;
  mapState: IMapState;
  allSilkNames: string[];

  constructor(private cashOutMapIndex: any,
              private betModelService: BetModelService,
              private cashOutErrorMessage: CashoutErrorMessageService,
              private betHistoryMainService: BetHistoryMainService,
              private locale: LocaleService) {

    this.mapState = {
      isEmpty: true,
      isSpinnerActive: false,
      isUserLogOut: false
    };
  }

  /**
   * Get ids of all bets
   * @returns {Array}
   */
  getAllBetIds(): string[] {
    const betsObj = this;
    return this.getBetsIdArr(betsObj, null);
  }

  /**
   * Get array of bets by some criterias
   * @param {Object}
   * @returns {Array}
   */
  getBetsByCriterias(...args) {
    const betsObj = this;
    let result = [];
    _.each(args, item => {
      result = result.concat(this.getBetsIdArr(betsObj, item));
    });
    return result;
  }

  /**
   * Delete array of bets from map
   * @param idsArr {Array}
   * @param configObj {Object}
   */
  deleteBets(idsArr: string[], configObj): void {
    const that = this;
    _.each(idsArr, item => {
      if (that[item] && ((configObj && _.isMatch(that[item], configObj)) || !configObj)) {
        this.cashOutMapIndex.deleteItem(that[item].outcome, that[item].market, that[item].event, item);
        delete that[item];
      }
    });
  }

  /**
   * Delete completed bets from map
   * @param updatedBets {Array}
   */
  deleteCompletedBets(updatedBets: IUpdatedMap): void {
    const updatedBetIdArr = this.getBetsIdArr(updatedBets, null), // array of id-es all updatedBet objects,
      notInProgressAndNotCashedOut = this.getBetsByCriterias({ inProgress: false, isCashOutedBetSuccess: false }),
      cashedOutOrEventCompleted = _.difference(notInProgressAndNotCashedOut, updatedBetIdArr); // [1,2,3] diff [1,2] = [3]
    this.deleteBets(cashedOutOrEventCompleted, null);
  }

  /**
   * Delete success bets from map
   */
  deleteSuccessBets(): void {
    const cashoutedBetSuccess = this.getBetsByCriterias({ isCashOutedBetSuccess: true });
    this.deleteBets(cashoutedBetSuccess, null);
  }

  /**
   * Extend bets from map.
   * @param oldMap {Object}
   * @param newMap {Object}
   * @param predicateItem {Object}
   */
  extend(oldMap: CashOutBetsMap, newMap: IUpdatedMap, predicateItem): void {
    _.each(newMap, (item, i) => {
      if (oldMap[i] === undefined && predicateItem && this.mapState.isUserLogOut) {
        return;
      }
      if ((predicateItem && predicateItem(oldMap[i])) || !predicateItem) {
        item.isPriceDecrease = false;
        oldMap[i] = item;
      }
    });
  }

  /**
   * Reset cashout map
   * @param options {Object}
   */
  reset(options): void {
    this.deleteBets(this.getAllBetIds(), options);
    this.cashOutMapIndex.reset();

    this.mapState.isEmpty = true;
    this.mapState.isSpinnerActive = false;
  }

  /**
   * Create new cashoutBetsMap object
   *
   * @param betsArr []
   * @param currency {string}
   * @param currencySymbol {string}
   * @param fromWS {boolean} identifies whether bets are received from Cash Out WS
   * @returns {object}
   */
  createUpdatedCashoutBetsMap(betsArr: IBetDetail[] | IBetHistoryBet[], currency: string, currencySymbol: string,
                              fromWS: boolean = true): IUpdatedMap {
    const map = {};

    this.userCurrency = currency;
    this.userCurrencySymbol = currencySymbol;

    _.each(betsArr, (bet: IBetDetail|IBetHistoryBet) => {
      if (fromWS) {
        map[(bet as IBetHistoryBet).id] = new RegularBet(bet as IBetHistoryBet, this.betModelService, currency, currencySymbol,
          this.cashOutMapIndex, this.betHistoryMainService, this.locale, this.cashOutErrorMessage, this.cashoutConstants);
      } else {
        map[bet.betId] = new CashoutBet(bet, this.betModelService, currency, currencySymbol,
          this.cashOutMapIndex, this.cashOutErrorMessage);
      }
    });

    return map;
  }

  /**
   * Get array of bets ids
   * @param betsObj {object}
   * @param configObj {object}
   * @returns []
   */
  getBetsIdArr(betsObj, configObj): string[] {
    const betsData = configObj ? _.filter(betsObj, this.predicate(configObj)) : betsObj;
    return _.compact(_.map(betsData, (item: IBetHistoryBet) => {
      return item && item.betId;
    }));
  }

  /**
   * Predicate
   * @param configObj {object}
   */
  predicate(configObj) {
    return (item) => {
      return _.isMatch(item, configObj);
    };
  }

  /**
   * Is object empty
   * @param obj {object}
   * @returns {boolean}
   */
  isEmptyObj(obj): boolean {
    for (const key in obj) {
      // hasOwnProperty doesn't work in Windows Phone
      if (Number(key)) {
        return false;
      }
    }
    return true;
  }
}
