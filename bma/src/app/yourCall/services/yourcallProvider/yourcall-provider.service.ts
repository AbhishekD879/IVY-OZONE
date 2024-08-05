import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Observer } from 'rxjs';
import * as _ from 'underscore';
import { map } from 'rxjs/operators';

import { BybApiService } from '../BYB/byb-api.service';
import { BybHelperService } from '../BYB/byb-helper.service';
import { IBybProvider, IYourcallProviders } from '../../models/provider.model';
import {
  IBYBLeaguesPeriod,
  IEmptyMethodResult, IGetMarketSelectionsParams,
  IYourcallAPIRequestData, IYourcalStatValuesParams, IYourcallPlayerStatisticParams
} from '@yourcall/models/request-params.model';
import { IBybMarket, IYourCallMarket } from '@core/services/cms/models';
import { YourCallEvent } from '@yourcall/models/yourcall-event';
import { IYourcallDsEventsResponse } from '@yourcall/models/ds-events-response.model';
import {
  IYourcallAccumulatorOddsResponse,
  IYourcallStatisticResponse,
  IPlayerBets
} from '@yourcall/models/yourcall-api-response.model';
import { IOddsParams } from '@yourcall/models/odds-params.model';
import { IYourCallEDPMarket } from '@core/services/cms/models/yourcall/yourcall-market.model';
import {
  IYourcallBYBLeagueEventsResponse
} from '@yourcall/models/byb-events-response.model';
import { IConditions } from '@root/app/lazy-modules/bybHistory/models/byb-selection.model';

@Injectable({ providedIn: 'root' })
export class YourcallProviderService {
  private pendingRequestsList: Observer<any>[] = [];
  private provider: IBybProvider;
  private readonly providers: IYourcallProviders;
  public bybPlayers: IConditions = {};

  constructor(
    private bybApiService: BybApiService,
    private bYBHelperService: BybHelperService,
    private http: HttpClient
  ) {
    this.providers = {
      BYB: { api: this.bybApiService, helper: this.bYBHelperService }
    };
    this.use('BYB');
  }

  /**
   * Get active data provider api code
   * @return {*}
   * @constructor
   */
  get API(): string {
    return this.provider && this.provider.api.code;
  }
  set API(value:string){}

  /**
   * Get byb show card
   * @return {*|Array}
   */
   get showCardPlayers(): IConditions {
     return this.bybPlayers;
  }
  set showCardPlayers(value:IConditions){
    this.bybPlayers = value;
  }

  /**
   * Get provider related helper service which store provider data transformations
   * @return {*|Array}
   */
  get helper(): BybHelperService {
    return this.provider.helper;
  }
  set helper(value:BybHelperService){}
  /**
   * Updates the API to be used for performing requests to the data provider.
   * Whenever the API is changed all unresolved requests are considered to be outdated
   * and are dropped with $cancelRequest, which rejects its promise with "undefined".
   * For separate independent calls to different providers the useOnce method should be used.
   * @param providerAPI
   */
  use(providerAPI: string): void {
    if (this.try(providerAPI) && providerAPI !== this.API) {
      this.provider = this.providers[providerAPI];
      console.warn(`YC: api is set to ${providerAPI}`);
      while (this.pendingRequestsList.length) {
        this.pendingRequestsList.pop().complete();
      }
    }
  }

  /**
   * Creates a once-used 'shadow' instance with original YourCallProvider as prototype.
   * This instance has its own overridden properties, such as provider, request etc.
   * Method does not change the original provider API, but uses desired one to create a request.
   * Also this avoids dropping unresolved consecutive calls to different APIs as outdated.
   * @param providerAPI
   * @returns {YourcallProviderService}
   */
  useOnce(providerAPI: string): YourcallProviderService {
    const API = this.try(providerAPI) ? providerAPI : this.API;
    return _.extend(Object.create(this), {
      provider: this.providers[API],
      pendingRequestsList: []
    });
  }

  isValidResponse(error: any, requestName: string): boolean {
    return !!(error !== undefined || console.warn(`YC:${requestName || ''} request is expired due to provider API change`));
  }

  /**
   * Get list of leagues with #yourCall available
   * @returns {promise}
   */
  getLeagues(): Promise<any>  {
    return this.prepareRequest(this.provider.api.getLeagues());
  }

  getLeagueEventsWithoutPeriod(): Promise<IYourcallBYBLeagueEventsResponse> {
    return this.prepareRequest(this.provider.api.getLeagueEventsWithoutPeriod());
  }

  /**
   *  Get leagues public method
   */
  getUpcomingLeagues(): Promise<any> {
    return this.prepareRequest(this.provider.api.getUpcomingLeagues());
  }

  /**
   * Get events for league and period
   * @param leagueIds
   * @param period
   * @returns {promise}
   */
  getLeagueEvents(leagueIds: number | number[], period: IBYBLeaguesPeriod): Promise<IYourcallBYBLeagueEventsResponse> {
    return this.prepareRequest(this.provider.api.getLeagueEvents(leagueIds, period));
  }

  /**
   * Get games for array of league ids
   * @param {Array} typeIds
   */
  getGames(typeIds: number[]): Promise<IYourcallDsEventsResponse> {
    return this.prepareRequest(this.provider.api.getGames(typeIds));
  }

  /**
   * Get game object from DS with #yourCall available
   * @param obEventId
   * @returns {promise}
   */
  getGameInfo(obEventId: string): Promise<any> {
    return this.prepareRequest(this.provider.api.getGameInfo(obEventId));
  }

