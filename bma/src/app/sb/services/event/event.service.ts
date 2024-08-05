import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';
import { LiveStreamService } from '../liveStream/live-stream.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { EventsByClassesService } from '../eventsByClasses/events-by-classes.service';
import { LIVE_STREAM_CONFIG } from '@sb/sb.constant';
import { EventFiltersService } from '../eventFilters/event-filters.service';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { IVirtualSports } from '@core/services/cms/models/virtual-sports.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPool, IPoolEntity } from '@core/models/pool.model';
import { IFilterParam } from '@core/models/filter-param.model';
import { IFeaturedModel } from '@featured/models/featured.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { ISportCollectionData } from '@core/models/sport-collection-data.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { CmsService } from '@core/services/cms/cms.service';
import { Subject } from 'rxjs';

@Injectable()
export class EventService {
  eventsByClasses: Function = this.cachedEvents(this.getEventsByClasses.bind(this));
  getNextEvents: Function = this.cachedEvents(this.getNextEventsFn.bind(this));
  eventsByTypeWithMarketCounts: Function = this.cachedEventsByFn(this.getEventsByTypeWithMarketCounts.bind(this), 'currentMatches');
  couponEventsByCouponId: Function = this.cachedCouponEvents(this.getCouponEventsByCouponId.bind(this), 'coupons');
  getNamesOfMarketsCollection: Promise<ISportCollectionData[]>
    = this.siteServerService.getNamesOfMarketsCollection.bind(this.siteServerService);
  isAnyLiveStreamAvailable: Function = this.isPropertyAvailableService.isPropertyAvailable(
    _.partial(this.liveStreamService.checkCondition, LIVE_STREAM_CONFIG));
  isAnyCashoutAvailable: Function = this.isPropertyAvailableService.isPropertyAvailable(
    this.cashOutLabelService.checkCondition.bind(this.cashOutLabelService));
    hrEventSubscription: Subject<boolean> = new Subject<boolean>();
  constructor(
    private cacheEventsService: CacheEventsService,
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private eventFiltersService: EventFiltersService,
    private liveStreamService: LiveStreamService,
    private cashOutLabelService: CashOutLabelService,
    private eventsByClasseService: EventsByClassesService,
    private isPropertyAvailableService: IsPropertyAvailableService,
    private awsService: AWSFirehoseService,
    private cmsService: CmsService
  ) {}

  inPlayEventsOnlyStream(cacheName: string): Function {
    return this.cachedEventsByFn(this.isInPlayEventsOnlyStream.bind(this), cacheName);
  }

  /**
   * Abstract caching wrapper
   * Returns wrapped function that can be used as a method,
   * which either loads the data results then caching,
   * or takes it from the cache if already stored,
   * but in both cases it returns the link to the cached object.
   * @param  {Function} loaderFn loading function
   * @param  loaderFn {Object} params request params
   * @return {Function}        Function empowered with caching
   */
  cachedEvents(loaderFn: Function): Function {
    return (params: ISSRequestParamsModel, cacheLabel: string = 'events', isOverlay?): ISportEvent[] => {

      const store: Function = _.partial(this.cacheEventsService.store, cacheLabel, params.date, params.categoryId),
        stored: IFeaturedModel = this.cacheEventsService.stored(cacheLabel, params.date, params.categoryId);
      return stored && !isOverlay? this.cacheEventsService.async(stored) : loaderFn(params).then((events: ISportEvent[]) => store(events));
    };
  }

  /**
   * wrapper for coupons cache
   * @param loaderFn
   * @param cacheName
   * @returns {Function}
   */
  cachedCouponEvents(loaderFn: Function, cacheName: string): Function {
    return (params: any) => {
      const store: Function = _.partial(this.cacheEventsService.store, cacheName, params.couponId),
        stored: IFeaturedModel = this.cacheEventsService.stored(cacheName, params.couponId);

      return stored ? this.cacheEventsService.async(stored) : loaderFn(params).then((events: ISportEvent[]) => store(events));
    };
  }

