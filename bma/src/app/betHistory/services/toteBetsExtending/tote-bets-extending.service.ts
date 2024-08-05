import {
  combineLatest as observableCombineLatest,
  from as observableFrom,
  of as observableOf,
  Observable
} from 'rxjs';

import { mergeMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { UkToteEventsLinkingService } from '@core/services/ukTote/uktote-events-linking.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IUkToteUpdateFunctionsModel } from '@core/services/ukTote/uktote-update.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import TotePotPoolBet from '../../betModels/totePotPoolBetClass/TotePotPoolBetClass';
import TotePoolBet from '@app/betHistory/betModels/totePoolBet/tote-pool-bet.class';

@Injectable({ providedIn: BetHistoryApiModule })
export class ToteBetsExtendingService {

  /**
   * Get Scoop6 event ids
   * @param {Array} bets - array of bets
   * @returns {Array} - array of Scoop6 event ids
   */
  static getScoop6EventIds(bets: (TotePotPoolBet | TotePoolBet)[]): string[] {
    return _.chain(bets)
      .filter(bet => bet.isScoop6Pool)
      .pluck('leg')
      .flatten()
      .pluck('part')
      .map(_.first)
      .pluck('outcome')
      .pluck('event')
      .pluck('id')
      .uniq()
      .value();
  }

  /**
   * Set linkedEntityId property of mainEntity
   * @param mainEntity - main (TOTE) event, market, outcome
   * @param extendingEntity - extending event, market, outcome
   * @private
   */
  static updateEntityId(mainEntity: ISportEvent | IMarket | IOutcome,
                        extendingEntity: ISportEvent | IMarket | IOutcome): void {
    mainEntity.linkedEntityId = extendingEntity.id;
  }

  /**
   * Get update functions object
   * @returns {{extendEvent: Function, extendMarket: Function, extendOutcome: Function}}
   * @private
   */
  static setLinkedId(linkedEntitiesMap: { [id: string]: string }, entity: ISportEvent | IOutcome | IMarket): void {
    if (!entity.linkedEntityId) {
      return;
    }
    linkedEntitiesMap[entity.id.toString()] = entity.linkedEntityId.toString();
  }
  constructor(private siteServerFactory: SiteServerService,
              private ukToteEventsLinkingService: UkToteEventsLinkingService) {}


  /**
   * Load TOTE events
   * @param {Array} ukToteBets - array of UK TOTE bets
   * @returns {*}
   */
  loadEventsForToteBets(ukToteBets: (TotePotPoolBet | TotePoolBet)[]): Observable<ISportEvent[]> {
    if (!ukToteBets || !ukToteBets.length) {
      return observableOf([]);
    }
    const toteOutcomeIds: string[] = _.chain(ukToteBets)
      .pluck('leg')
      .flatten()
      .pluck('part')
      .flatten()
      .pluck('outcome')
      .pluck('id')
      .uniq()
      .value();
    return observableFrom(this.siteServerFactory.getEventsByOutcomeIds({
      outcomesIds: toteOutcomeIds,
      includeUndisplayed: true,
      externalKeysEvent: true
    }));
  }


  /**
   * Extend TOTE events with fixed odds events
   * @param betsMap - {Object} - map of UK TOTE bets
   */
  extendToteBetsWithEvents(betsMap: { [key: string]: (TotePotPoolBet | TotePoolBet) })
  : Observable<(TotePotPoolBet | TotePoolBet)[]> {
    const toteBets: (TotePotPoolBet | TotePoolBet)[] = _.filter(_.values(betsMap), bet => bet.isToteBet && !bet.fixedEventLinked);
    const scoop6EventIds: string[] = ToteBetsExtendingService.getScoop6EventIds(toteBets);

    return this.loadEventsForToteBets(toteBets).pipe(
      mergeMap((toteEvents: ISportEvent[]) => {
        return this.extendToteEvents(toteEvents, scoop6EventIds);
      }),
      mergeMap((data: Array<ISportEvent[]>) => {
        const extendedToteEvents: ISportEvent[] = data[0].concat(data[1]);
        return this.extendBetsWithFixedEvents(toteBets, extendedToteEvents);
      }));
  }

  /**
   * Get update functions object
   * @returns {{extendEvent: Function, extendMarket: Function, extendOutcome: Function}}
   * @private
   */
  private getUpdateFunctions(): IUkToteUpdateFunctionsModel {
    return {
      extendEvent: ToteBetsExtendingService.updateEntityId.bind(this),
      extendMarket: ToteBetsExtendingService.updateEntityId.bind(this),
      extendOutcome: ToteBetsExtendingService.updateEntityId.bind(this)
    };
  }

  /**
   * Generate map of linked entities
   * @param extendedToteEvents {Array} - array of extended TOTE events
   * @private
   */
  private generateLinkedEntitiesMap(extendedToteEvents: ISportEvent[]): { [id: string]: string } {
    const linkedEntitiesMap: { [id: string]: string } = {};
    _.forEach(extendedToteEvents, (event: ISportEvent) => {
      ToteBetsExtendingService.setLinkedId(linkedEntitiesMap, event);
      _.forEach(event.markets, (market: IMarket) => {
        ToteBetsExtendingService.setLinkedId(linkedEntitiesMap, market);
        _.forEach(market.outcomes, (outcome: IOutcome) => {
          ToteBetsExtendingService.setLinkedId(linkedEntitiesMap, outcome);
        });
      });
    });
    return linkedEntitiesMap;
  }

  /**
   * Extend bet with fixed events info
   * @param ukToteBets {Array} - array of UK TOTE bets
   * @param extendedToteEvents {Array} - array of extended TOTE events
   */
  private extendBetsWithFixedEvents(ukToteBets: (TotePotPoolBet | TotePoolBet)[], extendedToteEvents: ISportEvent[])
  : Observable<(TotePotPoolBet | TotePoolBet)[]> {
    const linkedEntitiesMap = this.generateLinkedEntitiesMap(extendedToteEvents);

    _.forEach(ukToteBets, (ukToteBet: TotePotPoolBet | TotePoolBet) => {
      ukToteBet.extendWithLinkedEvents(linkedEntitiesMap);
      ukToteBet.addLiveUpdatesProperties();
    });

    return observableOf(ukToteBets);
  }

  /**
   * Extend TOTE events with fixed odds events
   * @param {Array} toteEvents - array of TOTE events
   * @param {Array} scoop6EventIds - array of scoop6 event ids
   */
  private extendToteEvents(toteEvents: ISportEvent[], scoop6EventIds: string[]): Observable<Array<ISportEvent[]>> {
    const updateFunctions: IUkToteUpdateFunctionsModel = this.getUpdateFunctions(),
      markToteEvents = (toteEvent: ISportEvent): string => _.contains(scoop6EventIds, toteEvent.id.toString()) ? 'Scoop6' : 'Tote',
      groupedToteEvents: _.Dictionary<ISportEvent[]> = _.groupBy(toteEvents, markToteEvents);
    return observableCombineLatest(
      this.ukToteEventsLinkingService.extendToteEvents(groupedToteEvents.Tote || [], false, updateFunctions),
      this.ukToteEventsLinkingService.extendToteEvents(groupedToteEvents.Scoop6 || [], true, updateFunctions)
    );
  }
}
