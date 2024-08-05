import { SlicePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import { Observable, of, from } from 'rxjs';

import { EventsByClassesService } from '@sb/services/eventsByClasses/events-by-classes.service';
import { EventFiltersService } from '@sb/services/eventFilters/event-filters.service';
import { ICategory } from '@core/models/category.model';
import { IFilterParam } from '@core/models/filter-param.model';
import { IResultedEventEntity } from '@core/models/resulted-event-entity.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { TimeService } from '@core/services/time/time.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import environment from '@environment/oxygenEnvConfig';
import * as _ from 'underscore';
import { IClassModel } from '@core/models/class.model';
import { IPool } from '@core/models/pool.model';
import { ICompetitionType } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { ISsGetEventsByTypeResponseItemModel } from '@core/models/ss-get-events-by-type-response.model';
import { IRacingResultedEventResponse } from '@core/models/racing-result-response.model';
import { concatMap, map } from 'rxjs/operators';
import { ISSResponseEntity } from '@core/models/ss-response-entity.model';


@Injectable()
export class SiteServerService {

  private readonly categories;
  private readonly outrights;
  private racingFormOutcomeArray;
  private simpleFiltersBank;
  public outcomeForOutcomeData=[];
  public isValidFzSelection: boolean = false;
  constructor(
    private ssRequestHelper: SiteServerRequestHelperService,
    private simpleFilters: SimpleFiltersService,
    private buildUtility: BuildUtilityService,
    private loadByPortions: LoadByPortionsService,
    private ssUtility: SiteServerUtilityService,
    private time: TimeService,
    private filter: FiltersService,
    private eventFilters: EventFiltersService,
    private slicePipe: SlicePipe,
    private eventsByClasses: EventsByClassesService
  ) {
    this.categories = environment.CATEGORIES_DATA;
    this.outrights = OUTRIGHTS_CONFIG;
    this.simpleFiltersBank = this.simpleFilters.simpleFiltersBank;
    this.outcomeForOutcomeData = [];
    /**
     * Context bindings
     * It's needed here because context losses in such functions, like "_.partial(Fn1, Fn2, ...)"
     */
    this.loadEventsWithMarketCounts = this.loadEventsWithMarketCounts.bind(this);
    this.loadEventsWithOutMarketCounts = this.loadEventsWithOutMarketCounts.bind(this);
    this.filterGamingEvents = this.filterGamingEvents.bind(this);
    this.loadResultedEvents = this.loadResultedEvents.bind(this);
    this.getResultedPricesByOutcomeIdFromResultedEvents = this.getResultedPricesByOutcomeIdFromResultedEvents.bind(this);
    this.addResultedPricesToEvents = this.addResultedPricesToEvents.bind(this);
    this.loadScoresAndClock = this.loadScoresAndClock.bind(this);
    this.getExtraPlaceMarkets = this.getExtraPlaceMarkets.bind(this);
  }

  /**
   * getEventByEventId()
   * @param {number} eventId
   * @returns {Promise<ISportEvent>}
   */
  getEventByEventId(eventId: number): Promise<ISportEvent> {
    return this.ssRequestHelper.getEvent({ eventId })
      .then(response => {
        const events: Array<any> = this.ssUtility.stripResponse(response);

        return !!events.length
          && this.buildUtility.eventBuilder(events[0]);
      });
  }

  /**
   * getEventsByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getEventsByClasses(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    if (params.classIds.length > 0) {
      return this.loadEventsWithOutMarketCounts(data => this.ssRequestHelper.getEventsByClasses(data, params.childCount), params,
        this.simpleFiltersBank.eventsByClasses, 'classIds', params.classIds
      ).then(data => this.buildUtility.buildEventsWithOutMarketCounts(data));
    }

    return Promise.resolve([]);
  }

  /**
   * getEventsByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Observable<ISportEvent[]>}
   */
  getEventsByClass(params: ISSRequestParamsModel): Observable<ISportEvent[]> {
    const reqParams = { classIds: params.classIds , simpleFilters: this.simpleFilters.genFilters(params) };
    return from(this.ssRequestHelper.getEventsByClasses(reqParams, false)).pipe(
      map((data: ISSResponseEntity) => this.ssUtility.stripResponse(data)),
      concatMap((data: ISportEventEntity[]) => of(this.buildUtility.buildEventsWithOutMarketCounts(data)))
    );
  }

  /**
   * getEventsByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getRawEventsByClasses(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    if (params.classIds.length > 0) {
      return this.loadEventsByClasses(data => this.ssRequestHelper.getEventForClass(data), params,
        this.simpleFiltersBank.eventsByClassesRaw, params.classIds
      )
      .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
      .then(data => _.map(data, (elm: ISportEventEntity) => this.buildUtility.eventBuilder(elm)));
    }

    return Promise.resolve([]);
  }

  /**
   * getEventsList()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEventEntity[]>}
   */
  getEventsList(params: ISSRequestParamsModel): Promise<ISportEventEntity[]> {
    const filters = _.extend({}, _.pick(params, this.simpleFiltersBank.eventsList));

    return this.ssRequestHelper
      .getEventsList({ simpleFilters: this.simpleFilters.genFilters(filters) })
      .then(data => this.ssUtility.stripResponse(data));
  }

  /**
   * getLiveEventsByEvents()
   * @param {ISSRequestParamsModel} params
   * @param {boolean} marketsLevelOnly
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getLiveEventsByEvents(params: ISSRequestParamsModel, marketsLevelOnly: boolean): Promise<ISportEvent[]>|Promise<any[]> {
    if (marketsLevelOnly) {
      this.simpleFiltersBank.liveEventsByEvents.push('limitOutcomesCount');
      params.limitOutcomesCount = 1;
    }

    if (params.eventsIds.length > 0) {
      return this
        .loadEventsWithOutMarketCounts(
          data => this.ssRequestHelper.getEventsByEvents(data), params,
          this.simpleFiltersBank.liveEventsByEvents, 'eventsIds', params.eventsIds
        )
        .then(data => this.buildUtility.buildEventsWithOutMarketCounts(data));
    }

    return Promise.resolve([]);
  }

  /**
   * getLiveOutrightEventsByEvents()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getLiveOutrightEventsByEvents(params: ISSRequestParamsModel): Promise<ISportEvent[]>|Promise<any[]> {
    if (params.eventsIds.length > 0) {
      return this
        .loadEventsWithOutMarketCounts(
          data => this.ssRequestHelper.getEventByIds(data), params,
          this.simpleFiltersBank.liveOutrightEventsByEvents, 'eventsIds', params.eventsIds
        )
        .then(data => this.buildUtility.buildEventsWithOutMarketCounts(data));
    }

    return Promise.resolve([]);
  }

  /**
   * getEventsByEventsIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getEventsByEventsIds(params: ISSRequestParamsModel): Promise<ISportEvent[]> | Promise<any[]> | any {
    const builder = params.marketsCount || params.childCount ?
                      this.buildUtility.buildEventsWithMarketCounts : this.buildUtility.buildEventsWithOutMarketCounts;
    const loader = params.marketsCount ? this.loadEventsWithMarketCounts : this.loadEventsWithOutMarketCounts;

    if (params.eventsIds.length > 0) {
      return loader(
        data => this.ssRequestHelper.getEventsByEvents(data, params.childCount),
        params,
        this.simpleFiltersBank.eventsByEventsIds,
        'eventsIds',
        params.eventsIds
      ).then(data => builder(data));
    }

    return Promise.resolve([]);
  }

  /**
   * getEventsByOutcomeIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
  getEventsByOutcomeIds(params: ISSRequestParamsModel, skipCache: boolean = false): Promise<ISportEvent[]> {
    if (this.isValidFzSelection) {
      this.ssRequestHelper.isValidFzSelection = true
    }
    const defaultFilters = {
      suspendAtTime: this.time.getSuspendAtTime(skipCache)
    };

    if (params.outcomesIds.length > 0) {
      const simpleParams = _.extend(defaultFilters, _.omit(params, 'outcomesIds')),
        builder = params.racingFormOutcome ? this.buildUtility.buildEventsWithRacingForm : this.buildUtility.buildEventsWithOutMarketCounts;

      return this.loadByPortions
        .get(data => this.ssRequestHelper.getEventsByOutcomes(data),
          this.simpleFilters.getFilterParams(simpleParams, this.simpleFiltersBank.eventsByOutcomeIds),
          'outcomesIds', <number[]>params.outcomesIds
        )
        .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
        .then(data => {
          this.outcomeForOutcomeData = data;        
          if (data && data.length) {
            return builder(data);
          }
          throw new Error('no events');
        });
    }

    return Promise.resolve([]);
  }

  /**
   * getNextEventsByType()
   * @param {IFilterParam} params
   * @returns {ISportEvent[]}
   */
  getNextEventsByType(params: IFilterParam): Promise<ISportEvent[]> {
    const eventFiltersParams = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.nextEventsByType),
      typeIds = _.isArray(params.typeId) ? (params.typeId).join(',') : params.typeId,
      eventsCount = params.eventsCount,
      extendedParams = _.extend({}, eventFiltersParams, {
        typeId: typeIds,
        count: params.siteServerEventsCount
      });

    return this.ssUtility
      .queryService(data => this.ssRequestHelper.getNextEventsByType(data), extendedParams)
      .then(data => this.buildUtility.buildEventsWithRacingForm(data))
      .then(this.eventFilters.applyFilters(['hasOutcomes']))
      .then(events => this.slicePipe.transform(events, 0, eventsCount));
  }

  /**
   * getEventsByTypeWithMarketCounts()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEvent[]> | Promise<any[]>}
   */
   getEventsByTypeWithMarketCounts(params: IFilterParam): Promise<ISportEvent[] | any[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.eventsByTypeWithMarketCounts),
      countFilters = this.simpleFilters.getFilterParams(params, _.without(this.simpleFiltersBank.eventsByTypeWithMarketCounts,
        'dispSortName', 'marketTemplateMarketNameIntersects', 'templateMarketNameOnlyIntersects'), true),
      typeIds = _.isArray(params.typeId) ? (params.typeId).join(',') : params.typeId,
      extendedParams = _.extend({}, eventFiltersData, { typeId: typeIds, childCount: params.childCount });

    const loadCounts = eventsArray => {
      const ids = params.childCount ? [] : eventsArray.map(eventEntity => eventEntity.event.id);
      return ids.length ?
        Promise.all([
          this.loadByPortions.get(
            data => this.ssRequestHelper.getMarketsCountByEventsIds(data), _.extend({}, countFilters), 'eventsIds', ids)
        ]) :
        Promise.all([]);
    };

    const loader = (serviceName, loaderParams) => {
      return this.ssUtility
        .queryService(data => serviceName(data), loaderParams)
        .then(eventsData => this.prepareCounts(loadCounts, eventsData));
    };

    return loader(data => this.ssRequestHelper.getOutrightsByTypeIds(data), extendedParams)
      .then(data => this.buildUtility.buildEventsWithMarketCounts(data))
      .then(this.loadScoresAndClock);
  }

  /**
   * getEventsByTypeId()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByTypeId(params: IFilterParam): Promise<ISportEvent[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.eventsByTypeId),
      typeIds = _.isArray(params.typeId) ? (params.typeId).join(',') : params.typeId,
      extendedParams = _.extend({}, eventFiltersData, { typeId: typeIds, count: params.siteServerEventsCount });

    return this.ssUtility
      .queryService(data => this.ssRequestHelper.getOutrightsByTypeIds(data), extendedParams)
      .then(data => this.buildUtility.buildEventsWithOutMarketCounts(data));
  }

  /**
   * getEventsByType()
   * @param {number} typeId
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByType(typeId: number): Promise<ISsGetEventsByTypeResponseItemModel[]> {
    return this.ssUtility
      .queryService(data => this.ssRequestHelper.getEventsByType(data), { typeId });
  }

  /**
   * getEventsByCategory()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByCategory(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    const builder = (params.marketsCount || params.childCount) ?
      this.buildUtility.buildEventsWithMarketCounts :
      this.buildUtility.buildEventsWithOutMarketCounts,
      loader = params.marketsCount ? this.loadEventsWithMarketCounts : this.loadEventsWithOutMarketCounts,
      loadEvents = _.partial(
        loader,
        this.ssRequestHelper.getEventsByClasses,
        params,
        this.simpleFiltersBank.eventsByCategory,
        'classIds'
      ),
      filterGaming = _.partial(this.filterGamingEvents, (params.categoryId as any), this.ssUtility.filterEventsWithPrices);

    return this.eventsByClasses
      .getClasses(params.categoryId, params.siteChannels)
      .then(data => loadEvents(data))
      .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
      .then(data => builder(data))
      .then(data => filterGaming(data));
  }

  /**
   * getEventsToMarketsByEvents()
   * @param {number[]} eventsIds
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsToMarketsByEvents(eventsIds: number[]): Promise<ISportEvent[]> {
    return this.loadByPortions
      .get(data => this.ssRequestHelper.getEventToMarketForEvent(data), {}, 'eventsIds', eventsIds)
      .then(data => this.buildUtility.buildEvents(data));
  }

  /**
   * loadScoresAndClock()
   * @param {ISportEvent[]} events
   * @returns {Promise<ISportEvent[]>}
   */
  loadScoresAndClock(events: ISportEvent[]): Promise<ISportEvent[]> {
    const eventsIds = events.filter(eventEntity => {
        return eventEntity.markets[0] &&
          _.has(eventEntity.markets[0], 'isMarketBetInRun') &&
          _.has(eventEntity, 'isStarted');
      }).map(eventEntity => {
        return eventEntity.id;
      }),
      eventsWithScoresAndClock = this
        .getCommentsByEvents(eventsIds)
        /* eslint-disable */
        .then(result => ({ events, comments: result }))
        /* eslint-enable */
        .then(data => this.buildUtility.buildEventsWithScoresAndClock(data));

    return Promise.resolve(eventsWithScoresAndClock);
  }

  /**
   * getResultsByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getResultsByClasses(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    if (params.isRacing) {
      params.date = params.resultsDay;
    }

    params.marketName = params.resultedMarketName;

    const loadEvents = _.partial(this.loadEventsWithOutMarketCounts, this.ssRequestHelper.getEventsByClasses,
      params, this.simpleFiltersBank.resultsByClasses, 'classIds'),
      addResults = _.partial(this.loadResultedEvents, params),
      filterGaming = _.partial(this.filterGamingEvents, (params.categoryId as any), this.ssUtility.filterEventsWithPrices);

    return this.eventsByClasses
      .getClasses(params.categoryId, params.siteChannels)
      .then(data => loadEvents(data))
      .then(data => this.buildUtility.buildEventsWithRacingForm(data))
      .then(addResults)
      .then(data => filterGaming(data));
  }

  /**
   * getCommentsByEvents()
   * @param {number[]} eventsIds
   * @returns {Promise<{}>}
   */
  getCommentsByEvents(eventsIds: number[]): Promise<{}> {
    return this.loadByPortions
      .get(data => this.ssRequestHelper.getCommentsByEventsIds(data), {}, 'eventsIds', eventsIds)
      .then(result => {
        return _.object(
          _.map(
            _.filter(result, obj => {
              return obj.event.children;
            }), obj => {
              return [obj.event.id, obj.event.children];
            }));
      });
  }

  /**
   * getInPlayEventsByClassesOnlyStream()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getInPlayEventsByClassesOnlyStream(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    const range = this.time.createTimeRange('today'),
      config = {
        startTime: range.startDate,
        endTime: range.endDate,
        eventDrilldownTagNamesContains: 'EVFLAG_BL',
        eventDrilldownTagNamesIntersects: 'EVFLAG_PVM,EVFLAG_IVM,EVFLAG_GVM'
      };

    return this
      .loadInPlayEvents(_.extend(params, config))
      .then(data => this.buildUtility.buildInPlayEventsWithMarketsCount(data))
      .then(e => {
        const events = e.map(z => this.buildUtility.buildEventWithScores([(z as any)]));
        return Promise.all(events).then(x => _.flatten(x));
      })
      .then(this.loadScoresAndClock);
  }

  /**
   * isRacing()
   * @param {string} sportId
   * @returns {boolean}
   */
  isRacing(sportId: string): boolean {
    for (const sport in this.categories.racing) {
      if (this.categories.racing.hasOwnProperty(sport) && this.categories.racing[sport].id === sportId) {
        return true;
      }
    }

    return false;
  }

  /**
   * filterGamingEvents()
   * @param {string} categoryId
   * @param {Function} filterFunction
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  filterGamingEvents(categoryId: string, filterFunction: Function, events: ISportEvent[]): ISportEvent[] {
    if (!this.isRacing(categoryId) && categoryId !== environment.TOTE_CATEGORY_ID) {
      return filterFunction(events);
    }
    return events;
  }

  /**
   * loadEventsWithMarketCounts()
   * @param {Function} loadEventsService
   * @param {IFilterParam} params
   * @param {string[]} filter
   * @param {string} idsPropName
   * @param {number[]} ids
   * @returns {Promise<any[][]>}
   */
  loadEventsWithMarketCounts(
    loadEventsService: Function, params: IFilterParam, filter: string[], idsPropName: string, ids: number[]): Promise<any[][]> {
    const loadCountsService = idsPropName === 'classIds' ?
      this.ssRequestHelper.getMarketsCountByClasses :
      this.ssRequestHelper.getMarketsCountByEventsIds,
      countFilters = this.simpleFilters
        .getFilterParams(params, _.without(filter,
          'dispSortName',
          'marketTemplateMarketNameIntersects',
          'outcomeSiteChannels',
          'includeUndisplayed',
          'existsMarketOutcomeOutcomeMeaningMajorCodeIn',
          'limitToMarketDisplayOrderIsLowest',
          'templateMarketNameOnlyIntersects'), true),
      filters = this.simpleFilters.getFilterParams(params, filter),
      countParams = _.extend({}, countFilters),
      eventParams = _.extend({}, filters, { count: params.siteServerEventsCount }),
      loadEvents = this.loadByPortions.get(data => loadEventsService(data), eventParams, idsPropName, ids),
      loadCounts = this.loadByPortions.get(data => loadCountsService(data), countParams, idsPropName, ids);

    return Promise.all([loadEvents, loadCounts]);
  }

  /**
   * loadEventsWithOutMarketCounts()
   * @param service
   * @param params
   * @param filter
   * @param propName
   * @param ids
   * @returns {Promise<any[]>}
   */
  loadEventsWithOutMarketCounts(service, params, filter, propName, ids) {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, filter);
    return this.loadByPortions.get(data => service(data, params.childCount), eventFiltersData, propName, ids);
  }

  /**
   * loadResultedEvents()
   * @param {IFilterParam} params
   * @param {ISportEvent[]} events
   * @returns {Promise<{}>}
   */
  loadResultedEvents(params: IFilterParam, events: ISportEvent[]) {
    const eventsIds = events.map(eventEntity => eventEntity.id),
      eventFiltersData = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.resultedEvents),
      resultedPricesByOutcomeId = _.partial(this.getResultedPricesByOutcomeIdFromResultedEvents,
        params.resultedPriceTypeCodeToDisplay, params.categoryId),
      resultedPriceToEvent = _.partial(this.addResultedPricesToEvents, events);

    return this.loadByPortions
      .get(data => this.ssRequestHelper.getResultedEventByEvents(data), eventFiltersData, 'eventsIds', eventsIds)
      .then(resultedPricesByOutcomeId)
      .then(resultedPriceToEvent);
  }

  /**
   * loadResultedEvents()
   * @param {IFilterParam} params
   * @param {ISportEvent[]} events
   * @returns {Promise<{}>}
   */
  loadResultsOfEvent(params: IFilterParam, event: IRacingEvent): Promise<IRacingResultedEventResponse[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.resultedEvents);

    return this.loadByPortions
      .get(data => this.ssRequestHelper.getResultedEventByEvents(data), eventFiltersData, 'eventsIds', [ event.id ]);
  }

  /**
   * loadInPlayEvents()
   * @param {ISSRequestParamsModel} params
   * @param {boolean} requestMarketsCount
   * @param {boolean} requestComments
   * @param {boolean} marketsLevelOnly
   * @returns {Promise<{}>}
   */
  loadInPlayEvents(params: ISSRequestParamsModel, requestMarketsCount = true, requestComments = true, marketsLevelOnly = false) {
    if (params.eventsIds) {
      return this.loadInPlayEventsByIds(params, requestMarketsCount, requestComments, marketsLevelOnly);
    }

    return this.getEventsList(params)
      .then(data => this.buildUtility.buildEventsIds(data))
      .then(eventsIds => {
        _.extend(params, { eventsIds });
        return this.loadInPlayEventsByIds(params, requestMarketsCount, requestComments, marketsLevelOnly);
      });
  }

  /**
   * loadInPlayEventsByIds()
   * @param {ISSRequestParamsModel} params
   * @param {boolean} requestMarketsCount
   * @param {boolean} requestComments
   * @param {boolean} marketsLevelOnly
   * @returns {Promise<{}>}
   */
  loadInPlayEventsByIds(params: ISSRequestParamsModel, requestMarketsCount: boolean, requestComments: boolean, marketsLevelOnly: boolean) {
    const commonParams = {
        marketBetInRun: true
      },
      liveNowRequestParams = this.getParams(params, commonParams, {
        isStarted: true
      }),
      liveLaterRequestParams = this.getParams(params, commonParams, {
        isNotStarted: true
      }),
      outrightSpecificLiveNowParams = this.getParams(params, commonParams, {
        eventSortCode: this.outrights.outrightSortCode,
        categoryCode: this.outrights.outrightsSports,
        isStarted: true,
        limitMarketCount: 1
      }),
      outrightLiveNowParams = this.getParams(params, commonParams, {
        eventSortCode: this.outrights.sportSortCode,
        limitMarketCount: 1,
        isStarted: true,
        limitOutcomesCount: 1
      }),
      outrightSpecificLiveLaterParams = this.getParams(params, commonParams, {
        eventSortCode: this.outrights.outrightSortCode,
        categoryCode: this.outrights.outrightsSports,
        isNotStarted: true,
        limitMarketCount: 1
      }),
      outrightLiveLaterParams = this.getParams(params, commonParams, {
        eventSortCode: this.outrights.sportSortCode,
        isNotStarted: true,
        limitMarketCount: 1,
        limitOutcomesCount: 1
      }),
      returnObject = {
        nowEvents: this.getLiveEventsByEvents(liveNowRequestParams, marketsLevelOnly),
        laterEvents: this.getLiveEventsByEvents(liveLaterRequestParams, marketsLevelOnly),
        outrightSpecificNowEvents: this.getLiveOutrightEventsByEvents(outrightSpecificLiveNowParams),
        outrightNowEvents: this.getLiveOutrightEventsByEvents(outrightLiveNowParams),
        outrightSpecificLaterEvents: this.getLiveOutrightEventsByEvents(outrightSpecificLiveLaterParams),
        outrightLaterEvents: this.getLiveOutrightEventsByEvents(outrightLiveLaterParams)
      };

    if (requestMarketsCount) {
      const marketNowCountsRequestParams = _.extend({}, params, { marketBetInRun: true, isStarted: true }),
        marketLaterCountsRequestParams = _.extend({}, params, { isNotStarted: true }),
        loadCount = (service, reqParams) => {
          const countFilters = this.simpleFilters.getFilterParams(reqParams, this.simpleFiltersBank.inPlayEventsByIds, true);
          return this.loadByPortions.get(data => service(data), countFilters, 'eventsIds', reqParams.eventsIds);
        };
      _.extend(returnObject, {
        nowMarkets: loadCount(data => this.ssRequestHelper.getMarketsCountByEventsIds(data), marketNowCountsRequestParams),
        laterMarkets: loadCount(data => this.ssRequestHelper.getMarketsCountByEventsIds(data), marketLaterCountsRequestParams)
      });
    }

    if (requestComments) {
      _.extend(returnObject, { comments: this.getCommentsByEvents(params.eventsIds) });
    }

    return this.filter.objectPromise(returnObject);
  }

  /**
   * getEnhancedMultiplesEvents()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getEnhancedMultiplesEvents(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.getEventsList(params)
      .then(data => this.buildUtility.buildEventsIds(data))
      .then(eventsIds => {
        _.extend(params, { eventsIds });
        return this.getEventsByEventsIds(params);
      });
  }

  /**
   * getResultedPricesByOutcomeIdFromResultedEvents()
   * @param {string} resultedPriceTypeCodeToDisplay
   * @param {string} categoryId
   * @param {IResultedEventEntity[]} resultedEventsArray
   * @returns {Promise<{}>}
   */
  getResultedPricesByOutcomeIdFromResultedEvents(
    resultedPriceTypeCodeToDisplay: string, categoryId: string, resultedEventsArray: IResultedEventEntity[]): Promise<{}> {
    const resultedOutcomesByIds = {};

    _.each(resultedEventsArray, resultedEvent => {
      _.each((resultedEvent as any).resultedEvent.children, resultedMarket => {
        _.each((resultedMarket as any).resultedMarket.children, resultedOutcome => {
          _.each((resultedOutcome as any).resultedOutcome.children, resultedPrice => {
            if (((resultedPrice as any).resultedPrice.priceTypeCode === resultedPriceTypeCodeToDisplay &&
              _.has((resultedPrice as any).resultedPrice, 'priceDec')) || categoryId === environment.TOTE_CATEGORY_ID) {
              resultedOutcomesByIds[(resultedOutcome as any).resultedOutcome.id] = {
                outcomeResultCode: (resultedOutcome as any).resultedOutcome.resultCode,
                priceNum: Number((resultedPrice as any).resultedPrice.priceNum),
                priceDen: Number((resultedPrice as any).resultedPrice.priceDen),
                priceDec: Number((resultedPrice as any).resultedPrice.priceDec).toFixed(2)
              };

              if (_.has((resultedOutcome as any).resultedOutcome, 'position')) {
                resultedOutcomesByIds[(resultedOutcome as any).resultedOutcome.id].outcomePosition =
                  Number((resultedOutcome as any).resultedOutcome.position);
              }
            }
          });
        });
      });
    });

    return Promise.resolve(resultedOutcomesByIds);
  }

  /**
   * addResultedPricesToEvents()
   * @param {ISportEvent[]} events
   * @param {Object} resultedPricesByOutcomeId
   * @returns {ISportEvent[]}
   */
  addResultedPricesToEvents(events: ISportEvent[], resultedPricesByOutcomeId: Object): ISportEvent[] {
    const eventsArray = events;
    _.each(eventsArray, eventEntity => {
      _.each(eventEntity.markets, marketEntity => {
        const outcomesArray = [];
        let outcome;

        _.each(marketEntity.outcomes, outcomeEntity => {
          if (resultedPricesByOutcomeId[outcomeEntity.id] !== undefined) {
            outcome = outcomeEntity;
            outcome.results = resultedPricesByOutcomeId[outcomeEntity.id];
            outcomesArray.push(outcome);
          }
        });

        delete marketEntity.outcomes;

        marketEntity.outcomes = outcomesArray;
      });
    });
    return eventsArray;
  }

  /**
   * Request to get next races events
   * @param params
   */
  getNextEvents(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this
      .loadEventsPartiallyByClasses(data => this.ssRequestHelper.getNextNEventToOutcomeForClass(data), params,
        this.simpleFiltersBank.nextEventsByIds, params.classIds)
      .then((data: ISportEventEntity[]) => {
        if (params.isVirtualRacesEnabled) {
          data = data.filter(eventObj => {
            if(!eventObj.event) 
              return true 
            else 
              return !(eventObj.event.className &&  eventObj.event.className.toLowerCase().includes('- live') && eventObj.event.typeFlagCodes && eventObj.event.typeFlagCodes.toLowerCase().includes('vr'));
          });
          this.racingFormOutcomeArray = data.filter(e => e.racingFormOutcome);
          data.sort(compareByStartTimeFromUTC);
          data = data.filter(e => e.event);
        }
        return data.filter(hasOutcomes)
        .sort(compareByStartTime)
        .slice(0, params.eventsCount);
      })
      .then((eventEntities: ISportEventEntity[]) => this.buildUtility.buildEventsWithRacingForm(eventEntities)).then((eventEntities: ISportEvent[]) => {
        if (params.isVirtualRacesEnabled && this.racingFormOutcomeArray.length) {
          return this.buildUtility.buildEventWithRacingFormOutcomes(eventEntities, this.racingFormOutcomeArray);
        } else return eventEntities
      });

    function hasOutcomes(evEntity: ISportEventEntity): boolean {
      return !!evEntity.event.children && !!evEntity.event.children.length && !!evEntity.event.children[0].market &&
        !!evEntity.event.children[0].market.children && !!evEntity.event.children[0].market.children.length;
    }

    function compareByStartTime(a: ISportEventEntity, b: ISportEventEntity): number {
        return Number(a.event.startTime) - Number(b.event.startTime);
    }

    function compareByStartTimeFromUTC(a: ISportEventEntity, b: ISportEventEntity): number {
            if(a.event && b.event && a.event.startTime && b.event.startTime) {
              const event1_startTime = new Date(a.event.startTime).getTime();
              const event2_startTime = new Date(b.event.startTime).getTime();
              return event1_startTime - event2_startTime;
            }
    }
  }

  /**
   * loadEventsByClasses()
   * @param {Function} service
   * @param {IFilterParam} params
   * @param {string[]} filter
   * @param {number[]} classIds
   * @returns {Promise<ISportEventEntity[]>}
   */
  loadEventsPartiallyByClasses(
    service: Function, params: IFilterParam, filter: string[], classIds: number[]): Promise<ISportEventEntity[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, filter);

    if (params.siteServerEventsCount) {
      eventFiltersData.siteServerEventsCount = params.siteServerEventsCount;
    }

    return this.loadByPortions.get(data => service(data), eventFiltersData, 'classIds', classIds);
  }

  /**
   * Loads events by ids
   * @param {Function} service
   * @param {IFilterParam} params
   * @param {string[]} filter
   * @param {number[]} ids
   */
  loadSpecificEventsByIds(service: Function, params: IFilterParam, filter: string[], ids: number[]): Promise<ISportEventEntity[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, filter);

    return this.loadByPortions.get(data => service(data), eventFiltersData, 'eventsIds', ids);
  }

  /**
   * loadEventsByClasses()
   * @param {Function} service
   * @param {IFilterParam} params
   * @param {string[]} filter
   * @param {number[]} classIds
   * @returns {Promise<ISportEventEntity[]>}
   */
  loadEventsByClasses(service: Function, params: IFilterParam, filter: string[], classIds: number[]): Promise<ISportEventEntity[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, filter),
      eventParams = _.extend({}, eventFiltersData, { count: params.siteServerEventsCount });

    return this.loadByPortions.get(data => service(data), eventParams, 'classIds', classIds);
  }

  /**
   * getCouponsList()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEventEntity[]>}
   */
  getCouponsList(params: IFilterParam): Promise<ISportEventEntity[]> {
    return this.ssRequestHelper
      .getCouponsList({ simpleFilters: this.simpleFilters.genFilters(params) })
      .then(data => this.ssUtility.stripResponse(data));
  }

  /**
   * getCouponEventsByCouponId()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEvent[]>}
   */
  getCouponEventsByCouponId(params: IFilterParam): Promise<ISportEvent[]> {
    const loadedEvents = this.ssRequestHelper.getCouponsByIds({
        couponsIds: params.couponId,
        simpleFilters: this.simpleFilters.genFilters(params)
      })
        .then(data => this.ssUtility.stripResponse(data))
        .then(coupon => coupon[0] && coupon[0].coupon.children);
    return !params.childCount ?
      loadedEvents.then(data => this.buildUtility.buildEvents(data)) :
      loadedEvents.then(data => this.buildUtility.buildCouponEventsWithMarketCounts(data));
  }

  /**
   * getJackpotList()
   * @returns {Promise<ISportEventEntity[]>}
   */
  getJackpotList(): Promise<IPool[]> {
    return this.ssRequestHelper
      .getJackpotPools()
      .then(data => this.ssUtility.stripResponse(data));
  }

  /**
   * getEventsByMarkets()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEvent[]>}
   */
  getEventsByMarkets(params: IFilterParam): Promise<ISportEvent[]> {
    const eventFiltersData = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.eventsByMarkets),
      extendedParams = _.extend({}, eventFiltersData, { marketIds: params.marketIds }),
      builder = params.racingFormOutcome ? this.buildUtility.buildEventsWithRacingForm : this.buildUtility.buildEvents;

    return this.ssUtility
      .queryService(data => this.ssRequestHelper.getEventsByMarkets(data), extendedParams)
      .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
      .then(data => builder(data));
  }

  /**
   * getEvent()
   * @param {string} eventId
   * @param {IFilterParam} filters
   * @param {boolean} isGamingSport
   * @returns {Promise<ISportEvent[]>}
   */
  getEvent(eventId: string | number, filters: IFilterParam, isGamingSport: boolean, isMTASport?: boolean): Promise<ISportEvent[]> {
    let service, builder;

    if (isGamingSport) {
      service = isMTASport ? this.ssRequestHelper.getEventToMarketForEvent : this.ssRequestHelper.getEventByIds;
      builder = filters.scorecast ? this.buildUtility.buildEventsWithScorecasts : this.buildUtility.buildEvents;
    } else {
      service = this.ssRequestHelper.getEventsByEvents;
      builder = this.buildUtility.buildEventsWithRacingForm;
    }

    return this.processResponse(service({ eventsIds: eventId, simpleFilters: this.simpleFilters.genFilters(filters)}), builder);
  }

  getEventByMarkets(marketIds : string[], filters?: IFilterParam): Promise<ISportEvent[]> {
    const service = this.ssRequestHelper.getEventsByMarkets;
    const builder = filters.scorecast ? this.buildUtility.buildEventsWithScorecasts : this.buildUtility.buildEvents;
    return this.processResponse(service({ marketIdArr: marketIds, simpleFilters: this.simpleFilters.genFilters(filters)}), builder);
  }

  private async processResponse(response: Promise<any>, builder: any){
    return response.then(data => this.ssUtility.stripResponse(data))
      .then(data => this.buildUtility.buildEventsWithExternalKeys(data))
      .then(data => builder(data))
      .then(data => this.buildUtility.buildEventWithScores(data));
  }

  /**
   * getCategories()
   * @param {number[]} categoriesIds
   * @returns {Promise<ICategory[]>}
   */
  getCategories(categoriesIds: number[] | string[]): Promise<ICategory[]> {
    const categoriesString = _.isArray(categoriesIds) ? categoriesIds.join(',') : categoriesIds;

    return this.ssRequestHelper
      .getCategories({ categoriesIds: categoriesString })
      .then(result => {
          const categoriesArray = result.SSResponse.children.slice(0, -1);

          return Promise.resolve(categoriesArray.map(categoryEntity => {
            categoryEntity.category.id = Number(categoryEntity.category.id);
            categoryEntity.category.displayOrder = Number(categoryEntity.category.displayOrder);
            return categoryEntity.category;
          }));
        }, error => {
          return Promise.reject(error);
        }
      );
  }

  /**
   * getNamesOfMarketsCollection()
   * @param {number} sportId
   * @returns {string[]}
   */
  getNamesOfMarketsCollection(sportId: number): Promise<any[]> {
    return this.ssRequestHelper
      .getSportToCollection({ simpleFilters: this.simpleFilters.genFilters({ sportId }) })
      .then(data => this.ssUtility.stripResponse(data))
      .then(data => this.filterCollections(data))
      .then(data => this.sortCollection(data));
  }

  /**
   * getClasses()
   * @param {number} catId
   * @param {string} channels
   * @returns {Promise<IClassModel[]>}
   */
  getClasses(catId: string, channels = 'M'): Promise<ICompetitionType[]> {
    return this.ssRequestHelper
      .getClassesByCategory({ siteChannels: channels, categoryId: catId, hasOpenEvent: '&simpleFilter=class.hasOpenEvent' })
      .then(data => this.ssUtility.stripResponse(data));
  }

  /**
   * getTypesByClasses()
   * @param {number[]} classIds
   * @returns {Promise<ISportEventEntity[]>}
   */
  getTypesByClasses(classIds: number[]): Promise<ISportEventEntity[] | IClassModel[]> {
    return this.ssRequestHelper
      .getClassToSubTypeForClass({ classIds, simpleFilter: this.simpleFilters.genFilters(this.simpleFiltersBank.typesByClasses) })
      .then(data => this.ssUtility.stripResponse(data));
  }

  /**
   * Get classes data by type ids
   * @param {array} ids
   * @returns {Promise}
   */
  getClassToSubTypeForTypeByPortions(ids: number[]): Promise<ISportEvent[] | IClassModel[]> {
    return this.loadByPortions.get(this.ssRequestHelper.getClassToSubTypeForType, {}, 'typeIds', ids);
  }

  /**
   * getInPlayEventsWithOutOutcomes()
   * @param {IFilterParam} params
   * @returns {Promise<ISportEvent[]>}
   */
  getInPlayEventsWithOutOutcomes(params: IFilterParam): Promise<ISportEvent[]> {
    const filters = _.extend({}, _.pick(params, this.simpleFiltersBank.inPlayEventsWithOutOutcomes));

    return this.ssRequestHelper
      .getEventsList({ simpleFilters: this.simpleFilters.genFilters(filters) })
      .then(data => this.ssUtility.stripResponse(data))
      .then(data => data.map(eventEntity => eventEntity.event));
  }

  /**
   * getData()
   * @param {number} betLevel
   * @param {number} betIDs
   * @param {boolean} all
   * @returns {Promise<ISportEvent[]>}
   */
  getData(betLevel: string, betIDs: string[], all: boolean): Promise<ISportEvent[]> {
    const serviceAndParam = {
      SELECTION: [this.ssRequestHelper.getEventsByOutcomes.bind(this.ssRequestHelper), 'outcomesIds'],
      MARKET: [this.ssRequestHelper.getEventsByMarkets.bind(this.ssRequestHelper), 'marketIds'],
      EVENT: [this.ssRequestHelper.getEventsByEvents.bind(this.ssRequestHelper), 'eventsIds'],
      TYPE: [this.ssRequestHelper.getClassToSubTypeForType.bind(this.ssRequestHelper), 'typeIds'],
      CLASS: [this.ssRequestHelper.getClasses.bind(this.ssRequestHelper), 'classIds']
    }[betLevel];

    return serviceAndParam[0]({ [serviceAndParam[1]]: betIDs })
      .then(data => {
        data.SSResponse.children.pop();
        return all ? data.SSResponse.children : _.first(data.SSResponse.children);
      });
  }

  /**
   * getExtraPlaceMarkets()
   * @param ids
   * @param params
   * @returns {Promise<ISportEvent[]>}
   */
  getExtraPlaceMarkets(ids: string[] | number[], params: IFilterParam): Promise<ISportEventEntity[]> {
    const countParams = this.simpleFilters.getFilterParams(params, this.simpleFiltersBank.extraPlaceMarkets, false);
    if (params.siteServerEventsCount) {
      countParams.siteServerEventsCount = params.siteServerEventsCount;
    }

    return this.loadByPortions.get(data => this.ssRequestHelper.getNextNEventToOutcomeForClass(data),
      countParams, 'classIds', ids as number[]);
  }

  /**
   * getExtraPlaceEvents()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getExtraPlaceEvents(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.eventsByClasses
      .getClassesByParams(params)
      .then(ids => this.getExtraPlaceMarkets(ids, params))
      .then(data => this.buildUtility.buildEventsWithRacingForm(data));
  }

  /**
   * getRacingSpecialsEvents()
   * @param {number} eventId
   * @param {params} IFilterParam
   * @returns {Promise<ISportEvent>}
   */
  getRacingSpecialsEvents(eventId: number, params: IFilterParam = {priceHistory: true}): Promise<ISportEvent[]> {
    const queryParams = this.simpleFilters.genFilters(params);

    return this.ssRequestHelper.getEventToLinkedOutcomeForEvent(eventId, queryParams)
      .then(data => this.ssUtility.stripResponse(data))
      .then(data => this.buildUtility.buildEvents(data));
  }

  /**
   * getInspiredVirtualEvents()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<ISportEvent[]>}
   */
  getInspiredVirtualEvents(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    return this.getEventsList(params)
      .then(data => this.buildUtility.buildEvents(data));
  }

  /**
   * Private
   */

  /**
   * getParams()
   * @param {ISSRequestParamsModel} params
   * @param {Object} commonParams
   * @param {Object} uniqueParams
   * @returns {ISSRequestParamsModel}
   */
  private getParams(params: ISSRequestParamsModel, commonParams: Object, uniqueParams: Object): ISSRequestParamsModel {
    return _.extend({}, params, commonParams, uniqueParams || {});
  }

  /**
   * filterCollections()
   * @param {any[]} collections
   * @returns {any[]}
   */
  private filterCollections(collections: any[]): any[] {
    if (collections.length) {
      return _.filter(collections[0].sport.children, child => {
        return child.collection.drilldownTagNames
          ? child.collection.drilldownTagNames.search('COLLFLAG_EP,') !== -1
          : false;
      });
    }
    return undefined;
  }

  /**
   * sortCollection()
   * @param {string[]} collections
   * @returns {string[]}
   */
  private sortCollection(collections: any[]): any[] {
    return _.sortBy(_.map(collections, collection => {
      return collection.collection;
    }), 'name');
  }

  private prepareCounts(runFn: Function, eventsData: ISportEvent): Promise<ISportEvent[]> {
    return runFn(eventsData).then(marketsCountData => {
      return [eventsData, marketsCountData[0]];
    });
  }
}
