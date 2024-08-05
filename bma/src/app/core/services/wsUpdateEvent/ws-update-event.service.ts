import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { TimeService } from '@core/services/time/time.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';

import { IMarket } from '@core/models/market.model';
import { IBaseObject } from '@app/inPlay/models/base-object.model';
import { IUpdateEvent } from '@core/models/update-event.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IStoredData } from '@core/services/cacheEvents/cache-events.model';
import { IEventData } from '@core/models/live-serve-update.model';
import { IDelta } from '@core/models/delta-object.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { SportEventHelperService } from '../sportEventHelper/sport-event-helper.service';

enum updateTypes {
  event = 'EVENT',
  market = 'EVMKT',
  selection = 'SELCN',
  price = 'PRICE',
  score = 'SCBRD',
  clock = 'CLOCK'
}

@Injectable()
export class WsUpdateEventService {
  isInited: boolean = false;

  constructor(
    private commentsService: CommentsService,
    private cacheEventsService: CacheEventsService,
    private timeService: TimeService,
    private fracToDecService: FracToDecService,
    private pubSubService: PubSubService,
    private scoreParserService: ScoreParserService,
    private sportEventHelperService: SportEventHelperService
   ) {}

  /**
   * initialise service, subscribe for updates
   */
  subscribe(): void {
    if (this.isInited) {
      return;
    }
    /**
     * Modify and apply update to event/events
     * {array} events - "inplay" filtered events with specific ID from update,
     * {object} updateDetails - ws update object
     */
    this.pubSubService.subscribe('wsUpdateEventService', this.pubSubService.API.WS_EVENT_UPDATE,
      (data: IUpdateEvent) => this.eventUpdateHandler(data));
    this.isInited = true;
  }

  /**
   * Event update handler
   * @param {IUpdateEvent} data
   */
  private eventUpdateHandler(data: IUpdateEvent): void {
    const eventsToUpdate = data.events;
    const updateDetails = _.extend({}, data.update);

    this.updateEvents(eventsToUpdate, updateDetails);
  }

  /**
   * Check update type and update events
   * @params {Array} eventsToUpdate - one update object response
   * @params {object} updateDetails - one update object response
   */
  private updateEvents(eventsToUpdate: ISportEvent[], updateDetails: IBaseObject): void {
    const type = updateDetails.type;
    const modifiedUpdateDetails = this.deltaObject(updateDetails);

    if (modifiedUpdateDetails.isDisplayed === false || modifiedUpdateDetails.resulted) {
      this.deleteItemFromList(eventsToUpdate, updateDetails);
    } else {
      this.applyUpdateByType(type, modifiedUpdateDetails, eventsToUpdate, updateDetails);
    }
  }

  private applyUpdateByType(type: string,
                            modifiedUpdateDetails: IDelta,
                            eventsToUpdate: ISportEvent[],
                            updateDetails: IBaseObject): void {
    _.forEach(eventsToUpdate, event => {
      switch (type) {
        case 'PRICE':
          this.updateOutcomePrice(modifiedUpdateDetails, event, updateDetails, this.eventPriceUpdate);
          break;
        case 'EVENT':
          this.applyDelta(modifiedUpdateDetails, event);
          break;
        case 'SCBRD':
          this.eventCommentsUpdate(modifiedUpdateDetails, event);
          break;
        case 'CLOCK':
          this.eventClockUpdate(modifiedUpdateDetails, event);
          break;
        case 'EVMKT' :
        case 'SELCN' :
          this.updateMarketOrOutcome(modifiedUpdateDetails, event, type, updateDetails);
          break;
        default:
      }
    });
  }

  /**
   * Preparing the delta object, based on message type - 'type'.
   * @param {object} updateDetails - data from the serve
   * @returns {object}
   */
  private deltaObject(updateDetails: IBaseObject): IDelta {
    // Parse string with updateItem prices
    const updateData = updateDetails.event;
    let payload;
    let delta = {};

    switch (updateDetails.type) {
      case 'PRICE':
        payload = updateData.market.outcome.price;

        if (payload.lp_num || payload.lp_den) {
          delta = {
            priceDec: Number(this.fracToDecService.getDecimal(payload.lp_num, payload.lp_den, 6)),
            priceDen: payload.lp_den,
            priceNum: payload.lp_num,
            status: payload.status
          };
        }
        break;
      case 'SCBRD':
        delta = updateData.scoreboard;
        break;
      case 'CLOCK':
        delta = updateData.clock;
        break;
      case 'EVMKT':
        payload = updateData.market;
        delta = {
          marketStatusCode: payload.status,
          isDisplayed: payload.displayed !== 'N'
        };
        break;
      case 'EVENT':
        payload = updateData;
        delta = {
          eventStatusCode: payload.status,
          isDisplayed: payload.displayed !== 'N',
          eventIsLive: (payload.started === 'Y'),
          raceStage: payload.race_stage,
          resulted: payload.result_conf === 'Y'
        };
        break;

      case 'SELCN':
        payload = updateData.market.outcome;
        delta = {
          outcomeStatusCode: payload.status,
          isDisplayed: payload.displayed !== 'N'
        };
        break;

      default :
        break;
    }

    return delta;
  }

