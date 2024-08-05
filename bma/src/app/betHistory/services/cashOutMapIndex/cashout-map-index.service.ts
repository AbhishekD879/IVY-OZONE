import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { ICashoutMapItem } from '../../models/cashout-map-item.model';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutMapIndexService {
  outcome: { [key: string]: ICashoutMapItem[]} = {};
  market: { [key: string]: ICashoutMapItem[]} = {};
  event: { [key: string]: ICashoutMapItem[]} = {};

  /**
   * Create an object for quick search on cashout map object.
   * @param type {String}
   * @param id {String}
   * @param cashOutBetId {String}
   */
  create(type: string, id: string | number, cashOutBetId: string | number, isSettled: boolean = false): void {
    this.initCreate(this, type, id);

    if (!_.find(this[type][id], (x: ICashoutMapItem) => x.id === cashOutBetId)) {
      this[type][id].push({
        id: cashOutBetId,
        isSettled
      });
    }
  }

  /**
   * Delete item from cashoutout index object
   * @param outcomeIds {Array}
   * @param marketIds {Array}
   * @param eventIds {Object}
   * @param eventIds {String}
   */
  deleteItem(outcomeIds: string[], marketIds: string[], eventIds: string[], cashoutId: string): void {
    if (eventIds.length !== 0) {
      this.deleteItemByType(this, 'event', cashoutId, eventIds);
    }

    if (marketIds.length !== 0) {
      this.deleteItemByType(this, 'market', cashoutId, marketIds);
    }

    if (outcomeIds.length !== 0) {
      this.deleteItemByType(this, 'outcome', cashoutId, outcomeIds);
    }
  }

  reset() {
    this.outcome = {};
    this.market = {};
    this.event = {};
  }

  /**
   * Retrieves all ids of cashout bets in a map by type
   * @param type {String}
   * @param onlyActive {Boolean} Identifies whether need to process only settled bets
   */
  getItems(type: string, onlyActive: boolean = false): any {
    if (!onlyActive) {
      return _.keys(this[type]);
    }
    return _.chain((this[type] as { [key: string]: ICashoutMapItem[]}))
      .pairs()
      .reject((items: ICashoutMapItem[][]) => !!_.find(items[1], (item: ICashoutMapItem) => item.isSettled))
      .map(_.first)
      .value();
  }

  /**
   * Create array for type
   *
   * @param index {object}
   * @param type {string}
   * @param id {string}
   */
  initCreate(index: object, type: string, id: string | number): void {
    if (!index[type][id]) {
      index[type][id] = [];
    }
  }

  /**
   * Delete item by type
   *
   * @param index {object}
   * @param type {string}
   * @param cashoutId {string}
   * @param arr {arr}
   */
  deleteItemByType(index: object, type: string, cashoutId: string, arr: string[]): void {
    _.each(arr, (id: string) => {
      index[type][id] = _.filter(index[type][id], (item: ICashoutMapItem) => item.id !== cashoutId);

      if (index[type][id].length === 0) {
        delete index[type][id];
      }
    });
  }

}
