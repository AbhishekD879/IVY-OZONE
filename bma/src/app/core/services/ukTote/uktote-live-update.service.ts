import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IUkToteLiveUpdateModel, IUkToteAllChannelsModel } from './uktote-update.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Injectable()
export class UkToteLiveUpdatesService {
  private channelName;
  constructor(private channelService: ChannelService,
              private command: CommandService) {
    this.channelName = {
      event: 'sEVENT',
      market: 'sEVMKT',
      selection: 'sSELCN'
    };

    this.command.register(command.API.UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE, (
      event: ISportEvent,
      liveUpdate: IUkToteLiveUpdateModel
    ) => {
      this.updateEventWithLiveUpdate(event, liveUpdate);
      return Promise.resolve();
    });
  }


  /**
   * Updated event status with received live update
   * @param {Object} event - event object
   * @param {Object} liveUpdate - received live update
   */
  updateEventStatus(event: ISportEvent, liveUpdate: IUkToteLiveUpdateModel): void {
    const { payload } = liveUpdate;
    event.eventStatusCode = payload.status;
  }

  /**
   * Updated market status with received live update
   * @param {Object} event - event object
   * @param {Object} liveUpdate - received live update
   */
  updateMarketStatus(event: ISportEvent, liveUpdate: IUkToteLiveUpdateModel): void {
    const { id, payload } = liveUpdate,
      marketToUpdate = _.find(event.markets, (market: IMarket) => +market.linkedMarketId === id);

    marketToUpdate.marketStatusCode = payload.status;
  }

  /**
   * Updated outcome status with received live update
   * @param {Object} event - event object
   * @param {Object} liveUpdate - received live update
   */
  updateOutcomeStatus(event: ISportEvent, liveUpdate: IUkToteLiveUpdateModel): void {
    const { id, payload } = liveUpdate,
      marketId = payload.ev_mkt_id,
      marketToUpdate = _.find(event.markets, (market: IMarket) => +market.linkedMarketId === +marketId);

    if (!marketToUpdate) {
      return;
    }

    const outcomeToUpdate = _.find(marketToUpdate.outcomes,
      (outcome: IOutcome) => +outcome.linkedOutcomeId === +id);
    if (!outcomeToUpdate) {
      return;
    }
    outcomeToUpdate.outcomeStatusCode = payload.status;
  }

  /**
   * Updated event with received live update
   * @param {Object} event - event object
   * @param {Object} liveUpdate - received live update
   */
  updateEventWithLiveUpdate(event: ISportEvent, liveUpdate: IUkToteLiveUpdateModel) {
    const { type } = liveUpdate;
    switch (type) {
      case this.channelName.event: {
        this.updateEventStatus(event, liveUpdate);
        break;
      }
      case this.channelName.market: {
        this.updateMarketStatus(event, liveUpdate);
        break;
      }
      case this.channelName.selection: {
        this.updateOutcomeStatus(event, liveUpdate);
        break;
      }
      default: {
        return;
      }
    }
  }


  /**
   * Get all channels for provided ids of events, markets and outcomes
   * @param {IUkToteAllChannelsModel} channelsIds - object which contains ids of events, markets and outcomes
   * @returns {string[]} - array of channels for provided ids
   */
  getAllChannels(channelsIds: IUkToteAllChannelsModel): string[] {
    let channels = [];
    if (channelsIds.event && channelsIds.event.length) {
      channels = channels.concat(this.getEventChannels(channelsIds.event));
    }

    if (channelsIds.market && channelsIds.market.length) {
      channels = channels.concat(this.getMarketChannels(channelsIds.market));
    }

    if (channelsIds.outcome && channelsIds.outcome.length) {
      channels = channels.concat(this.getOutcomeChannels(channelsIds.outcome));
    }
    return channels;
  }

  /**
   * Returns channels for subscription
   * @param {number[] | string[]} arrayIds
   * @param {string[]} type
   * @returns {string[]}
   */
  private getChannels(arrayIds: number[] | string[], type: string): string[] {
    return _.map(arrayIds, (id: number | string) => this.channelService.formChannel(type, id));
  }

  /**
   * Get event channels ids
   * @param {Array} eventIdsArray
   * @returns {string[]}
   */
  private getEventChannels(eventIdsArray: number[]): string[] {
    return this.getChannels(eventIdsArray, this.channelName.event);
  }

  /**
   * Get market channels ids
   * @param {Array} marketIdsArray
   * @returns {string[]}
   */
  private getMarketChannels(marketIdsArray: string[]): string[] {
    return this.getChannels(marketIdsArray, this.channelName.market);
  }

  /**
   * Get outcome channels ids
   * @param {Array} outcomeIdsArray
   * @returns {string[]}
   */
  private getOutcomeChannels(outcomeIdsArray: string[]): string[] {
    return this.getChannels(outcomeIdsArray, this.channelName.selection);
  }
}
