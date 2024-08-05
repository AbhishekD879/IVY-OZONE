import { from as observableFrom, of as observableOf,  Observable } from 'rxjs';

import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IUkToteUpdateFunctionsModel } from './uktote-update.model';
import { IMarket } from '@core/models/market.model';

@Injectable()
export class UkToteEventsLinkingService {
  constructor(private siteServerService: SiteServerService) {
  }

  /**
   * For tote pool events,
   * request linked fixed odds events,
   * and from them add outcomes info
   * @param {Array} toteEvents
   * @param {boolean} isScoop6Pool
   * @param {Object} updateFunctions - array of TOTE event entities
   * @returns {Observable<ISportEvent[]>}
   */
  extendToteEvents(toteEvents: ISportEvent[],
                   isScoop6Pool: boolean,
                   updateFunctions: IUkToteUpdateFunctionsModel): Observable<ISportEvent[]> {
    return isScoop6Pool ? this.extendScoop6ToteEvents(toteEvents, updateFunctions)
      : this.extendGenericToteEvents(toteEvents, updateFunctions);
  }

  /**
   * Extend tote event info
   * @param {ISportEvent} mainEvent - main event entity
   * @param {Object} extendingEvent - extending event entity
   * @param {Object} updateFunctions - functions for updating outcome, market, events
   */
  extendToteEventInfo(mainEvent: ISportEvent,
                      extendingEvent: ISportEvent,
                      updateFunctions: IUkToteUpdateFunctionsModel): void {
    if (!mainEvent || !extendingEvent) {
      return;
    }

    updateFunctions.extendEvent(mainEvent, extendingEvent);

    if (mainEvent.markets && mainEvent.markets.length && extendingEvent.markets && extendingEvent.markets.length) {
      updateFunctions.extendMarket(this.getPrimaryMarket(mainEvent), this.getPrimaryMarket(extendingEvent));
    }

    const getOutcomesSafe = (event: ISportEvent) => event.markets && event.markets.length && this.getPrimaryMarket(event).outcomes,
      outcomes = getOutcomesSafe(mainEvent),
      extendingOutcomes = getOutcomesSafe(extendingEvent);

    _.each(outcomes, (outcome: IOutcome) => {
      const extendingOutcomeMatch = _.find(extendingOutcomes,
        (extendingOutcome: IOutcome) => this.compareOutcomes(outcome, extendingOutcome));
      if (!extendingOutcomeMatch) {
        return;
      }
      outcome['totePrices'] = extendingOutcomeMatch.prices;
      updateFunctions.extendOutcome(outcome, extendingOutcomeMatch);
    });
  }

  private getPrimaryMarket(event: ISportEvent): IMarket {
    return event.markets ? _.sortBy(event.markets, 'displayOrder')[0] : null;
  }

  /**
   * Load events for events IDs
   * @param {Array} eventIds
   * @returns {Observable<ISportEvent[]>}
   */
  private loadEventsByEventIds(eventIds: number[] | string[]): Observable<ISportEvent[]> {
    if (!eventIds || !eventIds.length) {
      return observableOf([]);
    }
    const eventIdsStr = eventIds.join(',');
    return observableFrom(this.siteServerService.getEvent(eventIdsStr, { racingFormOutcome: true },
      false));
  }

  /**
   * Load events for events IDs of Scoop6 events
   * @param {Array} scoop6EventIds
   * @returns { Observable<ISportEvent[]>}
   */
  private loadEventsByScoop6EventIds(scoop6EventIds: number[], isItv7?): Observable<ISportEvent[]> {
    if (!scoop6EventIds || !scoop6EventIds.length) {
      return observableOf([]);
    }
    const externalEventIdentifiers = _.map(scoop6EventIds, (eventId: string) => {
      if(isItv7) {
        return `~ext-OBEvLinkPlacepot7:event:${eventId}`
      }
      return `~ext-OBEvLinkScoop6:event:${eventId}`;
    }),
      eventIdsStr = externalEventIdentifiers.join(',');
    return  observableFrom(this.siteServerService.getEvent(eventIdsStr,
      { racingFormOutcome: true, externalKeysEvent: true }, false));
  }

