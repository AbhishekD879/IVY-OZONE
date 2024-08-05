/**
 * TODO: refactoring points:
 *
 * 1. split url to independent pieces (path/params)
 * 2. simpleFilter
 *   make simpleFilter param array only (even if one member),
 *   move to query params (as key-value pair),
 * 3. no manual entering of `&` or `?` dividers (providing params as HttpParams will do the work)
 * 4. remove (unite) dubs (eg getEventToOutcomeForMarket)
 */


import { map, catchError, timeout } from 'rxjs/operators';
import { HttpClient, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import environment from '@environment/oxygenEnvConfig';
import { cache } from '@core/rxjs-operators/cache';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';

@Injectable()
export class SiteServerRequestHelperService {

  private readonly SSEndpoint: string;
  private readonly SSHistoricEndpoint: string;
  private readonly SSCommentaryEndpoint: string;
  private readonly TIMEOUT: number = 60000;
  public isValidFzSelection: boolean = false;

  constructor(
    private http: HttpClient
  ) {
    this.SSEndpoint = environment.SITESERVER_ENDPOINT;
    this.SSHistoricEndpoint = environment.SITESERVER_HISTORIC_ENDPOINT;
    this.SSCommentaryEndpoint = environment.SITESERVER_COMMENTARY_ENDPOINT;
    /**
     * Context bindings
     * It's needed here because context losses in such functions, like "_.partial(Fn1, Fn2, ...)"
     */
    this.getEventsByClasses = this.getEventsByClasses.bind(this);
    this.getEventsByEvents = this.getEventsByEvents.bind(this);
    this.getMarketsCountByClasses = this.getMarketsCountByClasses.bind(this);
    this.getEventByIds = this.getEventByIds.bind(this);
    this.getClassToSubTypeForType = this.getClassToSubTypeForType.bind(this);
    this.getMarketsCountByEventsIds = this.getMarketsCountByEventsIds.bind(this);
    this.getEventToMarketForEvent = this.getEventToMarketForEvent.bind(this);
    this.getEventsByMarkets = this.getEventsByMarkets.bind(this);
  }

  /**
   * getOutrightsByTypeIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getOutrightsByTypeIds(params: ISSRequestParamsModel): Promise<any> {
    const
      typeId = params.typeId || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToOutcomeForType/${typeId}?${simpleFilters}`;
    let queryParams = new HttpParams()
        .append('prune', 'event')
        .append('prune', 'market');
    if (params.childCount) {
      queryParams = queryParams.append('childCount', 'event');
    }
    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getCouponsByIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getCouponsByIds(params: ISSRequestParamsModel): Promise<any> {
    const
      couponsIds = params.couponsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/CouponToOutcomeForCoupon/${couponsIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getCouponsList()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getCouponsList(params: ISSRequestParamsModel): Promise<any> {
    const
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/Coupon?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getOutcomeByExternalId()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getOutcomeByExternalId(params: ISSRequestParamsModel): Promise<any> {
    const
      id = params.id || '',
      url = `${this.SSEndpoint}/EventToOutcomeForOutcome/~ext-ExternalOutcome:outcome:${id}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getOutcomeByExternalIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getOutcomeByExternalIds(params: ISSRequestParamsModel): Promise<any> {
    const
      ids = params.ids || '',
      url = `${this.SSEndpoint}/EventToOutcomeForOutcome/${ids}`,
      queryParams = new HttpParams()
        .append('externalKeys', 'outcome');

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEvent()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEvent(params: ISSRequestParamsModel): Promise<any> {
    const
      eventId = params.eventId || '',
      url = `${this.SSEndpoint}/Event/${eventId}`,
      queryParams = new HttpParams()
        .append('includeUndisplayed', 'true');

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventByIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventByIds(params: ISSRequestParamsModel): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToOutcomeForEvent/${eventsIds}?${simpleFilters}`;

      const queryParams = new HttpParams()
      .append('referenceEachWayTerms',true);

    return this.performRequest(url,queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventToOutcomeForOutcome()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventToOutcomeForOutcome(params: ISSRequestParamsModel): Promise<any> {
    const
      outcomesIds = params.outcomesIds || '',
      url = `${this.SSEndpoint}/EventToOutcomeForOutcome/${outcomesIds}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventsByOutcomes()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventsByOutcomes(params: ISSRequestParamsModel): Promise<any> {
    const outcomesIds = params.outcomesIds || '';

    let isValidFzSelection = params.isValidFzSelection || false;
    let simpleFilters = params.simpleFilters || '';

    if (this.isValidFzSelection) {
      isValidFzSelection = true;
    }
    // Adding include undisplayed query parameter to make sure invalid selections are not getting added
    if (this.checkForUnDisplayTrue(simpleFilters)){
      simpleFilters = simpleFilters.replace("&includeUndisplayed=true","");
      isValidFzSelection = true;
    }
    const url = `${this.SSEndpoint}/EventToOutcomeForOutcome/${outcomesIds}?${simpleFilters}`;
    const queryParams = new HttpParams()
        .append('includeRestricted', 'true')
        .append('prune', 'event')
        .append('prune', 'market')
        .append('referenceEachWayTerms', true)
        .append('includeUndisplayed', isValidFzSelection);
 
    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * Check for undisplay true filter to allow regular betreceipt flow after betplacement
   * Also during the selection addition to betslip validating the selection 
   * to make sure invalid selections are not getting added.
   * @param simpleFilters 
   * @returns {boolean}
   */
  private checkForUnDisplayTrue(simpleFilters : string): boolean {
    return simpleFilters.indexOf('includeUndisplayed=true') > -1;
  }

  /**
   * getEventsByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventsByClasses(params: ISSRequestParamsModel, childCount: boolean): Promise<any> {
    const
      classIds = params.classIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToOutcomeForClass/${classIds}?${simpleFilters}`;
      let queryParams = new HttpParams()
        .append('prune', 'event')
        .append('prune', 'market');
        
     if (childCount) {
        queryParams = queryParams.append('childCount', 'event');
     }
    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventsByEvents()
   * @param {ISSRequestParamsModel} params
   * @param {boolean} childCount
   * @returns {Promise<any>}
   */
  getEventsByEvents(params: ISSRequestParamsModel, childCount?: boolean): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters: string = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToOutcomeForEvent/${eventsIds}?${simpleFilters}`;
    let queryParams = new HttpParams()
        .append('prune', 'event')
        .append('prune', 'market')
        .append('referenceEachWayTerms',true);

    if (childCount) {
      queryParams = queryParams.append('childCount', 'event');
    }

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventsByMarkets()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventsByMarkets(params: ISSRequestParamsModel): Promise<any> {
    const
      marketIds = params.marketIds || params.marketIdArr || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToOutcomeForMarket/${marketIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventsList()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventsList(params: ISSRequestParamsModel): Promise<any> {
    const
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/Event/?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getNextEventsByType()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getNextEventsByType(params: ISSRequestParamsModel): Promise<any> {
    const
      typeId = params.typeId || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/NextNEventToOutcomeForType/${params.count}/${typeId}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getNextNEventForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getNextNEventToOutcomeForClass(params: ISSRequestParamsModel): Promise<ISportEventEntity[]> {
    const
      classIds = params.classIds,
      simpleFilters = params.simpleFilters || '',
      siteServerEventsCount = params.siteServerEventsCount,
      url = `${this.SSEndpoint}/NextNEventToOutcomeForClass/${siteServerEventsCount}/${classIds}?${simpleFilters}`;
      const queryParams = new HttpParams()
      .append('referenceEachWayTerms',true);
    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * Get Racing Results ForEvent
   * @param {ISSRequestParamsModel} params
   * @param {boolean} isPromise
   * @returns {Promise<any> | Observable<any>}
   */
  getRacingResultsForEvent(params: ISSRequestParamsModel, isPromise: boolean = true): Promise<any> | Observable<any> {
    const
      eventsIds = params.eventsIds || '',
      url = `${this.SSHistoricEndpoint}/RacingResultsForEvent/${eventsIds}`;

    const result = this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body));

    return isPromise ? result.toPromise() : result;
  }

  /**
   * EventToLinkedOutcomeForEvent()
   * @param {number} eventId
   * @returns {Observable<any>}
   */
  getEventToLinkedOutcomeForEvent(eventId: number, params: string): Promise<any> {
    const url = `${this.SSEndpoint}/EventToLinkedOutcomeForEvent/${eventId}?${params}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body)).toPromise();
  }

  /**
   * getResultedEventByEvents()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getResultedEventByEvents(params: ISSRequestParamsModel): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSHistoricEndpoint}/ResultedEvent/${eventsIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getCommentsByEventsIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getCommentsByEventsIds(params: ISSRequestParamsModel): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      url = `${this.SSCommentaryEndpoint}/CommentaryForEvent/${eventsIds}`,
      queryParams = new HttpParams()
        .append('includeUndisplayed', 'true');

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getCategories()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getCategories(params: ISSRequestParamsModel): Promise<any> {
    const
      categoriesIds = params.categoriesIds || '',
      url = `${this.SSEndpoint}/Category/${categoriesIds}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getClasses(params: ISSRequestParamsModel): Promise<any> {
    const
      classIds = params.classIds || '',
      url = `${this.SSEndpoint}/Class/${classIds}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getClassesByCategory()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getClassesByCategory(params: ISSRequestParamsModel): Promise<any> {
    const
      categoryId = params.categoryId || '',
      siteChannels = params.siteChannels || '',
      url = `${this.SSEndpoint}/Class`;
    let
      queryParams = new HttpParams()
        .append('simpleFilter', `class.categoryId:equals:${categoryId}`)
        .append('simpleFilter', `class.isActive`)
        .append('simpleFilter', `class.siteChannels:contains:${siteChannels}`);

    if (params.hasOpenEvent) {
      queryParams = queryParams.append('simpleFilter', 'class.hasOpenEvent');
    }

    const operations = [
      map((data: HttpResponse<any>) => data.body)
    ];

    // cache data for HR and GH for 10 seconds
    const cacheCategories = [
      environment.CATEGORIES_DATA.racing.horseracing.id,
      environment.CATEGORIES_DATA.racing.greyhound.id
    ];
    if (cacheCategories.includes(params.categoryId)) {
      operations.push(cache(`${url}/${queryParams}`, 10000));
    }

    return (this.performRequest(url, queryParams)as any).pipe(...operations).toPromise();
  }

  /**
   * getClassToSubTypeForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getClassToSubTypeForClass(params: ISSRequestParamsModel): Promise<any> {
    const
      classIds = params.classIds || '',
      url = `${this.SSEndpoint}/ClassToSubTypeForClass/${classIds}`;
    let
      queryParams = new HttpParams();

    if (params.simpleFilter) {
      queryParams = queryParams.append('simpleFilter', params.simpleFilter);
    }

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getClassToSubTypeForType()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getClassToSubTypeForType(params: ISSRequestParamsModel): Promise<any> {
    const
      typeIds = params.typeIds || '',
      url = `${this.SSEndpoint}/ClassToSubTypeForType/${typeIds}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getMarketsCountByClasses()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getMarketsCountByClasses(params: ISSRequestParamsModel): Promise<any> {
    const
      classIds = params.classIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToMarketForClass/${classIds}?${simpleFilters}`,
      queryParams = new HttpParams()
        .append('count', `event:market`);

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventToMarketForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventToMarketForClass(params: ISSRequestParamsModel): Promise<any> {
    const
      classIds = params.classIds,
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToMarketForClass/${classIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEvenForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise <ISportEvent[]> }
   */
  getEventForClass(params: ISSRequestParamsModel): Promise<ISportEvent[]> {
    const
      classIds = params.classIds,
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventForClass/${classIds}?${simpleFilters}`;
    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getMarketsCountByEventsIds()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getMarketsCountByEventsIds(params: ISSRequestParamsModel): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/EventToMarketForEvent/${eventsIds}?${simpleFilters}`,
      queryParams = new HttpParams()
        .append('count', `event:market`);

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventToMarketForEvent()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventToMarketForEvent(params: ISSRequestParamsModel): Promise<any>  {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters = params.simpleFilters || '';
    let url = `${this.SSEndpoint}/EventToMarketForEvent/${eventsIds}`;
    url = url + (simpleFilters !== '' ? `?${simpleFilters}` : ``);

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getSportToCollection()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getSportToCollection(params: ISSRequestParamsModel): Promise<any> {
    const
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/SportToCollection?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getJackpotPools()
   * @returns {Promise<any>}
   */
  getJackpotPools(): Promise<any> {
    const url = `${this.SSEndpoint}/Pool`,
      queryParams = new HttpParams()
        .append('simpleFilter', `pool.type:equals:V15`)
        .append('simpleFilter', `pool.isActive`);

    return this.performRequest(url, queryParams).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getPoolToPoolValue()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getPoolToPoolValue(params: ISSRequestParamsModel): Promise<any> {
    const
      poolsIds = params.poolsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/PoolToPoolValue/${poolsIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getPoolForEvent()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getPoolForEvent(params: ISSRequestParamsModel): Promise<any> {
    const
      eventsIds = params.eventsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/PoolForEvent/${eventsIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getPoolForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getPoolForClass(params: ISSRequestParamsModel): Promise<any> {
    const
      classIds = params.classIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/PoolForClass/${classIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getPool()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getPool(params: ISSRequestParamsModel): Promise<any> {
    const
      poolsIds = params.poolsIds || '',
      simpleFilters = params.simpleFilters || '',
      url = `${this.SSEndpoint}/Pool/${poolsIds}?${simpleFilters}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * getEventsByType()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<any>}
   */
  getEventsByType(params: ISSRequestParamsModel): Promise<any> {
    const
      typeId = params.typeId || '',
      url = `${this.SSEndpoint}/EventForType/${typeId}`;

    return this.performRequest(url).pipe(
      map((data: HttpResponse<any>) => data.body))
      .toPromise();
  }

  /**
   * PerformRequest()
   * @param url
   * @param params
   * @returns {Observable<HttpResponse<T>>}
   */
  private performRequest<T>(url, params: any = {}): Observable<HttpResponse<T>> {
    return this.http
      .get<T>(`${url}`, {
        observe: 'response',
        params: params,
        headers: {
          accept: 'application/json'
        }
      }).pipe(
        timeout(this.TIMEOUT),
        catchError((err) => {
          return throwError(err);
        })
      );
  }
}
