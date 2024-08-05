import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { UkToteEventsLinkingService } from '@core/services/ukTote/uktote-events-linking.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { SiteServerPoolService } from '@ss/services/site-server-pool.service';

import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPoolModel } from '@shared/models/pool.model';
import { IUkToteAllChannelsModel, IUkToteUpdateFunctionsModel } from '@core/services/ukTote/uktote-update.model';
import { IRacingPoolIndicator } from '@core/models/race-grid-meeting.model';

@Injectable({
  providedIn: 'root'
})
export class UkToteService {

  constructor(
    private siteServerPoolService: SiteServerPoolService,
    private siteServerService: SiteServerService,
    private sbFilter: SbFiltersService,
    private ukToteEventsLinkingService: UkToteEventsLinkingService,
    private routingHelperService: RoutingHelperService,
    private locale: LocaleService
  ) {
  }

  /**
   * Returns pools with guide values
   * @param {Object} params
   * @returns {Promise.<T>}
   */
  getGuidesData(params): Promise<IPoolModel[]> {
    return this.siteServerPoolService.getPoolToPoolValue(params);
  }

  /**
   * Get pools for event with specific params(for example event ids)
   *
   * @param {object} poolsConfig
   * @returns {Observable.<T>}
   */
  getPoolsForEvent(poolsConfig): Observable<IPoolModel[]> {
    return this.siteServerPoolService.getPoolsForEvent(poolsConfig);
  }

  /**
   * Load events for markets IDs
   * @param marketIds
   */
  loadEventsByMarketIds(marketIds: string[]): Promise<ISportEvent[]> {
    return this.siteServerService.getEventsByMarkets({ marketIds, racingFormOutcome: true, externalKeysEvent: true });
  }

  /**
   * Load events for events IDs
   * @param eventIds
   */
  loadEventsByEventIds(eventIds: string[]) {
    const eventIdsStr = eventIds.join(',');
    return this.siteServerService.getEvent(eventIdsStr, { racingFormOutcome: true }, false);
  }

  /**
   * Add to event property poolTypes if they are available for this event
   * {
   *    ...
   *    poolTypes: ["UEXA", "UPLC", ...]
   *    ...
   * }
   *
   * @param events
   */
  addAvailablePoolTypes(events: ISportEvent[]): Promise<ISportEvent[]> {
    const toteEventsIds = _.reduce(events, (memo, event: ISportEvent) => {
      const linkedToteEventIds = this.getTotePoolEventIds(event);
      return memo.concat(linkedToteEventIds);
    }, []);
    if (!toteEventsIds) {
      return Promise.resolve(events);
    }

    return Promise.all([
      this.siteServerService.getEventsToMarketsByEvents(toteEventsIds),
      this.siteServerPoolService.getPoolsForEvent({ eventsIds: toteEventsIds, poolTypes: 'UPLP,UQDP,UJKP,USC6,UPP7' }).toPromise()
    ]).then(responses => {
      const toteEvents: ISportEvent[] = responses && responses[0],
        pools = responses && responses[1];

      if (toteEvents && pools) {
        this.mapEventsWithPoolTypes(events, toteEvents, pools);
      }

      return events;
    });
  }

  /**
   * Return linked Tote event ids
   * @returns {Array} - array of linked Tote event ids
   */
  getTotePoolEventIds(eventEntity: ISportEvent): string[] {
    if (!eventEntity || !eventEntity.externalKeys) {
      return [];
    }
    const totePoolExternalKeys = ['OBEvLinkTote', 'OBEvLinkScoop6', 'OBEvLinkPlacepot7'];
    return _.compact(
      totePoolExternalKeys.map(externalKey => eventEntity.externalKeys[externalKey])
    );
  }

  /**
   * Generate pool indicators
   *
   * @param events
   * @returns {array} array of pool indicators
   */
  getPoolIndicators(events: ISportEvent[]): IRacingPoolIndicator[] {
    const indicatorsMap: { [key: string]: IRacingPoolIndicator } = {};

    // Create pool indicators map to add only the first event of certain pool type
    _.each(events, event => {
      _.each(event.poolTypes, poolType => {
        const skipEvent = event.isStarted || event.isResulted || event.isFinished;
        if (!skipEvent && (!indicatorsMap[poolType] || event.startTime < indicatorsMap[poolType].startTime)) {
          indicatorsMap[poolType] = {
            id: event.id,
            startTime: event.startTime,
            poolType: this.locale.getString(`uktote.${poolType}`),
            link: `${this.generateLinkToEvent(event)}/${UK_TOTE_CONFIG.marketPath}/${UK_TOTE_CONFIG.poolTypesMap[poolType].path}`
          };
        }
      });
    });

    return _.compact(
      _.map(UK_TOTE_CONFIG.displayOrder, (poolType: string) => indicatorsMap[poolType])
    );
  }

