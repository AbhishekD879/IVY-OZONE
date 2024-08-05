import { empty as observableEmpty, Observable, Observer } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { catchError, concatMap, map } from 'rxjs/operators';
import {
  IAuthenticateResponseModel,
  ICheckEligibilityResponseModel,
  IGetPlayerInfoResponseModel,
  IGetWebTokenResponseModel, IResponseCommonModel,
  IUpgradeAccountResponseModel, IRequestCommonModel, IGetIdTokenInfoFromUserNameResponseModel
} from '@retail/services/upgradeAccountProvider/upgrade-account-provider.model';

@Injectable({providedIn: 'root'})
export class UpgradeAccountProviderService {
  // TODO: move to env.
  private retailCreds = { hash: 'MzFhNDYwNDhkZGJiNjdiYzZkYTI0ODMzZTRmNDAxNmEwMTliNzFmYTkzODc0NDY0MTJmMDRmOTZmZDk2N2M5YQ' };
  private token: string;

  constructor(
    private http: HttpClient,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService
  ) { }

  /**
   * Authenticate
   * Call authenticate service.
   *
   * @param {object} - data - card information data.
   * @return {object} - promise
   */
  authenticate(cardNo: string, pin: number): Observable<IAuthenticateResponseModel> {
    return this.getRequest<IAuthenticateResponseModel>('authenticate', { cardNo, pin });
  }

  /**
   * isEligible
   * Check if user is elegible for upgrade.
   *
   * @param {object} - data - card information data.
   * @return {object} - promise
   */
  isEligible(cardNumber: string, pin: number): Observable<ICheckEligibilityResponseModel> {
    return this.getRequest<ICheckEligibilityResponseModel>('isinshopeligibleforupgrade',
      { cardNumber, pin });
  }

  /**
   * getPlayerInfo
   * Call getPlayerInfo service.
   *
   * @return {object} - Observable
   */
  getPlayerInfo(cardNumber: string): Observable<IGetPlayerInfoResponseModel> {
    return this.getRequest<IGetPlayerInfoResponseModel>('getplayerinfo', { username: cardNumber });
  }

  /**
   * upgradeAccount
   * Call upgradeAccount service.
   *
   * @param {object} - data - userData map.
   * @return {object} - promise
   */
  upgradeAccount(userData: any): Observable<IUpgradeAccountResponseModel> {
    return this.getRequest<IUpgradeAccountResponseModel>('upgradeinshoptomultichannel', userData);
  }

  getRequest<T>(url: string, params?: any, apolloRoute = environment.APOLLO.CWA_ROUTE): Observable<T> {
    const endpoint = `${ environment.APOLLO.API_ENDPOINT }/${ apolloRoute }/${ url }`;

    return this.getWebToken().pipe(
      concatMap(token => {
        if (token) {
          return this.http
            .post<T>(endpoint, params, {
              headers: new HttpHeaders({
                'Authorization': `Bearer ${ token }`
              })
            }).pipe(
            map((res: IResponseCommonModel|any) => {
              if (res.errorMessage === 'Token is not valid') {
                this.token = '';
                return this.getRequest<T>(url, params);
              }
              return res;
            }),
            catchError((error: HttpErrorResponse) => {
              if (error && error.status === 401) {
                this.token = '';
                return this.getRequest<T>(url, params);
              } else {
                if (error.error.text && error.error.text.includes('Service failure')) {
                  this.infoDialogService.openOkDialog(this.localeService.getString('app.serverError'));
                }

                return observableEmpty();
              }
            }));
        }
      }));
  }

  /**
   * getCardRequest
   * Call to get loggedIn user card number.
   *
   * @param {object} - data - IRequestCommonModel map.
   * @return {object} - Observable
   */
  getCardRequest(params: IRequestCommonModel): Observable<IGetIdTokenInfoFromUserNameResponseModel> {
    const endpoint = `${environment.APOLLO.CARD_ENDPOINT}/${params.username}/token-id?api-key=`
    +`${environment.APOLLO.API_KEY}&locale=en-GB&tokenType=gvc`;
    const headerData = params.customerSessionId.substring(12);
    return this.http
      .get(endpoint, {
        observe: 'response',
        headers: {
          'X-CLIENT-REQUEST-ID': headerData,
          'X-FORWARDED-FOR': headerData,
          'Authorization': `Bearer ${params.customerSessionId}`
        }
      }).pipe(
        map((res: IResponseCommonModel | any) => {
          return res;
        })
      );
  }

  private getWebToken(): Observable<string> {
    const endpoint = `${ environment.APOLLO.API_ENDPOINT }/${ environment.APOLLO.CWA_ROUTE }/sessionwebtoken`;

    if (this.token) {
      return Observable.create((observer: Observer<string>) => {
        observer.next(this.token);
      });
    }

    return this.http.post(endpoint, this.retailCreds).pipe(
      map((res: IGetWebTokenResponseModel) => {
        this.token = res.data.token;
        return this.token;
      }));
  }
}
