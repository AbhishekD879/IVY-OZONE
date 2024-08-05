import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Injectable()
export class ChannelService {
  /**
   * Forms channel. A channel name has two parts - 'sSELCN' + ten digit.(subscribe for outcome only)
   *
   * @return {string}
   * @param type
   * @param itemId
   */
  formChannel(type: string, itemId: number | string): string {
    let id = _.isNumber(itemId) ? itemId.toString() : itemId;
    while ((id.length) < 10) {
      id = `0${id}`;
    }
    return type + id;
  }

  /**
   * Return Push LiveServe channels from array
   * @param entities
   * @param withChildrenChannels
   */
  getLSChannelsFromArray<T extends ISportEvent | IMarket | IOutcome>(
    entities: Array<T>, withChildrenChannels: boolean = true, subscribeForScores: boolean = false
  ): string[] {
    if (!Array.isArray(entities)) {
      return [];
    }
    return entities.reduce((acc: string[], entity: T) => acc.concat(
      this.getLSChannels(entity, withChildrenChannels, subscribeForScores)
    ), []);
  }

  /**
   * Return Push LiveServe channels
   * @param entities
   * @param withChildrenChannels
   */
  getLSChannels(entity: ISportEvent | IMarket | IOutcome,
                withChildrenChannels: boolean = true,
                subscribeForScores: boolean = false): string[] {
    const channels: string[] = [];

    if (entity) {
      if (typeof entity.liveServChannels === 'string') {
        channels.push(entity.liveServChannels.replace(',', ''));
      }
      if (withChildrenChannels && typeof entity.liveServChildrenChannels === 'string') {
        channels.push(entity.liveServChildrenChannels.replace(',', ''));
      }
      if (subscribeForScores && entity.id) {
        channels.push(this.formChannel('sSCBRD', entity.id));
      }
    }

    return channels;
  }

  /**
   * Return Push LiveServe channels for sEVENT and for all markets channels sEVMKT SEVMKT
   * @param events
   */
  getLSChannelsForCoupons(events: ISportEvent[]) {
    return events.reduce((eArr: string[], e: ISportEvent) => eArr.concat(
      this.getLSChannels(e, false),
      this.getLSChannelsFromArray(e.markets)
    ), []);
  }

  /**
   * Collects sEVENT, sEVMKT, sSELCN ids of given events.
   * @param {ISportEvent[]} events
   * @return {Array}
   */
  getEventsChildsLiveChannels(events: ISportEvent[]): Array<string> {
    const channels = [];

    _.each(events, (eventEntity: ISportEvent) => {
      const markets = eventEntity ? eventEntity.markets : [];

      channels.push(...this.getLSChannels(eventEntity, false));

      _.each(markets, (market: IMarket) => {
        const outcomes = market ? market.outcomes : [];

        channels.push(...this.getLSChannels(market, false));

        _.each(outcomes, (outcome: IOutcome) => {
          channels.push(...this.getLSChannels(outcome, false));
        });
      });
    });

    return _.compact(channels);
  }
}
