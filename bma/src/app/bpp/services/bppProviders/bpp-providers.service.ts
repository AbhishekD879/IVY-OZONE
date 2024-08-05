import { map, shareReplay } from 'rxjs/operators';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, Subject, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import {
  IAccountFreebetsResponse,
  IAccountHistoryRequest,
  IAccountHistoryResponse,
  IBetsRequest,
  IBetsResponse,
  IBppRequest,
  ICashoutBetRequest,
  ICashoutBetResponse,
  ICurrenciesResponse,
  IMatchDayRewardsParamsRequest,
  IMatchDayRewardsResponse,
  IFreeBetOfferRequest,
  IFreeBetOfferResponse,
  IFreebetsTypes,
  IGetVideoStreamRequest,
  IGetVideoStreamResponse,
  IHowItWorks,
  IOfferBet,
  IReadBetRequest,
  IReadBetResponse,
  IRequestTransFreebetTrigger,
  IRequestTransGetBetDetail,
  IRequestTransGetBetDetails,
  IRequestTransGetBetsPlaced,
  IRequestTransPoolGetDetail,
  IResponseTransFreebetTrigger,
  IResponseTransGetBetDetail,
  IResponseTransGetBetDetails,
  IResponseTransGetBetsPlaced,
  IResponseTransPoolGetDetail,
  IValidateBetResponse,
  IRequestTransBetpackTrigger,
  IResponseTransBetpackTrigger,
  IApiGetLimitsResponse
} from './bpp-providers.model';
import { ProxyHeadersService } from '../proxyHeaders/proxy-headers.service';
import * as _ from 'underscore';
import { BppCacheService } from '@app/bpp/services/bppProviders/bpp-cache.service';
import { DeviceService } from '@core/services/device/device.service';
import { IFreebestsResponsesCache } from '@app/bpp/services/bpp/bpp.model';

@Injectable()
export class BppProvidersService {
  BPP_ENDPOINT: string;
  getFreebetsRequest: Subject<IFreebestsResponsesCache>;

  constructor(
    private bppCacheService: BppCacheService,
    private proxyHeaders: ProxyHeadersService,
    private http: HttpClient,
    private deviceService: DeviceService,
  ) {
    this.BPP_ENDPOINT = environment.BPP_ENDPOINT;
  }

  buildBet(body: IBetsRequest): Observable<IBetsResponse> {
    return this.postData(`v1/buildBet`, body).pipe(
      map((response: HttpResponse<IBetsResponse>) => response.body));
  }

