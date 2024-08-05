import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { Subscription, timer } from 'rxjs';
import { concatMap } from 'rxjs/operators';

import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { TimeService } from '@core/services/time/time.service';
import { LStoSSDataStructureConverterService } from '@core/services/lStoSSDataConverter/ls-ss-data-converter.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { IConstant } from '@core/services/models/constant.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ILiveServeUpd, IPayload, IReference, IEventData } from '@core/models/live-serve-update.model';
import { IDelta } from '@core/models/delta-object.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { SiteServerEventToOutcomeService } from '@ss/services/site-server-event-to-outcome.service';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@core/services/cms/cms.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable()
export class UpdateEventService {
  // update id cache, for identifying duplicate updates
  cache: { updateId: string, channel: string } = { updateId: '', channel: '' };
  storedData: any;
  private siteServerLiveMarketsConfig: {
    enabled: boolean;
    sportCategoriesIds: string;
    delayMilliseconds: number;
  };
  private siteServerLiveMarketsSubscriptions: Subscription[] = [];
  private readonly HR_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  private static getEventCategory(event: IConstant): string {
    if (!event) {
      return '';
    }

    for (const i of Object.keys(event)) {
      if (event[i].reference && event[i].reference.categoryId) {
        return event[i].reference.categoryId;
      }
    }

    return '';
  }

constructor(
    private cacheEventsService: CacheEventsService,
    private commentsService: CommentsService,
    private timeService: TimeService,
    private lStoSSDataStructureConverterService: LStoSSDataStructureConverterService,
    private fracToDecService: FracToDecService,
    private filtersService: FiltersService,
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService,
    private scoreParserService: ScoreParserService,
    private siteServerEventToOutcomeService: SiteServerEventToOutcomeService,
    private cmsService: CmsService,
    private awsService: AWSFirehoseService,
  ) {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.siteServerLiveMarketsConfig = config.SiteServerLiveMarkets || { enabled: false, sportCategoriesIds: '', delayMilliseconds: 0 };
    });
    this.init();
  }

  /**
   * initialise service, subscribe for updates
   */
  init(): void {
    this.cache = { updateId: '', channel: '' }; // update id cache, for identifying duplicate updates
    this.storedData = this.cacheEventsService.storedData; // get data from local storage

    this.pubSubService.subscribe('updateEventFactory', this.pubSubService.API.SPORT_EDP_CLOSED,
      this.clearLiveMarketsSubscriptions.bind(this));

    this.pubSubService.subscribe('updateEventFactory', this.pubSubService.API.LIVE_SERVE_MS_UPDATE, (update: any) => {
      setTimeout(() => {
        if (this.checkForNewMarketOutcomeFromLS(update)) {
          // new market or outcome found (not stored in cache)
          this.handleEDPLiveMarket(update);
        } else {
          this.updateStoredDataElement(update);
        }
      });
    });

    this.windowRefService.document.addEventListener('LIVE_SERVE_UPDATE', (data: CustomEvent) => {
      const update = data.detail.liveUpdate;
      const msgId: string = update.msg_id || update[0].msg_id;

      if (this.cache.updateId !== msgId) {
        this.cache.updateId = msgId;
        this.cache.channel = update.channel;
        setTimeout(() => {
          if (_.isArray(update)) {
            _.forEach(update, (updateItem: ILiveServeUpd) => {
              if (this.checkForNewMarketOutcomeFromLS(updateItem)) {
                // new market or outcome found (not stored in cache)
                this.handleEDPLiveMarket(updateItem);
              } else {
                this.updateStoredDataElement(updateItem);
              }
            });
          } else {
            if (this.checkForNewMarketOutcomeFromLS(update)) {
              // new market or outcome found (not stored in cache)
              this.handleEDPLiveMarket(update);
            } else {
              this.updateStoredDataElement(update);
            }
          }
          this.pubSubService.publish(this.pubSubService.API.LIVE_SERVE_UPDATE);
        });
      }
    });
  }

  /**
   * Adds market to cache and send to EDP when market is undisplayed and
   * put to not displayed market to map in order to push them to EDP later on displayed = 'Y" update
   * @param update
   * @private
   */
  private handleEDPLiveMarket(update: ILiveServeUpd): void {
    if (update.payload.displayed === 'Y') {
      const marketLink = this.cacheEventsService.storeNewMarketOrOutcome(
        this.lStoSSDataStructureConverterService.convertData(update)
      ) as IMarket;
      if (marketLink) {
        if (this.isSiteServerGetNewMarketAllowed(update, this.siteServerLiveMarketsConfig, this.storedData)) {
          const subscription = timer(Number(this.siteServerLiveMarketsConfig.delayMilliseconds))
            .pipe(
              concatMap(() => this.siteServerEventToOutcomeService.getEventToOutcomeForMarket({marketIds: [update.subject_number]}))
            )
            .subscribe((data) => {
              const ssMarketAvailable = !!(data.length && data[0].markets && data[0].markets.length);
              let ssMarketOutcomesAvailable = false;

              if (ssMarketAvailable && data[0].markets[0].outcomes && data[0].markets[0].outcomes.length) {
                ssMarketOutcomesAvailable = true;
                marketLink.cashoutAvail = data[0].markets[0].cashoutAvail;

                this.cacheEventsService.storeNewOutcomes(data[0].markets[0].outcomes);
                this.pubSubService.publish(this.pubSubService.API.LIVE_MARKET_FOR_EDP, marketLink);
              }

              this.awsService.addAction('EDPLiveMarketInfoAvailable', { ssMarketAvailable });
              this.awsService.addAction('EDPLiveMarketOutcomesInfoAvailable', { ssMarketOutcomesAvailable });
            });
          this.siteServerLiveMarketsSubscriptions.push(subscription);
        } else {
          this.pubSubService.publish(this.pubSubService.API.LIVE_MARKET_FOR_EDP, marketLink);
        }
      }
    }
  }

  /**
   * clearLiveMarketsSubscriptions are left from requests to ss for new markets
   */
  private clearLiveMarketsSubscriptions(): void {
    this.siteServerLiveMarketsSubscriptions.forEach(subscription => subscription.unsubscribe());
    this.siteServerLiveMarketsSubscriptions = [];
  }

  /**
   * Check whether SiteServ Live Markets configured in CMS and whether the call to SiteServ is needed.
   * @param update
   * @param config
   * @param storedData
   */
  private isSiteServerGetNewMarketAllowed(update: ILiveServeUpd, config, storedData): boolean {
    if (update.subject_type !== 'sEVMKT' || !this.siteServerLiveMarketsConfig.enabled) {
      return false;
    }

    const eventCategoryId: string = storedData.index[update.channel_number].eventdata.reference.categoryId;

    return !!(config.sportCategoriesIds === '' || config.sportCategoriesIds.split(',').includes(eventCategoryId)) ;
  }

  /**
   * Check if market or selection is new(not stored in cache index)
   * @param {object} update
   * @return {object|null}
   */
  private checkForNewMarketOutcomeFromLS(update: ILiveServeUpd): boolean {
    let isInCache = true;
    if (update.subject_type === 'sEVMKT') {
      isInCache = _.has(this.storedData.marketsIndex, update.subject_number.toString());
    } else if (update.subject_type === 'sSELCN') {
      isInCache = _.has(this.storedData.outcomesIndex, update.subject_number.toString());
    }

    return !isInCache;
  }

  /**
   * Pick response type and update event
   * @params {Object} update - one update object response
   */
  private updateStoredDataElement(update: ILiveServeUpd): void {
    const type = update.subject_type;
    let updateFunc;

    if (type === 'sPRICE' || type === 'sSELCN') {
      updateFunc = this.eventPriceUpdate;
    } else if (type === 'sSCBRD') {
      updateFunc = this.eventCommentsUpdate;
    } else if (type === 'sCLOCK') {
      updateFunc = this.eventClockUpdate;
    } else {
      updateFunc = this.applyDelta;
    }

    const delta = this.deltaObject(update);

    this.updateEventsObject(delta, update, updateFunc, type);
  }

  /**
   * Preparing the delta object, based on message type - 'subject_type'.
   * @param {Object} updateItem - data from the serve
   * @returns {Object}
   */
  private deltaObject(updateItem: ILiveServeUpd): IDelta {
    // Parse string with updateItem prices
    const payload = updateItem.payload;
    let delta = <IDelta>{};

    switch (updateItem.subject_type) {
      case 'sPRICE':

        if (payload.lp_num || payload.lp_den) {
          delta = {
            priceDec: Number(this.fracToDecService.getDecimal(Number(payload.lp_num), Number(payload.lp_den), 6)),
            priceDen: Number(payload.lp_den),
            priceNum: Number(payload.lp_num),
            status: payload.status,
            isDisplayed: true,
            priceType: 'LP'
          };
        }
        break;

      case 'sSCBRD':
      case 'sCLOCK':
        delta = payload;
        delta.isDisplayed = true;
        break;

      case 'sEVMKT':
        delta = {
          marketStatusCode: payload.status,
          isDisplayed: payload.displayed !== 'N'
        };
        break;

      case 'sEVENT':
        // get event to which this update is referring, in order to determine,
        // if we need to parse scores with fallback score parser for Gaelic Football or Tennis
        const event = this.storedData.index[updateItem.channel_number];
        const categoryId = UpdateEventService.getEventCategory(event);
        const scoreType = this.scoreParserService.getScoreType(categoryId);
        const scores = ['BoxScore', 'GAA', 'SetsGamesPoints'].includes(scoreType) &&
            this.scoreParserService.parseScores(payload && payload.names.en, scoreType);

        delta = {
          eventStatusCode: payload.status,
          isDisplayed: payload.displayed !== 'N',
          eventIsLive: (payload.started === 'Y'),
          raceStage: payload.race_stage,
          resulted: payload.result_conf === 'Y',
          score: scores || this.commentsService.parseScoresFromName(payload.names),
          originalName: payload.names && payload.names.en,
        };
        break;
      case 'sSELCN':
        delta = {
          status: payload.status,
          isDisplayed: payload.displayed !== 'N'
        };
        if (payload.lp_num || payload.lp_den) {
          const priceDelta = {
            priceDec: Number(this.fracToDecService.getDecimal(Number(payload.lp_num), Number(payload.lp_den), 6)),
            priceDen: Number(payload.lp_den),
            priceNum: Number(payload.lp_num)
          };
          _.extend(delta, priceDelta);
        }
        break;

      default :
        break;
    }

    return delta;
  }

  /**
   * Updating price of outcome.
   *
   * @param {Object} delta - object with new price
   * @param {Object} outcome - object which need to update
   */
  private eventPriceUpdate(delta: IDelta, outcome: IOutcome): void {
    let className = (outcome.prices && outcome.prices[0] && outcome.prices[0].liveShowTimer &&
      outcome.prices[0].liveShowTimer.type) || '';

    outcome.prices = outcome.prices || [];
    if (delta.priceType === 'LP' && outcome.prices.length === 0) {
      outcome.correctPriceType = 'LP';
      outcome.prices.push(delta as IOutcomePrice);
      return;
    }
    // if we have prices
    if (outcome.prices.length) {
      // get class name for highlighting buttons
      className = this.getPriceChangeClassName(delta, outcome) || className;
      this.extendOutcome(delta, outcome, className);
    } else if (delta.status !== undefined) {
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
      if (+outcome.prices[0].priceDec > delta.priceDec) {
        className = 'bet-down';
      } else if (+outcome.prices[0].priceDec < delta.priceDec) {
        className = 'bet-up';
      }
    }
    return className;
  }

  /**
   * Extend outcome with updates
   * @param {Object} delta - LiveServe update
   * @param {Object} outcome
   * @param {string} className - className
   */
  private extendOutcome(delta: IDelta, outcome: IOutcome, className: string): void {
    const oPrice = outcome.prices && outcome.prices[0];

    if (outcome.runnerNumber && oPrice && oPrice.priceDec && oPrice.priceDec !== delta.priceDec) {
      outcome.prices.push(_.clone(oPrice));
    }
    /**
     * FYI, the outcome.prices has quite a specific structure:
     * outcome.prices[0] always contains the current price value
     * outcome.prices[1] is the oldest historic price (sic!)
     * outcome.prices[n - 1] is the price before the last update
     */
    // Applying new price and set type of update inc/dec
    _.extend(oPrice, delta, { liveShowTimer: { type: className } });

    // Applying new status, in case event has no prices('SP')
    if (delta.status !== undefined) {
      outcome.outcomeStatusCode = delta.status;
    }

    // Remove liveShowTimer.type (class) after timeout
    setTimeout(() => oPrice && delete oPrice.liveShowTimer.type, this.timeService.hideLiveUpdateClassTime);
  }

  /**
   * Extend event(s) cache with updated data.
   *
   * @param {Object} payload - object with new comments data
   * @param {Object} obj - event which need to update
   */
  private eventCommentsUpdate(payload: IPayload, obj: ISportEvent): void {
    const methodName = `${obj.categoryCode.toLowerCase()}UpdateExtend`;
    const extender = this.commentsService[methodName];

    if (obj.comments && extender) {
      extender(obj.comments, payload);
    }
  }

  /**
   * Extend event(s) cache with updated clock.
   *
   * @param {Object} payload - object with new clock data
   * @param {Object} obj - event which need to update
   */
  private eventClockUpdate(payload: IPayload, obj: ISportEvent): void {
    if (obj && payload.ev_id === String(obj.id) && obj.clock) {
      obj.clock.refresh(payload);
    }
  }

  /**
   * Extend event(s) cache with updated data.
   *
   * @param {Object} delta - object with new data
   * @param {Object} obj - object which need to update
   */
  private applyDelta(delta: IDelta, obj: ISportEvent): void {
    if (delta.score && obj.comments) {
      this.commentsService.sportUpdateExtend(obj.comments, delta.score);
    }

    _.extend(obj, delta);
  }

  /**
   * Delete element from cache by type, could be event|market|selection
   * @params {Object} updateData - live update object response
   */
  private deleteItemFromCacheByType(updateData: ILiveServeUpd): void {
    const eventId = updateData.channel_number.toString();
    if (updateData.subject_type === 'sEVENT') {
      this.deleteEvent(eventId);
    } else if (updateData.subject_type === 'sEVMKT') {
      this.deleteMarket(eventId, updateData.subject_number.toString());
    } else if (updateData.subject_type === 'sSELCN') {
      this.deleteSelection(eventId, updateData.payload.ev_mkt_id.toString(), updateData.subject_number.toString());
    }
  }

  /**
   * Delete selections from cache
   * @param {string} eventId
   * @param {string} marketId
   * @param {string} selectionId
   */
  private deleteSelection(eventId: string, marketId: string, selectionId: string): void {
    _.each(this.storedData.index[eventId], (ref: IEventData) => {
      const marketIndex = _.findIndex(ref.reference.markets, { id: marketId });
      if (marketIndex !== -1) {
        const isSurfaceBet = ref.path[0].match('surfaceBet');
        const outcomeIndex = _.findIndex(ref.reference.markets[marketIndex].outcomes, { id: selectionId });
        if (outcomeIndex !== -1) {
          ref.reference.markets[marketIndex].groupedOutcomes && ref.reference.markets[marketIndex].groupedOutcomes.splice(outcomeIndex, 1);
          ref.reference.markets[marketIndex].outcomes.splice(outcomeIndex, 1);
          this.pubSubService.publish(this.pubSubService.API.DELETE_SELECTION_FROMCACHE, { selectionId, marketId, eventId });
          delete this.storedData.outcomesIndex[selectionId];
          !isSurfaceBet && this.pubSubService.publish('UPDATE_OUTCOMES_FOR_MARKET', ref.reference.markets[marketIndex]);
          if (!ref.reference.markets[marketIndex].outcomes.length) {
            ref.reference.markets.splice(marketIndex, 1);
            !isSurfaceBet && this.pubSubService.publish(this.pubSubService.API.DELETE_MARKET_FROM_CACHE, marketId);
            if (!ref.reference.markets.length && !isSurfaceBet) {
              this.deleteEvent(eventId);
            }
          }
        }
      }
    });
  }

  /**
   * Delete market from cache
   * @param {string} eventId
   * @param {string} marketId
   */
  private deleteMarket(eventId: string, marketId: string): void {
    _.each(this.storedData.index[eventId], (ref: IEventData) => {
      const marketIndex = _.findIndex(ref.reference.markets, { id: marketId });

      if (marketIndex !== -1) {
        ref.reference.markets.splice(marketIndex, 1);
        delete this.storedData.marketsIndex[marketId];
        this.pubSubService.publish(this.pubSubService.API.DELETE_MARKET_FROM_CACHE, marketId);
        if (!ref.reference.markets.length) {
          this.deleteEvent(eventId);
        }
      }
    });
  }

  /**
   * Delete event from cache
   *
   * @param {String} eventId
   */
  private deleteEvent(eventId: string): void {
    let persistentInCacheEventFound = false;
    // inPlay cache names
    const cacheNames = ['liveEventsStream', 'liveStream', 'liveStreamWidget'];
    _.each(this.storedData.index[eventId], (ref: IEventData) => {
      const path = ref.path.slice(0, -1),
        index = ref.path[ref.path.length - 1],
        arrayRef = path.reduce((obj, i) => obj[i], this.storedData);

      // In-Play workaround
      if (_.contains(cacheNames, path[0])) {
        const { id, isStarted, categoryName, categoryCode, typeName } = arrayRef[index];
        this.pubSubService.publish(this.pubSubService.API.DELETE_EVENT_ON_LIVE_STREAM_MODULE,
          { id, isStarted, categoryName, categoryCode, typeName });
      }

      if (ref.reference.persistentInCache) {
        persistentInCacheEventFound = true;
      }

      if (arrayRef && !ref.reference.persistentInCache) {
        const eventIdtoDelete = arrayRef.findIndex((eventDetail) => eventDetail.id === Number(eventId));
        if (eventIdtoDelete > -1) {
          arrayRef.splice(eventIdtoDelete, 1);
        }
      }
    });

    if (!persistentInCacheEventFound) {
      delete this.storedData.index[eventId];
    }

    this.pubSubService.publishSync(this.pubSubService.API.DELETE_EVENT_FROM_CACHE, Number(eventId));
  }

  /**
   * Update event.
   *
   * @param {Object} delta - LiveServe update
   * @param {Object} update - Payload object from server
   * @param {function} fn - Function to execute
   * @param {string} type of incoming update
   */
  private updateEventsObject(delta: IDelta, update: ILiveServeUpd, fn: Function, type: string): void {
    // getting events from index by index id which is equals to update.channel_number
    let eventForUpdate = this.storedData.index[update.channel_number];

    // channel can be not only sEVENT or SEVENT
    const isSelection = update.channel.indexOf('sSELCN') !== -1;
    const isMarket = update.channel.indexOf('sEVMKT') !== -1;
    const isMarketChild = update.channel.indexOf('SEVMKT') !== -1;

    /**
     * if channel is not sEVENT we can use index mapping
     * market.id -> event.id or outcome.id -> event.id
     */
    if (!eventForUpdate && (isSelection || isMarket || isMarketChild)) {
      const cacheFactory = isSelection
        ? this.storedData.outcomesIndex
        : this.storedData.marketsIndex;

      const id = cacheFactory && cacheFactory[update.channel_number];
      eventForUpdate = this.storedData.index[id] || [];
    }

    // if event update event, if not update entity with updateMarketOrOutcome func
    if (type === 'sEVENT' || type === 'sSCBRD' || type === 'sCLOCK') {
      _.each(eventForUpdate, (ref: IEventData) => {
        fn.call(this, delta, ref.reference);

        this.pubSubService.publish(this.pubSubService.API.EVENT_SCORES_UPDATE, {event: ref.reference});

        // Needs for next events module(bigcompetitions), move event from next event to inlay card
        if (delta.eventIsLive) {
          this.pubSubService.publish(this.pubSubService.API.MOVE_EVENT_TO_INPLAY, ref.reference);
        } else if (type === 'sEVENT') {
          // Needs for outrights module(bigcompetitions), apply update to all
          // events(because in outright module different markets stored in separate events with the same ids)
          this.pubSubService.publish(this.pubSubService.API.SUSPENDED_EVENT, [update.channel_number, delta]);
        }
      });
    } else if (type === 'sPRICE' || type === 'sSELCN') {
      this.updateOutcomePrice(delta, eventForUpdate, update, fn);
    } else {
      this.updateMarketOrOutcome(delta, eventForUpdate, type, update, fn);
    }

    // delete item from cache
    if (!delta.isDisplayed || delta.resulted || this.isNextRacingEventIsOff(eventForUpdate, update)) {
      this.deleteItemFromCacheByType(update);
    }

    if (type === 'sEVENT' && (update.payload.is_off === 'Y' || update.payload.race_stage === 'O')) {
      this.storedData.events?.featured && this.storedData.events.featured[this.HR_CATEGORY_ID]?.data?.forEach(event => {
        if(update.channel_number === event.id) {
          event.rawIsOffCode = 'Y';
        }
      });
      this.pubSubService.publish('EXTRA_PLACE_RACE_OFF', update.channel_number);
    }

    if ((type === 'sEVENT' && (delta.eventStatusCode === 'S' || delta.eventStatusCode === 'A')) || (type === 'sEVMKT' && (delta.marketStatusCode === 'S' || delta.marketStatusCode === 'A'))) {
      this.storedData.events?.featured && this.storedData.events.featured[this.HR_CATEGORY_ID]?.data?.forEach(event => {
        if (update.channel_number === event.id) {
          if (delta.eventStatusCode === 'S' || delta.eventStatusCode === 'A') {
            event.eventStatusCode = delta.eventStatusCode;
          } else {
            event.markets?.forEach(market => {
              if(market.id == update.subject_number){
                market.marketStatusCode = delta.marketStatusCode;
              }
            });
          }
        }
      });
      delta.fcMktAvailable = update.payload.fc_avail;
      delta.tcMktAvailable = update.payload.tc_avail;
      delta.originalName = update.payload.names && update.payload.names.en;
      this.pubSubService.publish(this.pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT, [update.channel_number, delta]);
    }
  }

  private isNextRacingEventIsOff(eventData: IConstant, update: ILiveServeUpd): boolean {
    const nextRacesEventsExistsInCache = eventData && Object.keys(eventData).some(cacheName => cacheName.includes('nextFour'));

    return !!(nextRacesEventsExistsInCache && (update.payload && update.payload.is_off === 'Y'));
  }

  private updateMarketPriceType(market: IMarket, payload: IPayload) {
    market.isLpAvailable = payload.lp_avail === 'Y';
    market.isSpAvailable = payload.sp_avail === 'Y';
    market.priceTypeCodes = `${market.isLpAvailable ? 'LP,' : ''}${market.isSpAvailable ? 'SP,' : ''}`;
  }

  /**
   * Update market or outcome
   * @param {Object} delta - LiveServe update
   * @param events
   * @param typeId
   * @param updateData
   * @param {function} callbackFn - Function to execute
   */
  private updateMarketOrOutcome(delta: IDelta,
                                events: IEventData[],
                                typeId: string,
                                updateData: ILiveServeUpd,
                                callbackFn: Function): void {
    const isMarketHcapUpdate = typeId === 'sEVMKT' || typeId === 'sMHCAP';
    const eventsReferences = events || [];
    let marketId = null;

    if (typeId === 'sEVMKT' || typeId === 'sMHCAP') {
      marketId = updateData.subject_number.toString();
    } else if (updateData.payload.ev_mkt_id) {
      marketId = updateData.payload.ev_mkt_id.toString();
    }

    _.each(eventsReferences, (ref: IEventData) => {
      const market = _.findWhere(ref.reference.markets, { id: marketId });
      if (market) {
        const payload = updateData.payload;

        if (isMarketHcapUpdate && payload.raw_hcap && payload.hcap_values) {
          this.updateOutcomeHandicap(market, payload);
        }

        if (typeId === 'sEVMKT') {
          this.updateMarketPriceType(market, payload);
        }

        const updateEntity = typeId === 'sEVMKT' ? market
          : _.findWhere(market.outcomes, { id: updateData.subject_number.toString() }); // type === 'sSELCN' - outcome
        if (updateEntity) {
          callbackFn.call(this, delta, updateEntity);
          this.pubSubService.publishSync(this.pubSubService.API.OUTCOME_UPDATED, market);
        }
      }
    });
  }

  /**
   * Updates index markets in two ways. Checks push response (payload.hcap_values) to define way of handling.
   * @param market {object}
   * @param payload {object}
   * @private
   */
  private updateOutcomeHandicap(market: IMarket, payload: IPayload): void {
    const rawHandicap = payload.raw_hcap;
    market.rawHandicapValue = rawHandicap;
    const hvalues = payload.hcap_values;
    const handicapThreeWayType = hvalues.H && hvalues.A && hvalues.L;
    const handicapTwoWayType = hvalues.H && hvalues.A;
    const totalPointsType = hvalues.B && hvalues.H && hvalues.L && hvalues.E;
    if(market.outcomes && market.outcomes.length){
      if (handicapThreeWayType) {
        this.setOutcomeNameWithHandicapVal(market.outcomes[0], rawHandicap, rawHandicap);
        this.setOutcomeNameWithHandicapVal(market.outcomes[1], rawHandicap, rawHandicap);
        if (market.outcomes[2]) {
          this.setOutcomeNameWithHandicapVal(market.outcomes[2], (-rawHandicap).toFixed(1), rawHandicap);
        }
      } else if (handicapTwoWayType) {
        this.setOutcomeNameWithHandicapVal(market.outcomes[0], rawHandicap, rawHandicap);
        this.setOutcomeNameWithHandicapVal(market.outcomes[1], (-rawHandicap).toFixed(1), rawHandicap);
      } else if (totalPointsType) {
        _.each(market.outcomes, outcome => {
          this.setOutcomeNameWithHandicapVal(outcome, rawHandicap, rawHandicap);
        });
      }
    }
  }

  /**
   * Sets outcome handicap values to props
   * @param outcome {object}
   * @param hcapVal {string}
   * @param rawHcapVal {string}
   * @private
   */
  private setOutcomeNameWithHandicapVal(outcome: IOutcome, hcapVal: number | string, rawHcapVal: number | string): void {
    outcome.name = `${this.getOriginalName(outcome)}${this.filtersService.makeHandicapValue(hcapVal, outcome)}`;

    if (outcome.alphabetName) {
      outcome.alphabetName = outcome.name;
    }

    outcome.prices[0].handicapValueDec = hcapVal;
    outcome.prices[0].rawHandicapValue = rawHcapVal;
  }

  /**
   * Defines name without handicap value
   * @param outcome {object}
   * @return {string}
   * @private
   */
  private getOriginalName(outcome: IOutcome): string {
    return outcome.name.replace(/\s+\S+$/, '');
  }

  /**
   * Update outcome
   * @param {Object} delta - LiveServe update
   * @param eventsReferences - could be NOT an array!
   * @param updateData
   * @param {function} callbackFn - Function to execute
   */
  private updateOutcomePrice(delta: IDelta, eventsReferences: IEventData[], updateData: ILiveServeUpd, callbackFn: Function): void {
    _.each(eventsReferences, (ref: { reference: IReference }) => {
      _.each(ref.reference.markets, (market: IMarket) => {
        const outcome = _.findWhere(market.outcomes, { id: updateData.subject_number.toString() });
        if (outcome) {
          callbackFn.call(this, delta, outcome);
          this.pubSubService.publishSync(this.pubSubService.API.OUTCOME_UPDATED, market);
        }
      });
    });
  }
}