  /**
   * Check whether provided outcome has suspended status
   * @param {Object} outcome - outcome entity
   * @returns {boolean}
   */
  isOutcomeSuspended(outcome: IOutcome): boolean {
    return outcome.outcomeStatusCode === UK_TOTE_CONFIG.SUSPENDED_STATUS_CODE;
  }

  /**
   * Check whether provided event has suspended status
   * @param {Object} event - event entity
   * @returns {boolean}
   */
  isEventSuspended(event: ISportEvent): boolean {
    return event && event.eventStatusCode === UK_TOTE_CONFIG.SUSPENDED_STATUS_CODE;
  }

  /**
   * Check whether market of provided event has suspended status
   * @param {Object} event - event entity
   * @returns {boolean}
   */
  isMarketSuspended(event: ISportEvent): boolean {
    return event && event.markets && event.markets[0].marketStatusCode === UK_TOTE_CONFIG.SUSPENDED_STATUS_CODE;
  }

  /**
   * Check whether bet is multiple legs tote bet
   * @param betType
   */
  isMultipleLegsToteBet(betType: string): boolean {
    return _.contains(UK_TOTE_CONFIG.MULTIPLE_LEGS_TOTE_BETS, betType);
  }

  /**
   * Set isFavourite property for outcomes which are unnamed favorites
   * @param {Object} outcomeEntity
   */
  setOutcomeFavourite(outcomeEntity: IOutcome): void {
    outcomeEntity.isFavourite = +outcomeEntity.outcomeMeaningMinorCode > 0;
  }

  /**
   * Sort outcomes by runner number
   * @param outcomes
   * @param excludeFavourites
   * @returns {*}
   */
  sortOutcomes(outcomes: IOutcome[], excludeFavourites?: boolean): IOutcome[] {
    let extendedOutcomes;
    _.forEach(outcomes, (outcome: IOutcome) => {
      this.setOutcomeFavourite(outcome);
    });

    if (excludeFavourites) {
      extendedOutcomes = _.filter(outcomes, (outcome: IOutcome) => !outcome.isFavourite);
    } else {
      extendedOutcomes = outcomes;
    }

    return this.sbFilter.orderOutcomeEntities(extendedOutcomes, false, true, true);
  }

  /**
   * Extend TOTE events with fixed odds events
   * @param  {Array} toteEvents - array of TOTE events
   * @param {Boolean} isScoop6Pool
   * @returns {*}
   */
  extendToteEvents(toteEvents: ISportEvent[], isScoop6Pool: boolean): Observable<ISportEvent[]> {
    const updateFunctions = this.getUpdateFunctions();
    return this.ukToteEventsLinkingService.extendToteEvents(toteEvents, isScoop6Pool, updateFunctions);
  }

  /**
   * Add racingForm info from one event to another,
   * for outcomes with same names
   * @param mainEvent
   * @param extendingEvent
   */
  extendToteEventInfo(mainEvent: ISportEvent, extendingEvent: ISportEvent): void {
    const updateFunctions = this.getUpdateFunctions();
    this.ukToteEventsLinkingService.extendToteEventInfo(mainEvent, extendingEvent, updateFunctions);
  }

  /**
   * Get race title
   * @param event - event entity
   * @returns {string}
   * @private
   */
  getRaceTitle(event: ISportEvent): string {
    if (!event) {
      return '';
    }
    return `${event.localTime} ${event.typeName}`;
  }

  /**
   *  Get all ids of events, markets
   * and outcomes for tote pool bet
   * @private
   */
  getAllIdsForEvents(events: ISportEvent[]): IUkToteAllChannelsModel {
    const markets = _.flatten(_.pluck(events, 'markets')),
      outcomes = _.flatten(_.pluck(markets, 'outcomes'));
    return {
      event: events ? _.compact(_.pluck(events, 'linkedEventId')) : [],
      market: markets ? _.compact(_.pluck(markets, 'linkedMarketId')) : [],
      outcome: outcomes ? _.compact(_.pluck(outcomes, 'linkedOutcomeId')) : []
    };
  }

  /**
   * Extended Tote event with needed properties from fixed odds event
   * @param mainEvent - tote event
   * @param extendingEvent - fixed odds event
   * @private
   */
  private extendEvent(mainEvent: ISportEvent, extendingEvent: ISportEvent): void {
    mainEvent.linkedEventId = extendingEvent.id;
    mainEvent.eventStatusCode = extendingEvent.eventStatusCode;
    mainEvent.isResulted = extendingEvent.isResulted;
    mainEvent.isUKorIRE = extendingEvent.isUKorIRE;
    /**
     * Local time is some why wrong for Tote events
     */
    mainEvent.localTime = extendingEvent.localTime;

    /**
     * For Scoop6 events type name is not correct
     */
    mainEvent.typeName = extendingEvent.typeName;
  }