  /**
   * Abstract caching wrapper
   * Returns wrapped function that can be used as a method,
   * which either loads the data results then caching,
   * or takes it from the cache if already stored,
   * but in both cases it returns the link to the cached object.
   *
   * Cache id is based on loader function name.
   *
   * @param  {Function} loaderFn loading function
   * @param  {Object} cacheName request params
   * @param  cachedParam {string} cash parameter
   * @return {Function} Function empowered with caching
   */
  cachedEventsByFn(loaderFn: Function, cacheName: string, cachedParam = 'categoryId'): Function {
    return (params?: ISSRequestParamsModel) => {
      const store: Function = params && params[cachedParam]
        ? _.partial(this.cacheEventsService.store, cacheName, params[cachedParam]) : _.partial(this.cacheEventsService.store, cacheName),
        stored: IFeaturedModel = params && params[cachedParam]
          ? this.cacheEventsService.stored(cacheName, params[cachedParam]) : this.cacheEventsService.stored(cacheName);

      return stored ? this.cacheEventsService.async(stored) : loaderFn(params).then((events: ISportEvent[]) => store(events));
    };
  }

  isDataOutdated(eventId: string | number, interval: number): boolean {
    this.cmsService.isEDPLogsEnabled().subscribe((enabled: boolean) => {
      if (enabled) {
        this.awsService.addAction('EventService=>isDataOutdated=>Start', { eventId: eventId });
      }
    });
    if (this.cacheEventsService.storedData && this.cacheEventsService.storedData.event &&
      this.cacheEventsService.storedData.event[eventId]) {
      return (this.timeService.getCurrentTime() - this.cacheEventsService.storedData.event[eventId].updated > interval);
    }
    return true;
  }

  /**
   * Getting event by ID
   *
   * @param {string} eventId
   * @param filters
   * @param isGamingSport
   * @param {boolean} useCache - use cache or reload event
   * @returns {Promise<ISportEvent | any>}
   */
  getEvent(eventId: string | number, filters?: IFilterParam, isGamingSport?: boolean, useCache = true, isMTASport?: boolean, marketIds?: string[]): Promise<ISportEvent | any> {
    if (useCache && this.cacheEventsService.storedData.event.data && this.cacheEventsService.storedData.event.data.length &&
      this.cacheEventsService.storedData.event.data[0].id === Number(eventId)) {
      if(marketIds && marketIds.length > 0){
        return this.siteServerService.getEventByMarkets(marketIds, {scorecast: false})
          .then((result: ISportEvent[]) => {
            if (result && result.length) {
              result[0].markets.forEach(market => {
                if(market.outcomes && market.outcomes.length > 0){
                    this.cacheEventsService.storeNewOutcomes(market.outcomes, true);
                  }
                });
              return Promise.resolve(this.cacheEventsService.storedData.event.data);
            }
          })
          .catch(err => {
            console.error('Error while getting Event from SS (eventService.getEvent)', err);
            return Promise.reject(err);
          });
      }
      return Promise.resolve(this.cacheEventsService.storedData.event.data);
    }

    if (this.isDataOutdated(eventId, this.timeService.apiDataCacheInterval.event)) {
      return this.siteServerService.getEvent(eventId, filters, isGamingSport, isMTASport)
        .then((result: ISportEvent[]) => {
          if (result && result.length) {
            _.extend(result[0], this.liveStreamService.isLiveStreamAvailable(LIVE_STREAM_CONFIG)(result[0]));
            result[0].liveSimAvailable = this.isLiveSimAvailable(result[0]);
            result[0].isUKorIRE = this.isUKorIRE(result[0]);
            const storedEvent = {
              event: {
                data: result,
                updated: this.timeService.getCurrentTime()
              }
            };

            // adding to cache index
            this.cacheEventsService.addToIndex(this.cacheEventsService.storedData, storedEvent);
            // merging with proper cache object
            this.cacheEventsService.storedData.event = storedEvent.event;

            return this.cacheEventsService.storedData.event.data;
          }

          return result;
        })
        .catch(err => {
          console.error('Error while getting Event from SS (eventService.getEvent)', err);
          return Promise.reject(err);
        });
    }

    return Promise.resolve(this.cacheEventsService.storedData.event[eventId].data);
  }

