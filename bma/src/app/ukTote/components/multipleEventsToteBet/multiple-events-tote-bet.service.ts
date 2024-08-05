import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';

import { ToteBetLeg } from '@uktote/models/toteBetLeg/tote-bet-leg';
import { IUkToteLiveUpdateModel } from '@core/services/ukTote/uktote-update.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import {
  IRacingPostHRResponse, IRacingPostHorse
} from '@coreModule/services/racing/racingPost/racing-post.model';
import { HORSERACING_MAPPING_CONFIG } from '@core/services/racing/racingPost/racing-post-mapping-config.constant';

@Injectable({
  providedIn: 'root'
})
export class MultipleEventsToteBetService {
  constructor(
    private ukToteLiveUpdatesService: UkToteLiveUpdatesService,
    private pubSubService: PubSubService,
    private racingPostService: RacingPostService
  ) {}

  /**
   * Update leg with received live update
   * @param {Array} legsArray - array of legs
   * @param {Object} liveUpdate - received live update
   */
  updateLegEvent(legsArray: ToteBetLeg[], liveUpdate: IUkToteLiveUpdateModel): void {
    const { id } = liveUpdate;
    const legToUpdate = _.find(legsArray, leg => leg.event && leg.event.linkedEventId === id);
    if (!legToUpdate) {
      return;
    }
    this.ukToteLiveUpdatesService.updateEventStatus(legToUpdate.event, liveUpdate);
    this.updateSuspendedStatus(legToUpdate);
  }

  /**
   * Update leg market with received live update
   * @param {Array} legsArray - array of legs
   * @param {Object} liveUpdate - received live update
   */
  updateLegMarket(legsArray: ToteBetLeg[], liveUpdate: IUkToteLiveUpdateModel): void {
    const { payload } = liveUpdate,
      eventId = payload.ev_id,
      legToUpdate = _.find(legsArray, leg => leg.event && leg.event.linkedEventId === eventId);

    this.ukToteLiveUpdatesService.updateMarketStatus(legToUpdate.event, liveUpdate);
    this.updateSuspendedStatus(legToUpdate);
  }

  /**
   * Update leg outcome with received live update
   * @param {Array} legsArray - array of legs
   * @param {Object} liveUpdate - received live update
   */
  updateLegOutcome(legsArray: ToteBetLeg[], liveUpdate: IUkToteLiveUpdateModel): void {
    const { payload } = liveUpdate,
      marketId = payload.ev_mkt_id,
      legToUpdate = _.find(legsArray, leg => +leg.linkedMarketId === marketId);

    if (!legToUpdate) {
      return;
    }
    this.ukToteLiveUpdatesService.updateOutcomeStatus(legToUpdate.event, liveUpdate);
    this.updateSuspendedStatus(legToUpdate);
  }

  /**
   * Change legs array according to received live update
   * @param {Array} legsArray - array of legs
   * @param {Object} liveUpdate - received live update
   */
  changeLegsWithLiveUpdate(legsArray: ToteBetLeg[], liveUpdate: IUkToteLiveUpdateModel): void {
    const { type } = liveUpdate;
    switch (type) {
      case UK_TOTE_CONFIG.channelName.event: {
        this.updateLegEvent(legsArray, liveUpdate);
        break;
      }
      case UK_TOTE_CONFIG.channelName.market: {
        this.updateLegMarket(legsArray, liveUpdate);
        break;
      }
      case UK_TOTE_CONFIG.channelName.selection: {
        this.updateLegOutcome(legsArray, liveUpdate);
        break;
      }
      default: {
        return;
      }
    }
  }

  setRacingForm(eventsData: ISportEvent[]): Observable<ISportEvent[]> {
    const linkedEventIds = eventsData.filter((e: ISportEvent) => e.linkedEventId)
      .map((e: ISportEvent) => e.linkedEventId).join(',');

    if (!linkedEventIds) {
      return of(eventsData);
    }

    return this.racingPostService.getHorseRacingPostById(linkedEventIds).pipe(
      map((raceData: IRacingPostHRResponse) => {
        if (raceData.Error || !raceData.document) {
          return eventsData;
        }

        eventsData.forEach((event: ISportEvent) => {
          const eventRaceData = raceData.document[event.linkedEventId];
          if (!eventRaceData) {
            return;
          }
          const runners = eventRaceData.horses;

          const runnersMap = runners.reduce((obj: {[key: string]: IRacingPostHorse}, runner: IRacingPostHorse) => {
            obj[runner.saddle] = runner;
            return obj;
          }, {});

          event.markets.forEach((market: IMarket) => {
            market.outcomes.forEach((outcome: IOutcome) => {
              if (/^unnamed (2nd )?favourite$/i.test(outcome.name)) {
                return;
              }
              this.racingPostService.addRacingFormOutcome(
                outcome, runnersMap, HORSERACING_MAPPING_CONFIG.outcomeKeysMap
              );
            });
          });
        });
        return eventsData;
      })
    );
  }

  /**
   * Update suspended status of event
   * @param legToUpdate {ToteBetLeg} - ToteBetLeg class member, leg to update suspended status of
   * @private
   */
  private updateSuspendedStatus(legToUpdate: ToteBetLeg): void {
    legToUpdate.updateSuspendedStatus();
    this.pubSubService.publish(this.pubSubService.API.UK_TOTE_LEG_UPDATED, legToUpdate);
  }
}