  /**
   * Extended market from Tote event with needed properties from fixed odds event
   * @param mainMarket - market entity from Tote event
   * @param extendingMarket - market entity from fixed odds event
   * @private
   */
  private extendMarket(mainMarket: IMarket, extendingMarket: IMarket): void {
    mainMarket.linkedMarketId = extendingMarket.id;
    mainMarket.marketStatusCode = extendingMarket.marketStatusCode;
  }

  /**
   * Extended outcome from Tote event with needed properties from fixed odds event
   * @param mainOutcome - outcome entity from Tote event
   * @param extendingOutcome - outcome entity from fixed odds event
   * @private
   */
  private extendOutcome(mainOutcome: IOutcome, extendingOutcome: IOutcome): void {
    if (!extendingOutcome) {
      return;
    }
    if (extendingOutcome.racingFormOutcome) {
      mainOutcome.racingFormOutcome = extendingOutcome.racingFormOutcome;
    }
    mainOutcome.linkedOutcomeId = extendingOutcome.id; 
    mainOutcome.outcomeStatusCode = extendingOutcome.outcomeStatusCode;
    this.markNonRunners(mainOutcome, extendingOutcome);
    this.normalizeRunnerName(mainOutcome);
  }

  /**
   * Get update function for event, market and outcome
   * @returns {{extendEvent: Function, extendMarket: Function, extendOutcome: Function}}
   * @private
   */
  private getUpdateFunctions(): IUkToteUpdateFunctionsModel {
    return {
      extendEvent: this.extendEvent.bind(this),
      extendMarket: this.extendMarket.bind(this),
      extendOutcome: this.extendOutcome.bind(this)
    };
  }

  /**
   * Mark outcomes as non runners only if outcome is non runner
   * in fixed odds event
   * @param {Array} events
   * @returns {Array}
   */
  private markNonRunners(outcome: IOutcome, extendingOutcomeMatch): void {
    if (extendingOutcomeMatch.name.search(/N\/R$/) === -1) {
      return;
    }
    const outcomeName = outcome.name.replace(/N\/R$/, '').trim(),
      nonRunnerOutcomeName = `${outcomeName} N/R`;
    outcome.name = nonRunnerOutcomeName;
    outcome.nonRunner = true;
  }

  /**
   * For Int TOTE names received in upper case, so this method make it normal
   * @param {IOutcome} outcome
   */
  private normalizeRunnerName(outcome: IOutcome): void {
    if (!outcome || !outcome.name || outcome.name !== outcome.name.toUpperCase()) {
      return;
    }
    const isNonRunner = outcome.name.search(/N\/R$/) !== -1,
      runnerName = outcome.name.replace(/N\/R$/, '').trim(),
      capitalizedRunnerName = runnerName.toLowerCase()
        .split(' ')
        .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
        .join(' ');
    outcome.name = isNonRunner ? `${capitalizedRunnerName} N/R` : capitalizedRunnerName;
  }

  /**
   * Generate link to horseracing event
   * @param {Object} event - outcome entity
   * @returns {string}
   */
  private generateLinkToEvent(event: ISportEvent) {
    return this.routingHelperService.formResultedEdpUrl(event);
  }

  private mapEventsWithPoolTypes(events: ISportEvent[], toteEvents: ISportEvent[], pools: IPoolModel[]): void {
    const toteEventToPoolsMap = {},
      marketToToteEventMap = _.reduce(toteEvents, (memo, toteEvent) => {
        const marketId = toteEvent.markets && toteEvent.markets.length && toteEvent.markets[0] && toteEvent.markets[0].id;
        if (marketId) {
          memo[marketId] = toteEvent.id;
        }

        return memo;
      }, {});

    _.each(pools, (pool: IPoolModel) => {
      _.each(pool.marketIds, (marketId: string) => {
        const toteEventId = marketToToteEventMap[marketId];

        if (!toteEventToPoolsMap[toteEventId]) {
          toteEventToPoolsMap[toteEventId] = [];
        }
        toteEventToPoolsMap[toteEventId].push(pool.type);
      });
    });

    _.each(events, (event: ISportEvent) => {
      const toteEventIds = this.getTotePoolEventIds(event);

      _.each(toteEventIds, toteEventId => {
        if (!toteEventToPoolsMap[toteEventId]) {
          return;
        }
        const currentPoolTypes = event.poolTypes ? event.poolTypes : [];
        event.poolTypes = currentPoolTypes.concat(toteEventToPoolsMap[toteEventId]);
      });
    });
  }
}