  /**
   * Get EDP Markets
   * @returns {promise}
   */
  getEDPMarkets(): Promise<IYourCallEDPMarket[]> & Promise<IBybMarket[]> {
    return this.prepareRequest(this.provider.api.getEDPMarkets());
  }

  /**
   * Get players for specific game
   * @param obEventId
   * @return {promise}
   */
  getPlayers(obEventId: number): Promise<IPlayerBets> {
    return this.prepareRequest(this.provider.api.getPlayers(obEventId));
  }

  /**
   * Get list of gfm markets
   * @param event
   * @returns {promise}
   */
  getMatchMarkets(event: YourCallEvent): Promise<any> {
    return this.prepareRequest(this.provider.api.getMatchMarkets(event));
  }

  /**
   * Get list of statistics
   * @param params
   * @returns {promise}
   */
  getStatistics(params: IYourcallPlayerStatisticParams): Promise<IYourcallStatisticResponse> {
    return this.prepareRequest(this.provider.api.getStatistics(params));
  }

  /**
   * Get max stake for betslip, validate selection in YC dashboard
   * @param params
   * @returns {*}
   */
  getMaxExposure(params): Promise<any> {
    return this.prepareRequest(this.provider.api.getMaxExposure(params));
  }

  /**
   * Get object with statistic params
   * @param params
   * @returns {promise}
   */
  getStatValues(params: IYourcalStatValuesParams): Promise<any> {
    return this.prepareRequest(this.provider.api.getStatValues(params));
  }

  /**
   * Calculate odds for Player Bets selection
   * @param params
   * @returns {promise}
   */
  calculateOdds(params): Promise<any> {
    return this.prepareRequest(this.provider.api.calculateOdds(params));
  }

  /**
   * Calculate accumulator odds
   * @param {object} params
   * @returns {promise}
   */
  calculateAccumulatorOdds(params: IOddsParams): Promise<IYourcallAccumulatorOddsResponse> {
    return this.prepareRequest(this.provider.api.calculateAccumulatorOdds(params));
  }

  /**
   * Get DS bet by bet id
   * @param betId
   */
  getBets(betId: number): Promise<any> {
    return this.prepareRequest(this.provider.api.getBets(betId));
  }

  /**
   * Get selections for specific markets
   * @param params
   * @returns {*}
   */
  getMarketSelections(params: IGetMarketSelectionsParams): Promise<any> {
    return this.prepareRequest(this.provider.api.getMarketSelections(params));
  }

  /**
   * Checks whether the provider API exists before trying to apply it.
   * If not - logs a corresponding warning.
   * @param providerAPI
   * @returns {boolean}
   * @private
   */
  try(providerAPI: string): boolean {
    return !!(this.providers[providerAPI] || console.warn(`YC: incorrect API ${providerAPI} is tried to be used, ${this.API} kept.`));
  }

  /**
   * Removes the resolved request form pendingRequestsList, so it won't be cancelled if toggling occurs.
   * Returns "true" if request was found in the list, "false" if not.
   * @param {Observer} requestObserver
   * @returns {boolean}
   * @private
   */
  private releaseRequest<T>(requestObserver: Observer<T>): boolean {
    const index = this.pendingRequestsList.indexOf(requestObserver);
    return !!(index >= 0 && this.pendingRequestsList.splice(index, 1));
  }

  /**
   * Prepare API request and add signature.
   * As soon as the request is resolved or rejected in a ordinary way its instance is removed from pendingRequestsList
   * If the provided requestData argument has 'resolve' property, then its value will be instantly passed to a returned promise.
   * This is used in case API instance does not have a certain method implementation but still should return some fallback value.
   * @param {object|promise} requestData
   * @param {boolean} cache
   * @returns {promise}
   * @private
   */
  private prepareRequest(
    requestData: IYourcallAPIRequestData | IEmptyMethodResult | Promise<IYourCallMarket[]> | Promise<IBybMarket[]>
  ): Promise<any> {
    const yourcallAPIRequestData = requestData as IYourcallAPIRequestData;
    const emptyMethodResult = requestData as IEmptyMethodResult;
    const promiseInRequest = requestData as Promise<IYourCallMarket[]> | Promise<IBybMarket[]>;

    if (_.isFunction(promiseInRequest.then)) {
      return promiseInRequest;
    }

    if (emptyMethodResult.resolve) {
      return Promise.resolve(emptyMethodResult.resolve);
    }

    const uri = this.provider.api.getUri(yourcallAPIRequestData);
    const method = yourcallAPIRequestData.method || 'GET';
    const params = this.provider.api.extendParams(yourcallAPIRequestData.params);

    return this.createRequest(uri, method, params)
      .toPromise();
  }

  private createRequest<T>(uri, method, params): Observable<T> {
    // additional observable
    // to have possibility complete observable earlier than we got data, emulates cancel request.
    return Observable.create(observer => {
      let request;

      if (method === 'GET') {
        request = this.http.get(uri, {
          observe: 'response',
          params: params
        });
      } else {
        request = this.http.post(uri, params, {
          observe: 'response'
        });
      }

      request.pipe(map((response: HttpResponse<T>) => {
        return response.body;
      })).subscribe((data: T) => {
        observer.next(data);
        observer.complete();
        this.releaseRequest(observer);
      }, error => {
        console.warn(`BYB REQUEST '${uri}' FAILED: (${error.message})`);
        observer.complete();
        this.releaseRequest(observer); // remove
      });

      // array of observable to complete it before we get data, emulates cancel
      this.pendingRequestsList.push(observer);
    });
  }
}