  /**
   * quickbet with and without login
   * @param  {IBppRequest} body
   * @param  {boolean} userloggedIn
   * @returns Observable
   */
   quickBet(body: IBppRequest, userloggedIn: boolean): Observable<IBetsResponse> {
    if(userloggedIn) {

      return this.postData(`v1/buildBet`, body, this.createHeaders()).pipe(
        map((response: HttpResponse<IBetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
    } else {
      return this.postData(`v1/buildBet`, body).pipe(
        map((response: HttpResponse<IBetsResponse>) => response.body));
    }
  }

  buildBetLogged(body: IBetsRequest): Observable<IBetsResponse> {
    return this.postData(`v1/buildBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IBetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  lottoBuildBet(body: IBetsRequest): Observable<IBetsResponse | any> {
    return this.postData(`v1/lotto/buildBet`, body).pipe(
      map((response: HttpResponse<IBetsResponse>) => response.body));
  }
  
  lottoBuildBetLogged(body: IBetsRequest): Observable<IBetsResponse> {
    return this.postData(`v1/lotto/buildBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IBetsResponse>) => response.body));
  }
  
  placeBet(body: IBetsRequest): Observable<IBetsResponse> {
    if (!body || !body.bet || body.bet.length === 0) {
      return throwError({
        errorCode: 'Mistery of bet with empty bet array of logged out'
      });
    }
    return this.postData(`v1/placeBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IBetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  placePoolBet(body: IBetsRequest): Observable<IBetsResponse> {
    return this.postData(`v2/placePoolBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IBetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  placeWinPoolBet(body: IBetsRequest): Observable<IBetsResponse> {
    return this.postData(`v1/placeWinPoolBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IBetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  cashoutBet(body: ICashoutBetRequest): Observable<ICashoutBetResponse> {
    return this.postData(`v1/cashoutBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<ICashoutBetResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  readBet(body: IReadBetRequest): Observable<IReadBetResponse> {
    return this.postData(`v1/readBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IReadBetResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  validateBet(body: IBetsRequest): Observable<IValidateBetResponse> {
    return this.postData(`validateBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IValidateBetResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  offerBet(body: IOfferBet): Observable<IOfferBet> {
    return this.postData(`v1/offerBet`, body, this.createHeaders()).pipe(
      map((response: HttpResponse<IOfferBet>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  getBetHistory(params: IAccountHistoryRequest, url: string = ''): Observable<IAccountHistoryResponse> {
    const httpParams: string = this.getEncodeParams(params);

    return this.getResponseData(`accountHistory${url}`, httpParams).pipe(
      map((response: HttpResponse<IAccountHistoryResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  getBetDetail(params: IRequestTransGetBetDetail): Observable<IResponseTransGetBetDetail> {
    let httpParams: HttpParams = this.createGetParams(_.omit(params, 'betId'));
    _.each(params.betId, id => {
      httpParams = httpParams.append('betId', id);
    });
    return this.getData(`getBetDetail/betslip`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransGetBetDetail>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  getPoolBetDetail(params: IRequestTransPoolGetDetail): Observable<IResponseTransPoolGetDetail> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`getPoolBetDetail`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransPoolGetDetail>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  getBetDetails(params: IRequestTransGetBetDetails): Observable<IResponseTransGetBetDetails> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`getBetDetails`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransGetBetDetails>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  getBetsPlaced(params: IRequestTransGetBetsPlaced): Observable<IResponseTransGetBetsPlaced> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`getBetsPlaced`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransGetBetsPlaced>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  /**
   * call to fetch data for euro when user is logged in
   * @param params {IMatchDayRewardsParamsRequest}
   * @returns Observable {IMatchDayRewardsResponse}
   */
  getMatchDayRewardsWithBadges(params: IMatchDayRewardsParamsRequest): Observable<IMatchDayRewardsResponse> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`matchDayRewardsWithBadges`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IMatchDayRewardsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  /**
   * call to fetch default data for euro when user is not logged in
   * @returns Observable {IMatchDayRewardsResponse}
   */
   getMatchDayRewardsWithOutBadges(): Observable<IMatchDayRewardsResponse> {
    return this.getData(`matchDayRewardsWithOutBadges`, this.createHeaders()).pipe(
      map((response: HttpResponse<IMatchDayRewardsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  /**
   * call to fetch howitworks string
   * @returns Observable {IHowItWorks}
   */
   getHowItWorksData(): Observable<IHowItWorks> {
    return this.getData(`howItWorks`, this.createHeaders()).pipe(
      map((response: HttpResponse<IHowItWorks>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  freeBetOffer(params: IFreeBetOfferRequest): Observable<IFreeBetOfferResponse> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`freebetOffers`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IFreeBetOfferResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  freebetTrigger(params: IRequestTransFreebetTrigger): Observable<IResponseTransFreebetTrigger> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`freebetTrigger`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransFreebetTrigger>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  /**
   * call to purchase bet pack trigger
   * @param params {IRequestTransFreebetTrigger}
   * @returns Observable {IResponseTransFreebetTrigger}
   */
  betPackTrigger(params: IRequestTransBetpackTrigger): Observable<IResponseTransBetpackTrigger> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`betPackTrigger`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IResponseTransBetpackTrigger>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  videoStream(params: IGetVideoStreamRequest): Observable<IGetVideoStreamResponse> {
    const httpParams: HttpParams = this.createGetParams(params);
    return this.getData(`videoStream`, this.createHeaders(), httpParams).pipe(
      map((response: HttpResponse<IGetVideoStreamResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  allAccountFreebets(freebetsType: IFreebetsTypes): Observable<IAccountFreebetsResponse> {
    if (!this.getFreebetsRequest && !this.bppCacheService.cachedFreebetsResponce[freebetsType]) {
      const requestUrl = `accountFreebets?channel=${this.deviceService.freeBetChannel}`;
      this.getFreebetsRequest = new Subject();
      this.getData(requestUrl, this.createHeaders())
        .pipe(
          map((response: HttpResponse<IAccountFreebetsResponse>) =>
            ({ ...this.bppCacheService.processFreebetsResponce(response), token: response.headers.get('token') } as any))
        )
        .subscribe((response: IFreebestsResponsesCache) => {
          this.getFreebetsRequest.next(response);
          this.getFreebetsRequest.complete();
          this.getFreebetsRequest = undefined;
        }, (err: HttpErrorResponse) => {
          this.getFreebetsRequest.error(err);
          this.getFreebetsRequest.complete();
          this.getFreebetsRequest = undefined;
        });
    } else if (this.bppCacheService.cachedFreebetsResponce[freebetsType]) {
      return of(this.bppCacheService.cachedFreebetsResponce[freebetsType]);
    }

    return this.getFreebetsRequest
      .pipe(
        map((response: IFreebestsResponsesCache) => {
          return (({ ...response[freebetsType], token: response.token }) as any);
        })
      );
  }

  accountFreebets(): Observable<IAccountFreebetsResponse> {
    const requestUrl = `accountFreebets?freebetTokenType=SPORTS&channel=${this.deviceService.freeBetChannel}`;
    return this.getData(requestUrl, this.createHeaders()).pipe(
      map((response: HttpResponse<IAccountFreebetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  /**
   * Get free bets with return limits 
   */
  accountFreebetsWithLimits(): Observable<IAccountFreebetsResponse> {
    const requestUrl = `accountFreebetsWithLimits?freebetTokenType=SPORTS&channel=${this.deviceService.freeBetChannel}&returnOffers=Y&returnFreebetTokens=Y&returnQualifiedOffers=Y`;
    return this.getData(requestUrl, this.createHeaders()).pipe(
      map((response: HttpResponse<IAccountFreebetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

    /**
   * Get free bets with return No limits 
   */
    accountFreebetsWithNoLimits(): Observable<IAccountFreebetsResponse> {
      const requestUrl = `accountFreebetsWithLimits?freebetTokenType=SPORTS&channel=${this.deviceService.freeBetChannel}&returnOffers=Y&returnQualifiedOffers=Y`;
      return this.getData(requestUrl, this.createHeaders()).pipe(
        map((response: HttpResponse<IAccountFreebetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
    }

  /**
   * Get account limits
   */
  accountGetLimits(): Observable<any> {
    const requestUrl = `accountGetLimits?freebetTokenType=SPORTS&limitSort=BETPACK_DAILY_CUST_LIMIT`;
    return this.getData(requestUrl, this.createHeaders()).pipe(
      map((response: HttpResponse<any>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  accountOffers(): Observable<IAccountFreebetsResponse> {
    const requestUrl = `accountFreebets?freebetTokenType=SPORTS&channel=${this.deviceService.freeBetChannel}&returnOffers=Y`;
    return this.getData(requestUrl, this.createHeaders()).pipe(
      map((response: HttpResponse<IAccountFreebetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  accountOddsBoost(): Observable<IAccountFreebetsResponse> {
    return this.getData(`accountFreebets?freebetTokenType=BETBOOST`, this.createHeaders()).pipe(
      map((response: HttpResponse<IAccountFreebetsResponse>) => ({ ...response.body, token: response.headers.get('token') })));
  }

  privateMarkets(): Observable<IAccountFreebetsResponse> {
    const privateMarketsType: IFreebetsTypes = 'ACCESS';
    const cachedResponse = this.bppCacheService.cachedFreebetsResponce[privateMarketsType];

    if (cachedResponse) {
      return of(cachedResponse);
    }

    if (this.getFreebetsRequest) {
      return this.allAccountFreebets(privateMarketsType);
    }

    return this.getData(`accountFreebets?freebetTokenType=ACCESS`, this.createHeaders()).pipe(
      map((response: HttpResponse<IAccountFreebetsResponse>) => {
        // cache private markets response, will be creared on logout or placebet
        this.bppCacheService.cachedFreebetsResponce[privateMarketsType] = response.body;
        this.bppCacheService.setupCacheRemoveLogic();
        return ({ ...response.body, token: response.headers.get('token') });
      }));
  }

  getCurrencyRates(): Observable<ICurrenciesResponse> {
    return this.getData(`currencies`).pipe(
    map((response: HttpResponse<ICurrenciesResponse>) => response.body));
  }

    /**
   * New API for Betpack Signposting
   * @param body
   * @returns
   */
  initialWSGetLimits(body: IBppRequest): Observable<IApiGetLimitsResponse> {
    return this.putData(`freebetOffers`, body).pipe(
      map((response: HttpResponse<IApiGetLimitsResponse>) => (response.body)));
  }

  private getData<T>(url: string, headers: HttpHeaders = null, params: HttpParams = null): Observable<HttpResponse<T>> {
    return this.http.get<T>( `${this.BPP_ENDPOINT}/${url}`, {
      observe: 'response',
      withCredentials: true,
      headers,
      params
    });
  }

  private getResponseData<T>(url: string, params: string): Observable<HttpResponse<T>> {
    return this.http.get<T>( `${this.BPP_ENDPOINT}/${url}?${params}`, {
      observe: 'response',
      withCredentials: true,
      headers: this.createHeaders()
    });
  }

  /**
   * Generate headers for BPP Api calls.
   */
  private createHeaders(): HttpHeaders {
    return new HttpHeaders({
      token: this.proxyHeaders.generateBppAuthHeaders()
    });
  }

  /**
   * Generate get params for BPP Api calls.
   */
  private createGetParams(params: IBppRequest): HttpParams {
    let httpParams: HttpParams = new HttpParams();
    Object.keys(params).forEach( param => {
      httpParams = httpParams.append(param, params[param]);
    });
    return httpParams;
  }

  private getEncodeParams(params: IBppRequest): string {
    return Object.keys(params).map(key => {
      return `${key}=${encodeURIComponent(params[key])}`;
    }).join('&');
  }

  private postData<T>(url: string, body: IBppRequest, headers: HttpHeaders = null): Observable<HttpResponse<T>> {
    return this.http.post<T>( `${this.BPP_ENDPOINT}/${url}`, body, {
      observe: 'response',
      withCredentials: true,
      headers
    }).pipe(
      shareReplay()
    );
  }

  private putData<T>(url: string, body: IBppRequest, headers: HttpHeaders = null): Observable<HttpResponse<T>> {
    return this.http.put<T>( `${this.BPP_ENDPOINT}/${url}`, body, {
      observe: 'response',
      withCredentials: true,
      headers
    }).pipe(
      shareReplay()
    );
  }
}
