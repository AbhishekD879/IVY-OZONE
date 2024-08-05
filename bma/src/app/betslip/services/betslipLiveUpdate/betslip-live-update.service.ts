import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import * as _ from 'underscore';

import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Bet } from '@betslip/services/bet/bet';
import { IBetInfo } from '@betslip/services/bet/bet.model';
import { ILeg } from '@betslip/services/models/bet.model';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';
import {
  ILiveUpdateCallback, ILiveUpdatePrice, ILiveUpdateResponse, ILiveUpdateResponseMessage,
} from '@betslip/services/betslipLiveUpdate/betslip-live-update.model';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { Subject } from 'rxjs';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipLiveUpdateService {
  private static CHANNEL_TYPES = {
    sPRICE: 'outcome',
    sMHCAP: 'outcome',
    sSELCN: 'outcome',
    sEVMKT: 'market',
    sEVENT: 'event'
  };
  private callbacks: { [key: string]: ILiveUpdateCallback } = {};
  private connection: ISocketIO = null;
  private priceUpdate: Subject<ILiveUpdateResponseMessage> = new Subject();

  constructor(
    private liveServConnectionService: LiveServConnectionService,
    private pubSubService: PubSubService,
    private betslipService: BetslipService,
    private betslipDataService: BetslipDataService
  ) {
    this.unsubscribe = this.unsubscribe.bind(this);
    this.disconnectHandler = this.disconnectHandler.bind(this);
    this.subscribeForToteBets = this.subscribeForToteBets.bind(this);
    this.pubSubService.subscribe('betslipLiveUpdateService', this.pubSubService.API.BETSLIP_LIVEUPDATE_SUBSCRIBE_FOR_TOTE_BETS,
      this.subscribeForToteBets);
    this.pubSubService.subscribe('betslipLiveUpdateService', this.pubSubService.API.BETSLIP_LIVEUPDATE_UNSUBSCRIBE,
      this.unsubscribe);
  }

  /**
   * Subscribe for live serve updates for TOTE bets
   * @param channels {Array} - fixed odds events/markets/outcomes channels
   * @param updateHandler {Function} - update handler
   */
  subscribeForToteBets(channels: string[], updateHandler: Function): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      const handler = (msg: ILiveUpdateResponseMessage) => {
        if (msg.type === 'MESSAGE' && updateHandler) {
          updateHandler(msg);
        }
      };
      this.liveServConnectionService.subscribe(channels, handler);
      this.updateConnection(connection);
    });
  }

  unsubscribe(channels: string[]): void {
    this.liveServConnectionService.unsubscribe(channels, _.noop);
  }

  /**
   * Subscribe for live serve updates for bet and it's channels
   * @param {Object} betSlipData
   * @return {*}
   */
  subscribe(betSlipData: Bet[]): Bet[] {
    const betslipDataCopy = [...betSlipData];
    const singles = this.getSingles(betSlipData);
    this.clearOutdatedSubs(singles);

    if (!(singles && singles.length)) {
      return betslipDataCopy;
    }

    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      _.each(singles, (sgl: IBetInfo) => {
        const channels = this.getChannels(sgl);
        const handler = (msg: ILiveUpdateResponse) => {
          if (msg.type === 'MESSAGE') {
            this.handleUpdateMsg(msg, sgl);
          }
        };

        if (!this.callbacks[sgl.outcomeId]) {
          this.liveServConnectionService.subscribe(channels, handler);
          this.handleSubscribe(sgl, channels, handler);
        }
      });

      this.updateConnection(connection);
    });

    return betSlipData;
  }

  reInitAfterReconnect(connection: ISocketIO): void {
    const data = _.extend({}, this.callbacks);
    this.clearAllSubs();

    _.each(data, (callback: ILiveUpdateCallback): void => {
      callback &&
        callback.channels &&
          callback.handler &&
            this.liveServConnectionService.subscribe(callback.channels, callback.handler);
    });

    this.callbacks = data;

    this.updateConnection(connection);
    this.pubSubService.unsubscribe('betslipLiveUpdateServiceReinit');
  }

  /**
   * Remove all subscription after failed connection and re-init again
   */
  reconnect(): void {
    this.pubSubService.subscribe(
      'betslipLiveUpdateServiceReinit',
      `liveServe.${EVENTS.SOCKET_CONNECT_SUCCESS}`,
      (connection) => this.reInitAfterReconnect(connection));

    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      this.reInitAfterReconnect(connection);
    });
  }

  /**
   * Remove all callbacks from map
   */
  clearAllSubs(): void {
    if (!_.isEmpty(this.callbacks)) {
      _.each(this.callbacks, (callback: ILiveUpdateCallback): void => {
        callback && this.liveServConnectionService.unsubscribe(callback.channels, callback.handler);
      });

      this.callbacks = {};
    }
  }

  /**
   * returns price update subject
   */
  getPriceUpdate(): Subject<ILiveUpdateResponseMessage> {
    return this.priceUpdate;
  }

  /**
   * checks if price was changed
   * @param msg
   * @param betInfo
   */
  private isPriceChanged(msg: ILiveUpdateResponseMessage, betInfo: IBetInfo): boolean {
    const { price: { priceNum, priceDen } } = betInfo;
    const { message: { lp_num, lp_den } } = msg;
    return !!(priceNum && priceDen) && !(priceNum.toString() === lp_num && priceDen.toString() === lp_den);
  }

  /**
   * Check if connenction is connencted and not dublicated
   * @param {Object} connection
   * @return {boolean}
   * @private
   */
  private isConnectionValid(connection: ISocketIO): boolean {
    return connection && connection.connected && (!this.connection || this.connection.id !== connection.id);
  }

  /**
   * Set disconnect listener only for new or re-established socket connections
   */
  private setDisconnectHandler(): void {
    this.liveServConnectionService.onDisconnect(this.disconnectHandler);
  }

  /**
   * Handle server disconnect and then reestablish connection
   */
  private disconnectHandler(error: string): void {
    if (this.liveServConnectionService.isDisconnected(error)) {
      this.reconnect();
    }
  }

  /**
   *
   * @param {Object} connection - socket connenction to LS MS
   * @private
   */
  private updateConnection(connection: ISocketIO): void {
    if (this.isConnectionValid(connection)) {
      this.connection = connection;
      this.setDisconnectHandler();
    }
  }

  /**
   * Write to map channel to subscribe and their handlers
   * @param {Object} sgl
   * @param {Array<String>} channels
   * @param {Function} handler
   * @private
   */
  private handleSubscribe(sgl: IBetInfo, channels: string[], handler: Function): void {
    if (sgl.outcomeId) {
      this.callbacks[sgl.outcomeId] = { channels, handler };
    }
  }

  /**
   * Remove old subscriptions from map
   * @param {Array} singles
   * @private
   */
  private clearOutdatedSubs(singles: IBetInfo[]): void {
    // if no current selections old subs are outdated and should be removed
    if (!_.isEmpty(this.callbacks) && !singles.length) {
      this.clearAllSubs();
      return;
    }

    const ids = _.keys(this.callbacks);
    const outdatedIds = _.filter(ids, (cbKey: string): boolean => !_.some(singles, (sgl: IBetInfo) => sgl.outcomeId === cbKey));

    _.each(outdatedIds, (id: string): void => {
      const callbackToRemove = this.callbacks[id];
      if (callbackToRemove) {
        this.liveServConnectionService.unsubscribe(callbackToRemove.channels, callbackToRemove.handler);
        this.callbacks[id] = undefined;
      }
    });
  }

  /**
   * Filter bets for single one by outcome Id
   * @param {Object} bets
   * @private
   * @return {Array}
   */
  private getSingles(bets: Bet[]): IBetInfo[] {
    const betSlipData = bets.map((bet: Bet): IBetInfo => <IBetInfo>bet.info());
    return _.filter(betSlipData, (bet: IBetInfo): boolean => !!bet.outcomeId);
  }

  /**
   * Receive LS update and apply for selection in betslip
   * @param {Object} update
   * @private
   */
  private handleUpdateMsg(update: ILiveUpdateResponseMessage, bet: IBetInfo): void {
    const betIndexes = this.getSelectionIndexes(update.channel.id);
    const type = update.subChannel && update.subChannel.type || update.channel.type;
    const updateType = BetslipLiveUpdateService.CHANNEL_TYPES[type];
    const payload = update.message;
    const priceUpdated = updateType === 'outcome' && !payload.raw_hcap && payload.lp_den
      && this.isPriceChanged(update, bet);
    const eachWayFlagUpdated: boolean = updateType === 'market' && this.isEachWayFlagUpdated(update.message.ew_avail, bet);
    _.each(betIndexes, (index: number): void => {
      if (_.isNumber(index)) {
        this.betslipService.updateSelectionLiveUpdateHistory(index, update);
        this.betslipService.updateSelection(index, update.message, updateType);
      }
    });

    if (priceUpdated) {
      this.betslipService.updateLegsWithPriceChange((payload as ILiveUpdatePrice), update.channel.id);
      this.emitPriceUpdate(update);
    }
    if(eachWayFlagUpdated){
        this.pubSubService.publish(this.pubSubService.API.EACHWAY_FLAG_UPDATED,[update.message, bet]);
    }
  }

  /**
   * emits value with update if there are some observers
   * @param update
   */
  private emitPriceUpdate(update: ILiveUpdateResponseMessage): void {
    if (this.priceUpdate.observers.length) {
      this.priceUpdate.next(update);
    }
  }

  /**
   * Get selections indexes by order in bet bets
   * @params {String} channelID
   * @private
   * @return {Array} selection indexes
   */
  private getSelectionIndexes(channelID: number): number[] {
    const betIndexes = [];
    let betInfo: IBetInfo;

    _.each(this.betslipDataService.bets, (bet: Bet, index: number): void => {
      betInfo = <IBetInfo>bet.info();
      _.each(<ILeg[]>betInfo.eventIds, (idArray: ILeg): void => {
        _.each(idArray, (id: string): void => {
          if (Number(id) === Number(channelID) && betInfo.type === 'SGL') {
            betIndexes.push(index);
          }
        });
      });
    });

    return betIndexes;
  }

  /**
   * get liveServChannels
   * @params {Object} betSlipData
   * @private
   * @return {Array} array with liveServChannels id's
   */
  private getChannels(betSlipItem: IBetInfo): string[] {
    const channelIds = [];

    _.each(betSlipItem.liveServChannels, (channelType: any): void => {
      _.each(channelType, (channelId: string): void => {
        channelIds.push(channelId);
      });
    });

    return channelIds;
  }
  /**
   * checks if the isEachWayAvailable flag is upadated or not
   * @param eachWayAvailable - upadte from live serve
   * @param betInfo - bet selection object
   * @returns boolean
   */
  private isEachWayFlagUpdated(eachWayAvailable: string, betInfo: IBetInfo): boolean {
    return !(betInfo && betInfo.Bet && betInfo.Bet.params && betInfo.Bet.params.eachWayAvailable === eachWayAvailable);
  }
}

