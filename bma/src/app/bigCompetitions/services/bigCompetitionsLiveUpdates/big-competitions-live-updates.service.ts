import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';
import { Observable } from 'rxjs';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IBCLiveUpdates, IUpdatedObject } from './big-cimpetitions-live-updates.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable()
export class BigCompetitionsLiveUpdatesService {

  constructor(
    private pubSubService: PubSubService,
    private liveServService: LiveServConnectionService
  ) {
    this.liveServeUpdateHandler = this.liveServeUpdateHandler.bind(this);
  }

  /**
   * Performs reconnect of LiveServe connection.
   * @return {Observable}
   */
  reconnect(): Observable<ISocketIO> {
    return this.liveServService.connect();
  }

  /**
   * Subscribes for live updates.
   * @param {Object} events
   */
  subscribe(events: ISportEvent[]): void {
    this.liveServService.connect().subscribe(() => {
      this.liveServService.subscribe(this.getIds(events), this.liveServeUpdateHandler);
    });
  }

  /**
   * Unsubscribes from LiveServe updates.
   * @param {Object} events
   */
  unsubscribe(events: ISportEvent[]): void {
    this.liveServService.unsubscribe(this.getIds(events), this.liveServeUpdateHandler);
  }

  /**
   * Remove event from events list when live update received from LS MS; unsubscribe from LS updates
   * @param {Array} events - events list where all undisplayed events(or markets/outcomes) should be removed
   */
  removeEventEntity(events: ISportEvent[]): void {
    _.each(events, (event: ISportEvent, i: number) => {
      if (event) {
        if (this.isUndisplayed(event) || !event.markets.length) {
          this.deleteAndUnsubscribe(events, i);
        } else {
          const market = _.first(event.markets),
            outcomes = market && market.outcomes;

          if (this.isUndisplayed(market) || this.isAllOutcomesUndisplayed(outcomes)) {
            this.deleteAndUnsubscribe(events, i);
          }
        }
      }
    });
  }

  /**
   * Check if event undisplayed
   * @param {Object} entity - event/market
   * @returns {*|boolean}
   * @private
   */
  private isUndisplayed(entity): boolean {
    return _.isBoolean(entity.isDisplayed) && !entity.isDisplayed;
  }

  /**
   * Delete event from list by index; unsubcribe from LP updates
   * @param {Array} events
   * @param {number} index
   * @private
   */
  private deleteAndUnsubscribe(events: ISportEvent[], index: number): void {
    this.unsubscribe([events[index]]);
    events.splice(index, 1);
  }

  /**
   * Check if all outcomes undisplayed in market
   * @param {Array} outcomes
   * @returns {*|boolean}
   * @private
   */
  private isAllOutcomesUndisplayed(outcomes: IOutcome[]): boolean {
    return _.every(outcomes, this.isUndisplayed);
  }

  /**
   * Parses outcome, event, market ids.
   * @param {Object} events
   * @returns {Array}
   * @private
   */
  private getIds(events: ISportEvent[]): string[] {
    const ids: string[] = [];

    _.each(_.compact(events), (event: ISportEvent) => {
      ids.push(event.liveServChannels.slice(0, -1));
      _.each(event.markets, (market: IMarket) => {
        ids.push(market.liveServChannels.slice(0, -1));
        _.each(market.outcomes, (outcome: IOutcome) => {
          ids.push(outcome.liveServChannels.slice(0, -1));
        });
      });
    });

    return ids;
  }

  /**
   * Handler for live serve updates
   * @param {Object} update
   * @private
   */
  private liveServeUpdateHandler(update: IBCLiveUpdates): void {
    if (update.type === 'MESSAGE') {
      const payload: string = update.message;
      const channel: string = update.channel.name;
      const updatedObject: IUpdatedObject = {
          channel,
          channel_number: update.event.id,
          payload,
          subject_number: update.channel.id,
          subject_type: update.subChannel.type
        };

      this.pubSubService.publish(this.pubSubService.API.LIVE_SERVE_MS_UPDATE, updatedObject);
    }
  }
}