  /**
   * Updating price of outcome.
   *
   * @param {object} delta - object with new price
   * @param {object} outcome - object which need to update
   */
  private eventPriceUpdate(delta: IDelta, outcome: IOutcome): void {
    let className = (outcome.prices && outcome.prices[0] && outcome.prices[0].liveShowTimer &&
      outcome.prices[0].liveShowTimer.type) || '';

    // if we have prices
    if (outcome.prices.length) {
      // get class name for highlighting buttons
      className = this.getPriceChangeClassName(delta, outcome) || className;
      this.extendOutcome(delta, outcome, className);
    } else {
      // if there was no prise before
      this.extendOutcome(delta, outcome, '');
    }
    if (delta.status !== undefined) {
      outcome.outcomeStatusCode = delta.status;
    }
  }

  /**
   * Return className for highlight buttons
   * @param {object} delta - LiveServe update
   * @param {object} outcome
   * @return {string} - className
   */
  private getPriceChangeClassName(delta: IDelta, outcome: IOutcome): string {
    let className = '';
    if (delta.status !== 'S') {
      const priceDec = outcome.prices[0].priceDec;
      const dPriceDec = delta.priceDec;
      if (+priceDec > dPriceDec) {
        className = 'bet-down';
      } else if (+priceDec < dPriceDec) {
        className = 'bet-up';
      }
    }
    return className;
  }

  /**
   * Extend outcome with updates
   * @param {object} delta - LiveServe update
   * @param {object} outcome
   * @param {string} className - className
   */
  private extendOutcome(delta: IDelta, outcome: IOutcome, className: string): void {
    if (outcome.runnerNumber &&
      outcome.prices && outcome.prices[0] &&
      outcome.prices[0].priceDec &&
      outcome.prices[0].priceDec !== delta.priceDec) {
      outcome.prices.push(_.clone(outcome.prices[0]));
    }
    /**
     * FYI, the outcome.prices has quite a specific structure:
     * outcome.prices[0] always contains the current price value
     * outcome.prices[1] is the oldest historic price (sic!)
     * outcome.prices[n - 1] is the price before the last update
     */
    // Applying new price and set type of update inc/dec
    delta.priceDen = +delta.priceDen;
    delta.priceNum = +delta.priceNum;
    // create object with priceType for cases when we receive price for selection which was empty when market was created
    if (!outcome.prices.length && delta.priceNum) {
      outcome.prices[0] = {priceType: 'LP'} as IOutcomePrice;
      outcome.correctPriceType = 'LP';
    }

    _.extend(outcome.prices[0], delta, { liveShowTimer: { type: className } });

    // Applying new status, in case event has no prices('SP')
    if (delta.status !== undefined) {
      outcome.outcomeStatusCode = delta.status;
    }

    // Remove liveShowTimer.type (class) after timeout
    setTimeout(() => delete outcome.prices[0].liveShowTimer.type,
      this.timeService.hideLiveUpdateClassTime);
  }

  /**
   * Extend event(s) cache with updated data.
   *
   * @param {object} scoreboardData - object with new comments data
   * @param {object} event - event which need to update
   */
  private eventCommentsUpdate(scoreboardData: IDelta, event: ISportEvent): void {
    const methodName = `${event.categoryCode.toLowerCase()}UpdateExtend`;
    const extender = this.commentsService[methodName];
    const scoreType = this.scoreParserService.getScoreType(event.categoryId);

    if (extender && event.comments) {
      extender(event.comments, scoreboardData);
      this.pubSubService.publish(this.pubSubService.API.EVENT_SCORES_UPDATE, { event });
    } else if (scoreType) {
      if (!event.comments) {
        if (this.sportEventHelperService.isTennis(event)) {
          event.comments = { teams: { player_1: { id: `${event.id}` }, player_2: { id: `${event.id}` } } };
        } else {
          event.comments = { teams: { home: { eventId: event.id }, away: { eventId: event.id } }  };
        }
      }

      this.commentsService.updateSportScores(event.comments, scoreboardData);
      this.pubSubService.publish(this.pubSubService.API.EVENT_SCORES_UPDATE, { event });
    }
  }