  /**
   * Get commentaries for events based on events!
   *
   * @returns {Promise<ISportEvent[]>}
   * @param params
   */
  favouritesMatches(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    // @ts-ignore
    return this.siteServerService.getEventsByEventsIds(params)
      .then(this.siteServerService.loadScoresAndClock.bind(this.siteServerService))
      .catch(err => {
        console.warn('Error while getting favouritesMatches from SS (eventService.favouritesMatches)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Get events by Classes
   *
   * @param requestData {obj}
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByClasses(requestData: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.siteServerService.getEventsByCategory(requestData)
      .then(data => this.addAvailability(data))
      .catch(err => {
        console.warn('Error while getting eventsByClasses from SS (eventService.eventsByClasses)', err);
        return Promise.reject(err);
      });
  }
  /**
   * Get events by Type id's with market counts
   *
   * @param params {obj}
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByTypeWithMarketCounts(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.siteServerService.getEventsByTypeWithMarketCounts(params)
      .catch(err => {
        console.warn('Error while getting eventsByClasses from SS (eventService.eventsByTypeWithMarketCounts)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Get events by Type id's
   *
   * @param params {obj}
   * @returns {Promise<ISportEvent[]>}
   */
  eventsByTypeIds(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.siteServerService
      .getEventsByTypeId(params)
      .catch(err => {
        console.warn('Error while getting eventsByTypeIds from SS (eventService.eventsByTypeIds)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Get Live(In Play) events by Classes only with live streaming avialiable - using for stream
   *
   * @param requestData {obj}
   * @returns {Promise<ISportEvent[]>}
   */
  isInPlayEventsOnlyStream(requestData: ISSRequestParamsModel): Promise<ISportEvent[] | void> {
    return this.siteServerService.getInPlayEventsByClassesOnlyStream(requestData)
      .then((data: ISportEvent[]) => this.addAvailability(data))
      .catch(err => {
        console.warn('Error while getting inPlayEventsOnlyStream from SS (eventService.inPlayEventsOnlyStream)', err);
      });
  }

  /**
   * get events with results By Classes
   * @param requestData
   * @returns {Promise<ISportEvent[]>}
   */
  resultsByClasses(requestData: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.siteServerService.getResultsByClasses(requestData)
      .catch(err => {
        console.warn('Error while getting resultsByClasses from SS (eventService.resultsByClasses)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Get Next Events
   * @params{object} params object
   * If typeId is set, we call getNextEventsByType service if not -
   * we call getNextEvents service, before calling getNextEvents we
   * get getClasses by categoryId and siteChannels
   * @return {Promise<ISportEvent[]>}
   */
  getNextEventsFn(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    if (params.typeId) {
      return this.siteServerService.getNextEventsByType(params);
    }

    return this.eventsByClasseService
    .getClassesByParams(params)
    .then((classIds: string[]) => {
      if(params.isVirtualRacesEnabled){
        return this.cmsService.getVirtualSportstoPromise()
        .then((data: IVirtualSports[]) => this.filterVirtualClass(data,classIds, params.virtualRacesIncluded))
        .then((data: string[]) => this.getEvents(data, params))
      } else {
        return this.getEvents(classIds, params)
      }
    })
    .then((data: ISportEvent[]) => this.defineHRsilksType(data))
    .catch(err => {
      console.warn('Error while getting getClasses from SS (eventService.getClasses)', err);
      return Promise.reject(err);
    });
  }

  filterVirtualClass(cmsVirtualSports: IVirtualSports[], classIds: string[], virtualRacesIncluded: string[]) : string[] {
    return classIds.concat([].concat(...virtualRacesIncluded.map(data => {
      return cmsVirtualSports.map(obj =>  obj.tracks.filter(t => t.title.toLowerCase() == data.trim().toLowerCase())).filter(arr => arr.length)[0]?.map(t=>t.classId);
    }).filter(Boolean)));
  }
  getFilteredEvents(loader: Function, request: ISSRequestParamsModel, filterNames: string[]): Promise<ISportEvent[]> {
    const applyFilters: Function = this.eventFiltersService.applyFilters(filterNames);

    return loader(request)
      .then(data => applyFilters(data))
      .catch(err => {
        console.error('Error while getting getFilteredEvents from SS (eventService.getFilteredEvents)', err);
      });
  }

  /**
   * Returns list of coupons
   *
   * @param requestData
   * @returns {Promise<ISportEvent[]>}
   */
  couponsList(requestData: ISSRequestParamsModel): Promise<ISportEventEntity[]> {
    return this.siteServerService.getCouponsList(requestData)
      .catch(err => {
        console.warn('Error while getting couponsList from SS (eventService.couponsList)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Returns events that are belongs to particular coupon
   *
   * @param requestData
   * @returns {Promise<ISportEvent[]>}
   */
  getCouponEventsByCouponId(requestData: ISSRequestParamsModel): Promise<ISportEvent[]>  {
    return this.siteServerService.getCouponEventsByCouponId(requestData)
      .catch(err => {
        console.warn('Error while getting couponByCouponId from SS (eventService.couponEventsByCouponId)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Checks whether Specials events are available
   * @param {object} params
   * @return {Promise<boolean>}
   */
  isSpecialsAvailable(params): Promise<boolean> {
    return this.getEventsByClasses(params)
      .then(response => {
        return !_.isEmpty(response);
      })
      .catch(err => {
        console.warn('Error while getting specials events list from SS (eventService.isSpecialsAvailable)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Gets list of pools and retrieves events by market ids of the pool with min id
   * @return {Promise<ISportEvent[] | void | boolean>}
   */
  getFootballJackpotList(): Promise<ISportEvent[] | void | boolean> {
    return this.siteServerService.getJackpotList()
      .then((data: IPool[]) => this.getJackpotListbyMarkets(data))
      .catch(err => {
        console.warn('Error while getting getJackpotList from SS (eventService.getFootballJackpotList)', err);
        return Promise.reject(err);
      });
  }

  getDailyRacingEvents(requestData: ISSRequestParamsModel): Promise<ISportEvent[]> {
    requestData.suspendAtTime = this.timeService.getSuspendAtTime();
    return this.siteServerService.getEventsByClasses(requestData)
      .then((result: ISportEvent[]) => {
        if (!!result) {
          return this.addAvailability(result);
        }
      })
      .catch(err => {
        console.error('Error while getting DailyRacingEvents eventService.getDailyRacingEvents', err);
        return Promise.reject(err);
      });
  }

  /**
   * Add for each event custom field liveStreamAvailable
   *
   * @param results
   * array of events
   * @returns {ISportEvent[]}
   */
  // TODO: extract livestream availability into builder
  addAvailability(results: ISportEvent[]): ISportEvent[] {
    return this.liveStreamService.addLiveStreamAvailability(LIVE_STREAM_CONFIG)(results);
  }

  isLiveStreamAvailable(eventObj: ISportEvent): ISportEvent {
    return this.liveStreamService.isLiveStreamAvailable(LIVE_STREAM_CONFIG)(eventObj);
  }

  /**
   * Check if Live Sim is available.
   *
   * Live Sim should be displayed for all UK&IRE races
   * and only ca. 15 minutes before the scheduled race-off time.
   *
   * @param {object} eventObj Object
   * @returns {boolean}
   */
  isLiveSimAvailable(eventObj: ISportEvent): boolean {
    const now = new Date().getTime(),
      interval = 15 * 60 * 1000,
      inAvailableCountry = this.isUKorIRE(eventObj);

    return now > (Number(eventObj.startTime) - interval) && inAvailableCountry;
  }

  /**
   * Check if event is UK or Ireland event.
   *
   * @param {object} eventObj Object
   * @returns {boolean}
   */
  isUKorIRE(eventObj: ISportEvent): boolean {
    return _.some(['UK', 'IE'], country => {
      return eventObj.typeFlagCodes ? eventObj.typeFlagCodes.indexOf(country) > -1 : false;
    });
  }

  /**
   * Get Live(In Play) events withOUT outcomes by Classes - using for stream
   *
   * @param requestData {obj}
   * @returns {Promise<ISportEvent[]>}
   */
  inPlayEventsWithOutOutcomes(requestData: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.siteServerService.getInPlayEventsWithOutOutcomes(requestData)
      .catch(err => {
        console.warn('Error while getting inPlayEventsWithOutOutcomes from SS (eventService.inPlayEventsWithOutOutcomes)', err);
        return Promise.reject(err);
      });
  }

  /**
   * Returns pool with min id
   * @param data {array}
   * @return {IPool[]}
   */
  private getSortedPools(data: IPool[]): IPool[] {
    return _.sortBy(data, (item: IPool) => Number(item.pool.id));
  }

  /**
   * Retrieves events by market ids
   * @param data {Promise<ISportEvent[] | boolean | void>}
   */
  private getJackpotListbyMarkets(data: IPool[]): Promise<ISportEvent[] | boolean | void>  {
    if (data.length) {
      const index: number = 0,
        sortedPools = this.getSortedPools(data);
      return this.getEventsByMarkets(sortedPools, index);
    }

    return Promise.resolve(false);
  }

  /**
   * Gets events by markets ids from pool
   * @param {array} sortedPools
   * @param {Promise<ISportEvent[] | void | boolean>} index
   */
  private getEventsByMarkets(sortedPools: IPool[], index: number): Promise<ISportEvent[] | void | boolean> {
    const pool: IPoolEntity = sortedPools[index].pool,
      requestParams: ISSRequestParamsModel = {
        isNotStarted: true,
        marketIds: pool.marketIds
      };

    return this.siteServerService.getEventsByMarkets(requestParams)
    // eslint-disable-next-line consistent-return
      .then((result: ISportEvent[])  => {
        if (pool) {
          _.each(result, (event: ISportEvent) => { // Adds pool info to event.
            event.pool = pool;
          });
        }

        if (result.length === 15) { // always should be 15 events for jackpot
          return result;
        } else if (++index < sortedPools.length) { // eslint-disable-line no-param-reassign
          // if for the pool with the lowest id
          // there are less then 15 not started events, try next one
          this.getEventsByMarkets(sortedPools, index);
        } else {
          return false;
        }
      })
      .catch(err => {
        console.error('Error while getting EventsByMarkets from SS (eventService.getEventsByMarkets)', err);
      });
  }

  private getEvents(classIds: string[], params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    const reqParams = _.extend({}, params, { classIds });
    return this.siteServerService.getNextEvents(reqParams)
      .catch(err => {
        console.warn('Error while getting getNextEvents from SS (eventService.getNextEvents)', err);
        return Promise.reject(err);
      });
  }

 /**
  * HR: To define silks type on UK/IRE or International events
  * @param {{}} data: ISportEvent[]
  */
  private defineHRsilksType(data: ISportEvent[]): Promise<ISportEvent[]> {
    data.forEach((el: ISportEvent) => {
      if (el.categoryCode === 'HORSE_RACING') {
        return el.isUKorIRE = this.isUKorIRE(el);
      }
    });
    return Promise.resolve(data);
  }
}
