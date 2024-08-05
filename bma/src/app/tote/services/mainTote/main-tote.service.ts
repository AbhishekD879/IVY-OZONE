import { from as observableFrom, of as observableOf, Observable, throwError, of } from 'rxjs';
import { catchError, map, mergeMap, switchMap } from 'rxjs/operators';
import { IToteEvents } from './../../models/tote-event.model';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { TimeService } from '@core/services/time/time.service';
import { TemplateService } from '@shared/services/template/template.service';
import { SiteServerPoolService } from '@ss/services/site-server-pool.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { TOTE_CONFIG } from '../../tote.constant';
import { LIVE_STREAM_CONFIG } from '@app/sb/sb.constant';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { SiteServerEventToOutcomeService } from '@app/ss/services/site-server-event-to-outcome.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ILiveStreamConfigObject } from '@sb/services/liveStream/live-stream.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRaceGridMeetingTote } from '@core/models/race-grid-meeting.model';
import { IToteOutcome } from '../../models/tote-outcome.model';
import { IMarket } from '@core/models/market.model';
import { IPoolModel } from '@shared/models/pool.model';
import { IToteEventTab } from '@app/tote/models/tote-event-tab.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { IToteEvent } from '@app/tote/models/tote-event.model';
import { ISystemConfig } from '@core/services/cms/models';
import { UK_TOTE_CONFIG } from '@uktote/constants/uk-tote-config.contant';

@Injectable({
  providedIn: 'root'
})
export class ToteService {
  liveStreamConfig: ILiveStreamConfigObject[];
  private TOTE_CATEGORY_ID: string;

  constructor(
    private timeService: TimeService,
    private cacheEventsService: CacheEventsService,
    private templateService: TemplateService,
    private siteServerPoolService: SiteServerPoolService,
    private liveStreamService: LiveStreamService,
    private pubSubService: PubSubService,
    private channelService: ChannelService,
    private isPropertyAvailableService: IsPropertyAvailableService,
    private siteServerEventToOutcomeService: SiteServerEventToOutcomeService,
    private siteServerService: SiteServerService,
    private cmsService: CmsService,
    private routingHelperService: RoutingHelperService
  ) {
    this.TOTE_CATEGORY_ID = environment.TOTE_CATEGORY_ID;
    this.liveStreamConfig = _.filter([...LIVE_STREAM_CONFIG, ...TOTE_CONFIG.LIVE_STREAM_CONFIG],
      provider => _.contains(TOTE_CONFIG.SUPPORTED_LIVE_STREAMS, provider.type));

    this.getToteEvent = this.getToteEvent.bind(this);
  }


  /**
   * Adds events to cache - wrapper
   *
   * @param loaderFn
   * @param cacheName
   * @param cacheArgs
   * @returns {Function}
   */
  cachedEvents(loaderFn: Function, cacheName: string, ...cacheArgs): Function {
    return (params: ISSRequestParamsModel) => {
      const stored = this.cacheEventsService.stored(cacheName, ...cacheArgs);

      return stored ? this.cacheEventsService.async(stored, false) : loaderFn(params)
        .pipe(map((events: IToteEvent[]) => {
          return this.cacheEventsService.store(cacheName, ...cacheArgs, events);
        }));
    };
  }