  /**
   * Extend event(s) cache with updated clock.
   *
   * @param {object} clockData - object with new clock data
   * @param {object} event - event which need to update
   */
  private eventClockUpdate(clockData: IDelta, event: ISportEvent): void {
    if (event && event.clock) {
      event.clock.refresh(clockData);
      this.pubSubService.publish(this.pubSubService.API.EVENTS_CLOCK_UPDATE, { event, clockData });
    }
  }

  /**
   * Extend event(s) cache with updated data.
   * @param {object} delta - object with new data
   * @param {object} obj - object which need to update
   */
  private applyDelta(delta: IDelta, obj: ISportEvent | IDelta): void {
    _.extend(obj, delta);
    this.pubSubService.publish(this.pubSubService.API.WS_EVENT_UPDATED, obj);
  }

  /**
   * Delete element from cache by type, could be event|market|selection
   * @params {object} updateData - live update object response
   */
  private deleteItemFromList(eventsList: ISportEvent[], updateData: IBaseObject): void {
    const eventId = updateData.event.eventId.toString();

    if (updateData.type === 'EVENT') {
      this.deleteEvent(eventId, eventsList, updateTypes.event);
    } else if (updateData.type === 'EVMKT') {
      this.deleteMarket(eventId, updateData.event.market.marketId.toString(), eventsList);
    } else if (updateData.type === 'SELCN') {
      this.deleteSelection(eventId,
        updateData.event.market.outcome.outcomeId.toString(),
        updateData.event.market.marketId.toString(),
        eventsList);
    }
  }

  /**
   * Delete selections from cache
   * @param {String} eventId
   * @param {String} marketId
   * @param {String} selectionId
   * @param {Array} eventsList
   */
  private deleteSelection(eventId: string, selectionId: string, marketId: string, eventsList: ISportEvent[]): void {
    _.each(eventsList, (event: ISportEvent) => {
      const marketIndex = _.findIndex(event.markets, { id: marketId });
      if (marketIndex !== -1) {
        const outcomeIndex = _.findIndex(event.markets[marketIndex].outcomes, { id: selectionId });
        if (outcomeIndex !== -1) {
          event.markets[marketIndex].outcomes.splice(outcomeIndex, 1);

          this.pubSubService.publish(this.pubSubService.API.DELETE_SELECTION_FROMCACHE, { selectionId, marketId, eventId });

          if (!event.markets[marketIndex].outcomes.length) {
            event.markets.splice(marketIndex, 1);
            this.pubSubService.publish(this.pubSubService.API.DELETE_MARKET_FROM_CACHE);

            if (!event.markets.length) {
              this.deleteEvent(eventId, eventsList, updateTypes.selection);
            }
          }
        }
      }
    });
  }

  /**
   * Delete market from cache
   * @param {String} eventId
   * @param {String} marketId
   * @param {Array} eventsList
   */
  private deleteMarket(eventId: string, marketId: string, eventsList: ISportEvent[]): void {
    _.each(eventsList, (event: ISportEvent) => {
      const marketIndex = _.findIndex(event.markets, { id: marketId });

      if (marketIndex !== -1) {
        event.markets.splice(marketIndex, 1);

        this.pubSubService.publish(this.pubSubService.API.DELETE_MARKET_FROM_CACHE);

        if (!event.markets.length) {
          this.deleteEvent(eventId, eventsList, updateTypes.market);
        }
      }
    });
  }

