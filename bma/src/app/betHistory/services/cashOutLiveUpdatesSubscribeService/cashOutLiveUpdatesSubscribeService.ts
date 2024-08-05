import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CashOutLiveServeUpdatesService } from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { HandleLiveServeUpdatesService } from '@core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';

import { cashoutConstants } from '../../constants/cashout.constant';

import { ITypesAndIds, ICashOutCtrl } from '@app/betHistory/models/bet-history-cash-out.model';
import { CashOutBetsMap } from '../../betModels/cashOutBetsMap/cash-out-bets-map.class';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import { CashOutSetDefaultStateService } from '@app/betHistory/services/cashoutSetDefaultStateService/cashout-set-default-state-service';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import TotePotPoolBet from '@app/betHistory/betModels/totePotPoolBetClass/TotePotPoolBetClass';
import TotePoolBet from '@app/betHistory/betModels/totePoolBet/tote-pool-bet.class';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashOutLiveUpdatesSubscribeService {

  private readonly CASH_OUT = cashoutConstants;
  private channels: string[] = [];
  private destroyedCashOutCtrls = [];

  constructor(
    private cashOutMapIndexService: CashoutMapIndexService,
    private cashOutSetDefaultStateService: CashOutSetDefaultStateService,
    private cashOutLiveServeHandleUpdatesService: HandleLiveServeUpdatesService,
    private cashOutLiveServeUpdatesService: CashOutLiveServeUpdatesService,
    private pubSubService: PubSubService,
    private channelService: ChannelService
  ) {
    this.registerCashOutControllerEvent();
  }
  /**
   * Subscribes for LP updates
   * @param map {object}
   */
  addWatch(map: CashOutBetsMap | { [key: string]: (TotePotPoolBet | TotePoolBet | IBetHistoryBet)}): void {
    this.cashOutLiveServeHandleUpdatesService.unsubscribe(this.channels);
    const ids: ITypesAndIds = this.getIds();
    this.channels = [];

    // ToDo: dynamic betId keys added to the CashOutBetsMap instance cause a big mess with typing.
    Object.assign(this.cashOutLiveServeUpdatesService.betsMap, map);

    if (ids.outcome.length) {
      this.cashOutSetDefaultStateService.extendMapWithEvents(ids.outcome, map as any)
        .subscribe(() => {
          this.extendChannelsAndSubscribe(ids);
          this.pubSubService.publish(this.pubSubService.API.BET_EVENTENTITY_UPDATED);
        }, () => {});
    }
  }

  /**
   * Subscribes for LP updates for non cashOut bets
   * @param data {Object}
   * @param myBetsIds {Object}
   * @returns {Object}
   */
  addWatchForPlacedEventsOnly(data: { [key: string ]: RegularBet }, myBetsIds: ITypesAndIds = null): void {
    const ids: ITypesAndIds = myBetsIds || this.getIds();
    const activeBetsIds: ITypesAndIds = this.getIds(true);
    this.cashOutLiveServeHandleUpdatesService.unsubscribe(this.channels);
    this.channels = [];

    Object.assign(this.cashOutLiveServeUpdatesService.betsMap, data);
    this.cashOutSetDefaultStateService.extendMapWithEvents(ids.outcome, data)
      .subscribe(() => {
        this.extendChannelsAndSubscribe(activeBetsIds);
        this.pubSubService.publish(this.pubSubService.API.BET_EVENTENTITY_UPDATED);
      }, () => {});
  }

  /**
   * Unsubscribe from live updates
   */
  unsubscribeFromLiveUpdates(): void {
    this.cashOutLiveServeHandleUpdatesService.unsubscribe(this.channels);
  }

  /**
   * Subscribes for LP updates for open bets
   * @param data {Object}
   * @param myBetsIds {Object}
   * @returns {Object}
   */
  addWatchForRegularBets(data: { [key: string ]: RegularBet }, myBetsIds: ITypesAndIds = null): void {
    return this.addWatchForPlacedEventsOnly(data, myBetsIds);
  }

  /**
   * Method to track cash out controllers
   * @private
   */
  private registerCashOutControllerEvent(): void {
    this.pubSubService.subscribe('CashOutLiveUpdatesSubscribeService', this.pubSubService.API.CASHOUT_CTRL_STATUS, (data: ICashOutCtrl) => {
      const arr = this.destroyedCashOutCtrls.filter((item: ICashOutCtrl) => item.ctrlName === data.ctrlName);

      if (!arr.length) {
        this.destroyedCashOutCtrls.push(data);
      } else {
        _.each(arr, (item: ICashOutCtrl) => {
          item.isDestroyed = data.isDestroyed;
        });
      }
    });
  }

  /**
   * Extends channels and subscribes to updates from LS
   * @param {ITypesAndIds} ids
   * @private
   */
  private extendChannelsAndSubscribe(ids: ITypesAndIds): void {
    if (ids.event.length) {
      this.channels = this.channels.concat(this.getEventChannels(ids.event));
    }

    if (ids.market.length) {
      this.channels = this.channels.concat(this.getMarketChannels(ids.market));
    }

    if (ids.outcome.length) {
      this.channels = this.channels.concat(this.getOutcomeChannels(ids.outcome));
    }

    this.registerLiveServEvents();
  }

  /**
   * Connects to live serve updates microservice
   * Add handlers
   * Registers event to handle unsubscribe
   * @private
   */
  private registerLiveServEvents(): void {
    this.cashOutLiveServeHandleUpdatesService.subscribe(this.channels,
      this.cashOutLiveServeUpdatesService.updateCashOutValue.bind(this.cashOutLiveServeUpdatesService));

    this.pubSubService.subscribe('cashOutLiveServeUpdatesService', this.pubSubService.API.UNSUBSCRIBE_LS_UPDATES_MS, idsAndTypes => {
      let channelsToUnsubscribe = this.channels,
        resetChannels = false;

      if (idsAndTypes) {
        channelsToUnsubscribe = this.getSpecificChannelsToUnsubscribe(idsAndTypes);
      } else {
        resetChannels = true;
      }

      this.cashOutLiveServeHandleUpdatesService.unsubscribe(channelsToUnsubscribe);

      if (resetChannels) {
        this.channels = [];
      }
    });
  }

  private getSpecificChannelsToUnsubscribe(idsAndTypes: ITypesAndIds): string[] {
    return this.getEventChannels(idsAndTypes.event)
      .concat(this.getMarketChannels(idsAndTypes.market))
      .concat(this.getOutcomeChannels(idsAndTypes.outcome));
  }

  /**
   * Returns channels for subscription
   * @param {string[]} arrayIds
   * @param {string} type
   * @returns {string[]}
   */
  private getChannels(arrayIds: string[], type: string): string[] {
    return _.map(arrayIds, (id: string) => this.channelService.formChannel(type, id));
  }

  /**
   * Get event channels ids
   * @param eventIdsArray []
   */
  private getEventChannels(eventIdsArray: string[]): string[] {
    return this.getChannels(eventIdsArray, this.CASH_OUT.channelName.event)
      .concat(this.getChannels(eventIdsArray, this.CASH_OUT.channelName.score))
      .concat(this.getChannels(eventIdsArray, this.CASH_OUT.channelName.clock));
  }

  /**
   * Get market channels ids
   * @param marketIdsArray []
   */
  private getMarketChannels(marketIdsArray: string[]): string[] {
    return this.getChannels(marketIdsArray, this.CASH_OUT.channelName.market);
  }

  /**
   * Get outcome channels ids
   * @param outcomeIdsArray []
   */
  private getOutcomeChannels(outcomeIdsArray: string[]): string[] {
    return this.getChannels(outcomeIdsArray, this.CASH_OUT.channelName.selection);
  }

  /**
   * Get outcome, event, market ids
   * @returns {ITypesAndIds}
   */
  private getIds(onlyActive: boolean = false): ITypesAndIds {
    return {
      outcome: this.cashOutMapIndexService.getItems(this.CASH_OUT.keyProperties.outcome, onlyActive),
      market: this.cashOutMapIndexService.getItems(this.CASH_OUT.keyProperties.market, onlyActive),
      event: this.cashOutMapIndexService.getItems(this.CASH_OUT.keyProperties.event, onlyActive)
    };
  }
}
