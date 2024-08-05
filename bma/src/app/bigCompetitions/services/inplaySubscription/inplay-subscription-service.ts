import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Injectable()
export class InplaySubscriptionService {

  constructor(
    private command: CommandService,
    private wsUpdateEventService: WsUpdateEventService
  ) {
    this.wsUpdateEventService.subscribe();
  }

  /**
   * Loads live now or upcoming events from Inplay MS by given category and type IDs.
   * @param {Boolean} isLiveNow
   * @param {number} categoryId
   * @param {number} typeId
   * @param {Boolean} modifyMainMarkets - flag to detect should we modify markets marketMeaningMinorCode
   * and dispSortName in inPlayDataService(see modifyMainMarkets methods comment)
   */
  loadCompetitionEvents(isLiveNow: boolean, categoryId: number, typeId: number, modifyMainMarkets: boolean = true): Promise<ISportEvent[]> {
    const requestParams = {
      categoryId,
      isLiveNowType: isLiveNow,
      topLevelType: isLiveNow ? 'LIVE_EVENT' : 'UPCOMING_EVENT',
      typeId,
      modifyMainMarkets
    };

    return this.command
      .executeAsync(this.command.API.LOAD_COMPETITION_EVENTS, ['competition', requestParams], [])
      .then((events: ISportEvent[]) => {
        return _.filter(events, (event: ISportEvent) => {
          return !!(event.markets && event.markets.length);
        });
      });
  }

  /**
   * Subscribes for live updates from Inplay MS for events by given IDs.
   * @param {Array} eventsIds
   */
  subscribeForLiveUpdates(eventsIds: string[]): void {
    this.command.executeAsync(this.command.API.SUBSCRIBE_FOR_LIVE_UPDATES, [eventsIds]);
  }

  /**
   * Unsubscribes from live updates from Inplay MS for events by given IDs.
   * @param {Array} eventsIds
   */
  unsubscribeForLiveUpdates(eventsIds: string[]): void {
    this.command.executeAsync(this.command.API.UNSUBSCRIBE_FOR_LIVE_UPDATES, [eventsIds]);
  }
}