  /**
   * Delete event from cache
   * @param {String} eventId
   * @param {array} eventsList
   * @param {string} updateType
   */
  private deleteEvent(eventId: string, eventsList: ISportEvent[], updateType: string): void {
    const globalEventsCacheData: IStoredData = this.cacheEventsService.storedData;
    // for events in global cache
    const refToDelete = [];

    _.each(globalEventsCacheData.index[eventId], (ref: IEventData, refName: string) => {
      const path = ref.path,
        index = path.pop(),
        arrayRef = path.reduce((obj, i) => obj[i], globalEventsCacheData) || [];
      let eventDataIndex = 0;

      arrayRef.forEach((data, dataIndex) => {
        if (data.id && data.id.toString() === eventId) {
          eventDataIndex = dataIndex;
        }
      });

      // As we can have duplicated events in modules with different markets/selections,
      // do not delete event with present market, when we have market or selection update
      if ((updateType === updateTypes.market || updateType === updateTypes.selection) &&
              arrayRef[eventDataIndex] && arrayRef[eventDataIndex].markets.length > 0) {
        // return popped value from path array if we do not delete event
        path.push(index);
        return;
      }

      refToDelete.push(refName);
      arrayRef.splice(index, 1);
      this.updatePaths(path, arrayRef, globalEventsCacheData);
    });

    // for internal inPlay cached events
    _.each(eventsList, (event: ISportEvent) => {
      const { id, isStarted, categoryName, categoryCode, typeName } = event;
      this.pubSubService.publish(this.pubSubService.API.DELETE_EVENT_ON_LIVE_STREAM_MODULE,
        { id, isStarted, categoryName, categoryCode, typeName });
    });

    this.pubSubService.publish(this.pubSubService.API.WS_EVENT_DELETE, [globalEventsCacheData, parseInt(eventId, 10)]);
    this.pubSubService.publish(this.pubSubService.API.DELETE_EVENT_FROM_CACHE, parseInt(eventId, 10));

    // remove only refs where event was deleted
    refToDelete.forEach((refName: string) => {
      delete globalEventsCacheData.index[eventId][refName];
    });

    // remove index property when no event caches
    if (globalEventsCacheData.index[eventId] && Object.keys(globalEventsCacheData.index[eventId]).length === 0) {
      delete globalEventsCacheData.index[eventId];
    }
  }

  /**
   * Update global cash indexes after deleting
   * @param path
   * @param arrayRef
   * @param globalEventsCacheData
   */
  private updatePaths(path: string[], arrayRef: ISportEvent[], globalEventsCacheData): void {
    _.each(arrayRef, (event: ISportEvent, index: number) => {
      _.each(globalEventsCacheData.index[event.id], (moduleOfEvent: IEventData) => {
        const oldPath = moduleOfEvent.path.slice();
        oldPath.pop();
        if (_.isEqual(oldPath, path)) {
          moduleOfEvent.path[moduleOfEvent.path.length - 1] = index;
        }
      });
    });
  }

  /**
   * Update market or outcome
   * @param {object} delta - LiveServe update
   * @param event
   * @param typeId
   * @param updateData
   * @param {function} callbackFn - Function to execute
   */
  private updateMarketOrOutcome(delta: IDelta, event: ISportEvent, typeId: string, updateData: IBaseObject): void {
    const marketId = updateData.event.market.marketId.toString();
    const market = _.findWhere(event.markets, { id: marketId });

    const modifiedUpdateData = delta;
    let updateEntity = <IDelta>{};

    if (!market) {
      return;
    }

    if (typeId === 'EVMKT') {
      updateEntity = market;
    }

    if (typeId === 'SELCN') {
      updateEntity = _.findWhere(market.outcomes, { id: updateData.event.market.outcome.outcomeId.toString() });
    }

    // If current status is changed, we will update the price
    const shouldUpdatePrice = (
      typeId === 'SELCN' &&
      updateEntity &&
      modifiedUpdateData &&
      updateEntity.outcomeStatusCode !== modifiedUpdateData.outcomeStatusCode &&
      updateData.event.market.outcome.price);

    // workaround for joined SELCN/PRICE update
    // if event is unsuspended/suspended and price changed at the same time, update data come in one SELCN update
    if (shouldUpdatePrice) {
      // change type of update
      updateData.type = 'PRICE';

      // run usual update with price type, to get updated prices
      this.updateEvents([event], updateData);
    }

    this.applyDelta(modifiedUpdateData, updateEntity);
    this.pubSubService.publishSync(this.pubSubService.API.OUTCOME_UPDATED, market);
  }

  /**
   * Update outcome
   * @param {object} delta - ws modified update
   * @param {object} event
   * @param {object} updateData - not modified update data
   * @param {function} callbackFn - Function to execute
   */
  private updateOutcomePrice(delta: IDelta, event: ISportEvent, updateData: IBaseObject, callbackFn: Function): void {
    _.each(event.markets, (market: IMarket) => {
      const outcome = _.findWhere(market.outcomes, { id: updateData.event.market.outcome.outcomeId.toString() });
      if (outcome) {
        callbackFn.call(this, delta, outcome);
        this.pubSubService.publishSync(this.pubSubService.API.OUTCOME_UPDATED, market);
      }
    });
  }
}