  /**
   * Check if outcome from tote event match with outcome from main event
   * @param {Object} outcome
   * @param {Object} extendingOutcome
   * @returns {boolean}
   */
  private compareOutcomes(outcome: IOutcome, extendingOutcome: IOutcome): boolean {
    const getComparator = (outcomeEntity: IOutcome) => outcomeEntity.name.replace(/N\/R$/, '')
      .trim().toLowerCase();
    return getComparator(outcome) === getComparator(extendingOutcome);
  }

  /**
   * For Scoop6 tote pool events,
   * request linked fixed odds events,
   * and from them add outcomes info
   * @param {Object} scoop6Events
   * @param {Object} updateFunctions
   * @returns {Observable<ISportEvent>}
   */
  private extendScoop6ToteEvents(scoop6Events: ISportEvent[],
                                 updateFunctions: IUkToteUpdateFunctionsModel): Observable<ISportEvent[]> {
    const scoop6EventEds = _.map(scoop6Events, (event: ISportEvent) => event.id);
    const itv7 = scoop6Events.some(event => event.typeName && event.typeName.includes("Placepot7"));
    return this.loadEventsByScoop6EventIds(scoop6EventEds, itv7).pipe(
      map((fixedOddsEvents: ISportEvent[]) => {
        _.each(fixedOddsEvents, (fixedOddsEvent: ISportEvent) => {
          let linkedScoop6EventId = fixedOddsEvent.externalKeys && fixedOddsEvent.externalKeys.OBEvLinkScoop6;
          if(itv7) {
            linkedScoop6EventId = fixedOddsEvent.externalKeys && fixedOddsEvent.externalKeys.OBEvLinkPlacepot7;
          }
          const linkedScoop6EventMatch = _.find(scoop6Events,
            (scoop6Event: ISportEvent) => scoop6Event.id === linkedScoop6EventId);

          if (linkedScoop6EventId && linkedScoop6EventMatch) {
            const fixedOddsEventIdMarkets = fixedOddsEvent.markets.filter((market) => market.eventId === fixedOddsEvent.id+'')
            fixedOddsEvent.markets = fixedOddsEventIdMarkets
            this.extendToteEventInfo(linkedScoop6EventMatch, fixedOddsEvent, updateFunctions);
          }
        });
        return scoop6Events;
      }));
  }

  /**
   * For tote pool events,
   * request linked fixed odds events,
   * and from them add outcomes info
   * @param {Array} toteEvents - array of TOTE event entities
   * @param {Array} updateFunctions - functions for updating outcome, market, events
   * @returns {Observable<ISportEvent[]>}
   */
  private extendGenericToteEvents(toteEvents: ISportEvent[],
                                  updateFunctions: IUkToteUpdateFunctionsModel): Observable<ISportEvent[]> {
    const linkedFixedOddsEventsIds = _.compact(
      _.map(toteEvents, (event: ISportEvent) => event.externalKeys && event.externalKeys.OBEvLinkNonTote)
    );

    return this.loadEventsByEventIds(<string[] | number[]>linkedFixedOddsEventsIds).pipe(
      map((fixedOddsEvents: ISportEvent[]) => {
        _.each(toteEvents, ((event: ISportEvent) => {
          const linkedEventId = event.externalKeys && event.externalKeys.OBEvLinkNonTote,
            linkedEventMatch = _.find(fixedOddsEvents, (fixedOddsEvent: ISportEvent) => fixedOddsEvent.id === linkedEventId);

          if (linkedEventId && linkedEventMatch) {
            const matchedEventIdMarkets = linkedEventMatch.markets.filter((market) => market.eventId === linkedEventId+'')
            linkedEventMatch.markets = matchedEventIdMarkets
            this.extendToteEventInfo(event, linkedEventMatch, updateFunctions);
          }
        }));
        return toteEvents;
      }));
  }
}
