import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import {
  IYourcallStorage,
  IYourcallStorageBet,
  IYourcallStorageCustomSelection
} from '@yourcall/models/yourcall-storage.model';
import { YourCallMarket } from '@yourcall/models/markets/yourcall-market';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';


@Injectable({ providedIn: 'root' })
export class YourcallStoredBetsService {
  KEY: string = 'yourCallStoredData';
  v: number = 1;

  private threeHours: number = 3 * 60 * 60 * 1000;
  private isUserLoggedIn: boolean;
  private readonly title = 'yourCallStoredBetsService';
  playerStatID: any;

  constructor(
    private userService: UserService,
    private pubSubService: PubSubService,
    private storageService: StorageService
  ) {
   this.isUserLoggedIn = this.userService.status;

    this.initStorage();

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGIN, () => (this.isUserLoggedIn = true));

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGOUT, () => {
        if (this.isUserLoggedIn) {
          this._clearStoredBets();
        }
      });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.REMOVE_BYB_STORED_EVENT, (eventId: string) => {
      this.removeEvent(eventId, null);
    });
  }

  initStorage(clear: boolean = false): IYourcallStorage {
    const storage: IYourcallStorage = this.storageService.get(this.KEY);

    if (!storage || (storage.v !== this.v) || clear) {
      this.storageService.set(this.KEY, { v: this.v });
    }
    return this.storageService.get(this.KEY);
  }

  /**
   * Returns bets stored in LocalStorage to be able to restore them
   * @returns {*}
   */
  getStoredBets(): IYourcallStorage {
    const allStoredBets = this.initStorage();
    for (const eventId in allStoredBets) {
      if (Object.prototype.hasOwnProperty.call(allStoredBets, eventId)) {
        if (!this.isValidBet(allStoredBets[eventId])) {
          delete allStoredBets[eventId];
        } else {
          this._reValidateBets(allStoredBets, eventId);
        }
      }
    }
    this.storageService.set(this.KEY, allStoredBets);

    return allStoredBets;
  }

  /**
   * Check is bet valid by UAC:
   *  should be not yet started (pre-match only)
   *  should have been modified not later than 3hrs
   *
   * @param bet
   * @returns {boolean}
   * @private
   */
  isValidBet(bet: IYourcallStorageBet): boolean {
    const now = Date.now();

    return !((now - bet.lastModified > this.threeHours) || now > bet.startTime);
  }

  /**
   * Save all selections/bets from particular event and market to LocalStorage
   * @param eventId
   * @param market
   * @param startTime
   * @param edit
   */
  modifyStoredBet(eventId: string, market: YourCallMarket, startTime?: string, edit: boolean = false): void {
    const allStoredBets = this.initStorage();

    if (!allStoredBets[eventId]) {
      allStoredBets[eventId] = { startTime, markets: {} };
    }

    const bet = allStoredBets[eventId];
    bet.lastModified = Date.now();

    if (!bet.markets[market.provider]) {
      bet.markets[market.provider] = {};
    }

    if (!bet.markets[market.provider][market.key]) {
      bet.markets[market.provider][market.key] = { isRestored: false };
    }

    bet.markets[market.provider][market.key].selections = this._collectSelections(market.selected, market.type);

    this.storageService.set(this.KEY, allStoredBets);

    this.reValidateEvent(eventId);
  }

  /**
   * Gather actual selections/bets that should be saved in Local Storage
   * @param selections
   * @param type
   * @returns {*}
   * @private
   */
  _collectSelections(selections: IYourcallSelection | IYourcallSelection[], type?: string): string[] | IYourcallStorageCustomSelection[] {
    if (Array.isArray(selections)) {
      if (type !== 'playerBets') {
        return selections.map(
          (selection: IYourcallSelection) => selection.title);
      } else {
        return selections.map(
          (selection: IYourcallSelection) => ({
            playerName: selection.player,
            statisticTitle: selection.statistic,
            value: selection.value,
            playerStatID:selection.idd
          } as any));
      }
    }

    return selections ? [selections.title] : [];
  }

  /**
   * When customer leaver BUILD YOUR BET tab then remove all empty markets and events if needed
   * @param eventId
   */
  reValidateEvent(eventId: string): void {
    const allStoredBets = this.initStorage();

    if (Object.keys(allStoredBets).length) {
      this._reValidateBets(allStoredBets, eventId);
    }

    this.storageService.set(this.KEY, allStoredBets);
  }

  _reValidateBets(storedBets: IYourcallStorage, eventId: string): void {
    if (!storedBets[eventId] || !storedBets[eventId].markets) {
      return;
    }
    _.each(storedBets[eventId].markets, (stored, provider) => {
      for (const mName in storedBets[eventId].markets[provider]) {
        if (Object.prototype.hasOwnProperty.call(storedBets[eventId].markets[provider], mName) &&
          !storedBets[eventId].markets[provider][mName].selections.length) {
          // remove empty markets
          delete storedBets[eventId].markets[provider][mName];
        }
      }
      if (!_.keys(storedBets[eventId].markets[provider]).length) {
        delete storedBets[eventId].markets[provider];
      }
    });
    if (!Object.keys(storedBets[eventId].markets).length) {
      // remove empty events
      delete storedBets[eventId];
    }
  }

  /**
   * Clears Local Storage with stored bets
   * @private
   */
  _clearStoredBets(): void {
    this.initStorage(true);
  }

  removeEvent(eventId: string, providerId: string): void {
    const allStoredBets = this.initStorage();

    if (providerId) {
      delete allStoredBets[eventId].markets[providerId];
    } else {
      delete allStoredBets[eventId];
    }
    this.storageService.set(this.KEY, allStoredBets);
  }
}