  /**
   * subscribe for updates from events for EDP page via liveServe PUSH updates (iFrame)!
   * @param {object} event
   */
  subscribeEDPForUpdates(event: ISportEvent): void {
    const channel = this.channelService.getLSChannels(event);

    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'edp'
    });
  }

  /**
   * UnSubscribe EDP page for updates via liveServe PUSH updates (iFrame)!
   */
  unSubscribeEDPForUpdates(): void {
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'edp');
  }

  /**
   * group events by meeting
   *
   * @param eventsArray
   * @returns {{}}
   */
  eventsByMeeting(eventsArray: ISportEvent[]): IRaceGridMeetingTote[] {
    const meetings = {};
    eventsArray.forEach((event: ISportEvent) => {
      if (!meetings[event.typeName]) {
        meetings[event.typeName] = {
          name: event.typeName,
          typeDisplayOrder: event.typeDisplayOrder,
          events: []
        };
      }

      meetings[event.typeName].events.push(event);
    });
    return _.toArray(meetings);
  }

  /**
   * Filter groups where all events from this group are resulted
   *
   * @param meetingsArray
   */
  filterResultedMeetings(meetingsArray: IRaceGridMeetingTote[]): IRaceGridMeetingTote[] {
    return meetingsArray.filter(m => !m.events.every(e => e.isResulted === true
    ));
  }

  /**
   * addLiveStreamAvailability To Meetings
   * @param meetingsArray
   */
  addLiveStreamAvailabilityToMeetings(meetingsArray: IRaceGridMeetingTote[]): void {
    const lSConditionChecker = _.partial(this.liveStreamService.checkCondition, this.liveStreamConfig),
      lSEventInMeeting = this.isPropertyAvailableService.isPropertyAvailable(lSConditionChecker);
    meetingsArray.forEach(meeting => {
      meeting.liveStreamAvailable = lSEventInMeeting(meeting.events);
      _.each(meeting.events, _.partial(this.liveStreamService.addLiveStreamAvailability, this.liveStreamConfig));
    });
  }

  /**
   * add Race Names property to event
   *
   * @param eventsArray
   * @returns {Array|*}
   */
   addRaceNames(eventsArray: ISportEvent[]): IRaceGridMeetingTote[] {
    return eventsArray.map((event: ISportEvent) => {
      return _.extend(event, { raceName: `${event.localTime} ${event.typeName}` });
    });
  }

  /**
   * arranging Events by meetings and events
   *
   * @param eventsArray
   */
  arrangeEvents(eventsArray) {
    const filteredEvents = this.eventsByMeeting(this.templateService.filterEventsWithoutMarketsAndOutcomes(eventsArray)),
      eventsByTime = eventsArray.filter(e => e.isStarted !== 'true'),
      meetings = this.filterResultedMeetings(filteredEvents);

    this.addLiveStreamAvailabilityToMeetings(meetings);

    return {
      meetings,
      events: eventsByTime
    };
  }

  /**
   * returns pools that contains marketId
   * @param marketId
   * @param pools
   * @returns {*}
   */
  poolsForMarket(marketId, pools): IPoolModel[] {
    return pools.filter((pool: IPoolModel) => pool.marketIds.indexOf(marketId) > -1);
  }

  /**
   * Ordering Pools
   *
   * @param {Array} pools
   * @param {Array} poolTypeOrder
   * @returns {Array}
   */
  filterByPoolTypeOrder(pools, poolTypeOrder): IPoolModel[] {
    // make object
    const poolsObj = pools.reduce((obj, val) => {
      obj[val] = val;
      return obj;
    }, {});
    // order and return array with values of object
    return poolTypeOrder
      ? _.values(_.pick(poolsObj, poolTypeOrder))
      : pools;
  }

  /**
   * Adds 'nonRunner' property to non-runner outcomes
   * @param {Array} events
   * @returns {Array}
   */
  addNonRunners(events): IToteEvent[] {
    _.each(events, (event: IToteEvent) => {
      _.each(event.markets, (market: IMarket) => {
        _.each(market.outcomes, (outcome: IToteOutcome) => {
          if (outcome.name.search(/N\/R$/) !== -1) {
            outcome.nonRunner = true;
          }
        });
      });
    });
    return events;
  }

  /**
   * returns event with polls in it
   * @returns {Object}
   * @param poolsArray
   * @param eventsArray
   */
  addPoolsToEvents(poolsArray, eventsArray): IToteEvent[] {
    return eventsArray.map(event => {
      const pools = this.poolsForMarket(event.markets[0].id, poolsArray);
      const poolsTypes = pools.map(p => p.type);
      const poolsTypesOrdered = this.filterByPoolTypeOrder(poolsTypes, TOTE_CONFIG.POOLS_TYPE_ORDER);
      const defaultPoolType = this.setDefPoolType(poolsTypesOrdered);
      return _.extend({}, event, { pools, defaultPoolType, poolsTypesOrdered });
    }, this);
  }

  /**
   * Set default pool type
   * @param {Array} poolsTypes
   * @return {String}
   */
  // TODO: Temporary solutions, in future this function should be removed or changed,
  // TODO: currently we are working only with such types: 'WN', 'SH', 'PL'
  setDefPoolType(poolsTypes) {
    switch (true) {
      case _.contains(poolsTypes, TOTE_CONFIG.DEFAULT_POOL_TYPE):
        return TOTE_CONFIG.DEFAULT_POOL_TYPE;
      case _.contains(poolsTypes, 'PL'):
        return 'PL';
      case _.contains(poolsTypes, 'SH'):
        return 'SH';
      default:
        return undefined;
    }
  }

  /**
   * returns pools with guide values
   * @param {Object} params
   * @returns {Promise.<T>}
   */
  getGuidesData(params): Promise<any> {
    return this.siteServerPoolService.getPoolToPoolValue(params);
  }

  /**
   * returns events that belong to international totes class (horse racing, greyhounds, trotting)
   *
   * @returns {Observable}
   */
  getToteEvents(classesIds): Observable<IToteEvents> {
    const method = classesIds
        ? this.siteServerPoolService.getPoolsForClass.bind(this.siteServerPoolService)
        : this.siteServerPoolService.getPools.bind(this.siteServerPoolService),
      config = classesIds ? _.extend(TOTE_CONFIG.poolsReqConfig, { classIds: [classesIds] }) : TOTE_CONFIG.poolsReqConfig,
      loader = poolsConf => method(poolsConf).pipe(
        mergeMap((pools: IPoolModel[]) => {
          const timeRange = this.setTimeRange(),
            marketIds = pools.reduce((arr, curr) => arr.concat(curr.marketIds), []),
            eventsConf = _.extend({}, timeRange, TOTE_CONFIG.eventsReqConfig, { marketIds });
          return !eventsConf.marketIds.length ? observableOf([])
            : this.siteServerEventToOutcomeService.getEventToOutcomeForMarket(eventsConf).pipe(
              map((eventsArray: IToteEvent[]) => {
                const eventsWithPools = this.addPoolsToEvents(pools, eventsArray),
                  eventsWithLiveStream = this.liveStreamService.addLiveStreamAvailability(this.liveStreamConfig)(eventsWithPools),
                  eventWithRaceNames = this.addRaceNames(eventsWithLiveStream);
                return this.arrangeEvents(eventWithRaceNames);
              }));
        }),
        catchError(err => {
          console.warn('Error while getting getToteEvents from SS (toteFactory.getToteEvents)', err);
          return throwError(err);
        }));

    return this.cachedEvents(loader, 'toteEvents')(config);
  }

  /**
   * Set time range for tote events request
   */
  setTimeRange() {
    return TOTE_CONFIG.eventsReqConfig.timeRange
      ? this.timeService.getRacingTimeRangeForRequest(TOTE_CONFIG.eventsReqConfig.timeRange)
      : {};
  }

  /**
   * returns event that belongs to tote with event pools and racingForm decorations
   *
   * @param eventId
   * @returns {Promise.<T>}
   */
  getToteEvent(eventId): Promise<any> {
    const loader = poolsConfig => this.siteServerPoolService.getPoolsForEvent(poolsConfig).pipe(
      mergeMap(pools => {
        const marketIds = pools.reduce((arr, curr) => arr.concat(curr.marketIds), []);
        const eventConfig = _.extend({}, TOTE_CONFIG.eventReqConfig,
          { marketIds, eventIdEquals: poolsConfig.eventsIds.toString() }
        );
        return this.siteServerEventToOutcomeService.getEventToOutcomeForMarket(eventConfig).pipe(
          map((eventsArray) => {
            const eventsWithLiveStream = this.liveStreamService.addLiveStreamAvailability(this.liveStreamConfig)(eventsArray),
              eventsWithPools = this.addPoolsToEvents(pools, eventsWithLiveStream);
            return this.addNonRunners(eventsWithPools);
          }));
      }),
      catchError(err => {
        console.warn('Error while getting getToteEvent from SS (toteFactory.getToteEvent)', err);
        return throwError(err);
      }));

    return this.cachedEvents(loader, 'event', eventId)({ eventsIds: [eventId] });
  }

  /**
   * Return data for time tote event tabs
   * @param {Array} meeting
   * @return {Array}
   */
  getEventsTabsDataByMeeting(meeting: IRaceGridMeetingTote): IToteEventTab[] {
    return meeting.events.map(event => ({
      categoryId: event.categoryId,
      id: event.id,
      label: this.timeService.formatHours(event.localTime),
      url: `/tote/event/${event.id}`,
      isStarted: event.isStarted || false,
      isResulted: event.isResulted || false,
      markets: event.markets
    }));
  }

  /**
   * Return data for pools tote tabs
   * @param {Array} eventData
   * @return {Array}
   */
  getPoolTabsData(eventData: IToteEvent): IPoolModel[] {
    return eventData.pools.map(pool => ({
      id: pool.type,
      label: `tt.${pool.type}`,
      url: `/tote/event/${eventData.id}`
    }));
  }

  /**
   * Mocked service for results tab - temporary
   * @returns {$routeSegmentProvider|*}
   */
  getToteResults() {
    return this.resultsByClasses(_.extend(TOTE_CONFIG.RESULT_REQUEST, { categoryId: this.TOTE_CATEGORY_ID })).pipe(
      map((data) => {
        return this.prepareEventsObj(data);
      }));
  }

  /**
   * [prepareEventsObj description]
   * @param  {[type]} data [description]
   * @return {[type]}      [description]
   */
  prepareEventsObj(data) {
    const eventsByTypeName = this.templateService.groupEventsByTypeName(data, true);
    return {
      events: data,
      eventsByTypeName,
      typeNamesArray: _.keys(eventsByTypeName)
    };
  }

  /**
   * get events with results By Classes
   * @param requestData
   * @returns {*}
   */
  resultsByClasses(requestData): Observable<ISportEvent[]> {
    return observableFrom(this.siteServerService.getResultsByClasses(requestData)).pipe(
      catchError(err => {
        console.warn('Error while getting resultsByClasses from SS (eventFactory.resultsByClasses)', err);
        return throwError(err);
      }));
  }

  /**
   * Returns Collapsed Summaries array. Array index means market index, array value - Object with
   * outcomes indexes property with expanded/collapsed boolean value
   * @param expandedSummary
   * @returns {Array|*}
   */
  collapsedSummaries() {
    return {};
  }

  /**
   * Get active pool data based on active filter
   *
   * @param  {object} event current event object
   * @return {object}       object with active pool data
   */
  getPoolStakes(event, activeFilter = 'WN'): IPoolModel | any {
    const poolStake = event.pools.filter((item: IPoolModel) => {
      return item.poolType === activeFilter;
    });
    return poolStake.length ? _.clone(poolStake[0]) : undefined;
  }

  getRawToteEvents(classId: number): Observable<ISportEvent[]> {
    return observableFrom(
      this.siteServerService.getRawEventsByClasses({ classIds: [classId], externalKeysEvent: true }));
  }

  getEventById(eventId: number): Observable<ISportEvent> {
    return observableFrom(
      this.siteServerService.getEventByEventId(eventId));
  }

  /***
   * Prepare redirection link for tote events:
   *  to TOTEPOOL tab of HR EDP page in case if OpenBet event is not resulted,
   *  or to results page if event is resulted,
   *  or to international tote event page in case of switcher toggled off
   *
   * @param obEventId
   * @param toteEventId
   * @param isUkToteEvent
   */
  getToteLink(obEventId, toteEventId, isUkToteEvent): Observable<string> {
    if (!obEventId && !toteEventId) {
      return of(``);
    }

    const isToteRedirectsToEdp$ = isUkToteEvent
      ? of(true)
      : this.cmsService.getSystemConfig()
        .pipe(map((config: ISystemConfig) => {
          return config.InternationalTotePool
            && config.InternationalTotePool.Enable_International_Totepools
            && config.InternationalTotePool.Enable_International_Totepools_On_RaceCard;
        }));

    return isToteRedirectsToEdp$.pipe(switchMap((redirectToEdp: boolean) => {
      if (redirectToEdp && obEventId) {
        return this.getEventById(+obEventId)
          .pipe(map(obEvent => {
            if (!obEvent) {
              return '';
            }

            const edpUrl = this.routingHelperService.formResultedEdpUrl(obEvent);

            return obEvent.isResulted ? edpUrl : `${ edpUrl }/${ UK_TOTE_CONFIG.marketPath }`;
          }));
      } else {
        return of(toteEventId ? `/tote/event/${ toteEventId }` : ``);
      }
    }));
  }

  /**
   * To filter racing group based on today date
   * @param {IToteEvent[]} racing
   * @returns {IToteEvent[]}
   */
  filterToteGroup(racing: IToteEvent[]): IToteEvent[] {
    if (racing && racing.length) {
      return racing.filter((race: ISportEvent) => {
        const today = new Date();
        const todayTime = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0, 0).getTime();
        const eventDate = new Date(race.startTime);
        const eventTime = new Date(eventDate.getUTCFullYear(),
        eventDate.getUTCMonth(), eventDate.getUTCDate(),
        eventDate.getUTCHours(), eventDate.getUTCMinutes(), eventDate.getUTCSeconds(),
        eventDate.getUTCMilliseconds()).getTime();
        if (eventTime >= todayTime) {
          return race;
        }
      });
    }
    return racing;
  }
}
