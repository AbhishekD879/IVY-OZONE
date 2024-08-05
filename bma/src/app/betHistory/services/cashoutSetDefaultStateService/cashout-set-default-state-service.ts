import { of as observableOf, forkJoin as observableForkJoin,  Observable } from 'rxjs';

import { map, switchMap, mergeMap, finalize } from 'rxjs/operators';
import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { CashoutDataProvider } from '../cashoutDataProvider/cashout-data.provider';
import { CashoutMapIndexService } from '../cashOutMapIndex/cashout-map-index.service';
import { CmsService } from '@core/services/cms/cms.service';
import { cashoutConstants } from '../../constants/cashout.constant';

import { ISportEvent } from '@core/models/sport-event.model';
import { IBetHistoryOutcome, IOutcome } from '@core/models/outcome.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IBetHistoryBet, IBetHistoryLeg, IBetHistoryPart } from '../../models/bet-history.model';
import { IMarket } from '@core/models/market.model';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { PlacedBet } from '@app/betHistory/betModels/placedBet/placed-bet.class';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { ISystemConfig } from '@core/services/cms/models';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';
import { IRacingPostHRResponse } from '@core/services/racing/racingPost/racing-post.model';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class CashOutSetDefaultStateService {
  /**
   * Map for storing cash out bets
   * @type {Object}
   */
  cashoutBetsMap: { [key: string ]: CashoutBet | RegularBet | PlacedBet };

  private readonly CASH_OUT = cashoutConstants;
  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private cashoutDataProvider: CashoutDataProvider,
    private cashOutMapIndex: CashoutMapIndexService,
    private raceOutcomeDetailsService: RaceOutcomeDetailsService,
    private racingPostService: RacingPostService,
    private cmsService: CmsService,
    private betHistoryMainService: BetHistoryMainService
  ) { }

  /**
   * Extends map with SS Events
   * @param outcomeIds []
   * @param data {obj}
   */
  extendMapWithEvents(outcomeIds: string[], data: { [key: string ]: CashoutBet | RegularBet | PlacedBet })
    : Observable<{ [key: string ]: CashoutBet | RegularBet | PlacedBet }> {
    const originalMap = data || this.cashoutBetsMap;
    const eventIds = this.cashOutMapIndex.getItems('event');

    // - check CMS settings
    // * if RacingPost (DF) is enabled for HR
    //   - don't include racingFormOutcome in SiteServer request
    //   - make the SS request, forkJoin it with DF request (with HR event ids)
    //   - merge the racingOutcome data from DF response to SS events
    // * else
    //   - include racingFormOutcome in SS response
    //   - execute the SS request
    // - update the allSilks, legs and the rest
    return this.cmsService.getSystemConfig().pipe(
      map((cmsConfig: ISystemConfig): boolean => cmsConfig && cmsConfig.RacingDataHub && cmsConfig.RacingDataHub.isEnabledForHorseRacing),
      mergeMap((useRacingPost: boolean) => this.getEventsData(outcomeIds, originalMap, useRacingPost)),
      switchMap((eventsData: ISportEvent[]) => this.processEvents(originalMap, eventIds, eventsData)),
      finalize(() => this.processEvents(originalMap, eventIds))
    );
  }

  private getHREventIdsString(betsMap: { [key: string ]: CashoutBet | RegularBet | PlacedBet }): string {
    const hrEventIds = [],
      hrCategoryId = environment.CATEGORIES_DATA.racing.horseracing.id;

    // TODO simplify? via reduce
    Object.keys(betsMap).map(key => betsMap[key]).forEach((bet: CashoutBet | RegularBet | PlacedBet) => {
      const legs = bet && bet.leg || [];
      legs.forEach((leg: IBetHistoryLeg) => {
        const parts = leg.part || [];
        parts.forEach((part: IBetHistoryPart) => {
          // Cashout bets contain only an outcome id string instead of outcomes array, thus event category id cannot be determined
          if (typeof part.outcome === 'string') {
            if (hrEventIds.indexOf(part.eventId) < 0) {
              hrEventIds.push(part.eventId);
            }
          } else {
            const outcomes = part.outcome ? [].concat(part.outcome) : [];
            outcomes.forEach((outcome: IBetHistoryOutcome) => {
              if (outcome.eventCategory && outcome.eventCategory.id === hrCategoryId &&
                outcome.event && hrEventIds.indexOf(outcome.event.id) < 0) {
                hrEventIds.push(outcome.event.id);
              }
            });
          }
        });
      });
    });

    return hrEventIds.join(',');
  }

  private getEventsData(outcomeIds: string[], betsMap: { [key: string ]: CashoutBet | RegularBet | PlacedBet },
                        useRacingPost: boolean): Observable<ISportEvent[]> {

    const hrEventIds = useRacingPost ? this.getHREventIdsString(betsMap) : '',
      requests$: (Observable<ISportEvent[]>|Observable<IRacingPostHRResponse>)[] =
        [this.cashoutDataProvider.getEventsByOutcomesIds(outcomeIds, { racingFormOutcome: !useRacingPost })];

    if (hrEventIds) {
      requests$.push(this.racingPostService.getHorseRacingPostById(hrEventIds));
    }

    return observableForkJoin(requests$).pipe(
      map(([eventsData, racingData]: [ISportEvent[], IRacingPostHRResponse]) =>
        this.racingPostService.mergeHorseRaceData(eventsData, racingData)),
    );
  }

  private processEvents(originalMap, eventIds, eventsData: ISportEvent[] = []) {
    // eventsData - array of objects
    const eventsFromSS: { [index: string]: ISportEvent } = {};

    originalMap.allSilkNames = this.raceOutcomeDetailsService.getsilkNamesForEvents(eventsData);

    _.each(eventsData, eventEntity => {
      eventsFromSS[eventEntity.id] = eventEntity;
    });

    this.updateLegForEvent(eventsFromSS, originalMap);

    return observableOf(originalMap);
  }

  /**
   * Updating legs checking isEventEntity
   * @param eventsFromSS {object}
   * @param betsMap {object}
   */
  // TODO: bets model in betsMap argument type
  private updateLegForEvent(eventsFromSS: { [index: string]: ISportEvent }, betsMap: any): void {
    _.each(betsMap, (bet: IBetHistoryBet) => {
      bet && _.each(bet.leg, (leg: IBetHistoryLeg) => {
        const eventId = parseInt(leg.part[0].eventId, 10);
        const eventFromSS = eventsFromSS[eventId];
        const partPath = leg.part[0],
          eWTerms = partPath.eachWayPlaces,
          isEWPlace = leg.legType && leg.legType.code === 'E' && partPath.outcome[0].result.value === 'P' &&
            Number(partPath.outcome[0].result.places) <= Number(eWTerms);

        // noEventFromSS property is needed because sometimes events disappear from SS
        // even if they are not resulted
        // eventFromSS property means that there is one
        // until eventFromSS = false, loading spinner is shown
        // that is why it is needed to have one more property not to show continuous spinner
        leg.isEventEntity = false;
        leg.isBetSettled = bet.settled === 'Y';

        if (eventFromSS) {
          this.setDefaultValuesToAttributesUpdateOn(bet, eventFromSS, betsMap.allSilkNames, isEWPlace);
          leg.isEventEntity = true;
          leg.noEventFromSS = false;
          leg.eventEntity = eventFromSS;
        } else {
          const eventStatus = leg.eventEntity && leg.eventEntity.eventStatusCode;
          const market = leg.eventEntity && leg.eventEntity.markets &&
            _.find(leg.eventEntity.markets , m => Number(m.id) === Number(partPath.marketId));
          const marketStatus = market && market.marketStatusCode;
          const betOutcomeStatuses = _.pluck(bet.outcomes, 'status');
          const marketOutcomeStatuses = market && market.outcomes.length && _.pluck(market.outcomes, 'outcomeStatusCode');
          const outcomeStatuses = this.betHistoryMainService.isSingleBet(bet) ? betOutcomeStatuses : marketOutcomeStatuses;
          const partResults = leg.part.map(part => part.result);
          const result = this.betHistoryMainService.getPartsResult(partResults);

          leg.status = this.getLegStatus(
            result,
            isEWPlace,
            eventStatus,
            marketStatus,
            outcomeStatuses);

          leg.noEventFromSS = true;
        }

        this.betHistoryMainService.setBybLegStatus(bet, leg);
      });
    });
  }

  /**
   * Set default values for attributes to update on:
   * for event attributes such as displayed, status and settled,
   * for market: displayed and status,
   * for outcome: displayed, status and price
   * @param bet {Object}
   * @param eventFromSS
   * @param silkNamesArray
   * @param isEWPlace
   */
  // TODO: bet model for bet argument
  private setDefaultValuesToAttributesUpdateOn(bet: any, eventFromSS: ISportEvent, silkNamesArray: string[], isEWPlace: boolean): void {
    if (_.contains(bet.event, eventFromSS.id.toString())) {
      bet.events[eventFromSS.id] = {
        displayed: eventFromSS.isDisplayed ? this.CASH_OUT.result.YES : this.CASH_OUT.result.NO,
        status: eventFromSS.eventStatusCode
      };

      const market = _.find(eventFromSS.markets, (item: IMarket) => _.contains(bet.market, item.id.toString()));
      if (market) {
        bet.markets[market.id] = {
          displayed: market.isDisplayed ? this.CASH_OUT.result.YES : this.CASH_OUT.result.NO,
          status: market.marketStatusCode
        };

        const outcomes = _.filter(market.outcomes, item => _.contains(bet.outcome, item.id.toString()));

        _.forEach(outcomes, (outcome: IBetHistoryOutcome) => {
          const legs = _.filter(bet.leg, (item: IBetHistoryLeg) => item.part[0].eventId === eventFromSS.id.toString());
          const price = outcome.price && _.isArray(outcome.price) && outcome.price[0];

          const legParts = legs && legs[0] && legs[0].part;
          if (legParts && legParts.length > 1 && bet.legType === 'W') {
            _.each(legParts, p => {
              const legResult = (p && p.result) || '';
              this.setOutcomeData(bet, outcome, price, legResult, p);
            });
          } else {
            const legResult = (legParts && legs[0].part[0] && legs[0].part[0].result) || '';
            this.setOutcomeData(bet, outcome, price, legResult);
          }

          legs.forEach((leg: IBetHistoryLeg) => {
            const partResults = leg.part.map(part => part.result === this.CASH_OUT.handicapResultCode ? part.dispResult : part.result);
            const result = this.betHistoryMainService.getPartsResult(partResults);
            leg.status = this.getLegStatus(
              result,
              isEWPlace,
              eventFromSS.eventStatusCode,
              market.marketStatusCode,
              _.map(outcomes, outcomeEntity => outcomeEntity.outcomeStatusCode)
            );
            if (eventFromSS.categoryId === this.HORSE_RACING_CATEGORY_ID) {
              leg.allSilkNames = silkNamesArray;
            }
          });
        });
      }
    }
  }

  // TODO: RegularBet model class
  private setOutcomeData(bet: any, outcome: IOutcome, price: IOutcomePrice, legResult?: string, part?): void {
    bet.outcomes[(part && part.outcome) || outcome.id] = {
      displayed: outcome.isDisplayed ? this.CASH_OUT.result.YES : this.CASH_OUT.result.NO,
      status: outcome.outcomeStatusCode,
      lp_num: price ? price.priceNum : '',
      lp_den: price ? price.priceDen : '',
      settled: legResult === '-' ? this.CASH_OUT.result.NO : this.CASH_OUT.result.YES
    };
  }

  /**
   * Calculates status of leg
   * @param result {string}
   * @param isEWPlace {String}
   * @param eventStatusCode {string}
   * @param marketStatusCode {string}
   * @param selectionsStatusCodes {Array}
   * @returns {string}
   */
  private getLegStatus(result: string,
                       isEWPlace: boolean,
                       eventStatusCode?: string,
                       marketStatusCode?: string,
                       selectionsStatusCodes?: string[]): string {
    let status = this.CASH_OUT.resultCodes[result] || '';

    if (!status) {
      const isSomeSelectionSuspended = _.some(selectionsStatusCodes, statusCode => statusCode === 'S'),
        suspended = eventStatusCode === 'S' || marketStatusCode === 'S' || isSomeSelectionSuspended,
        settled = result !== '-';

      if (suspended) {
        status = 'suspended';
      }

      if (!settled && !suspended) {
        status = 'open';
      }
    }

    if (result === 'P') {
      status = isEWPlace ? 'won' : 'lost';
    }

    return status;
  }
}
