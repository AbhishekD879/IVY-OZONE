import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Campaign } from '../../models/freeRideCampaign.model';
import { FreeRideSplashPageModel } from '@app/free-ride/splash-page/model/splash-page.model';
import { ViewPotsDataTable } from '@root/app/free-ride/view-pot-table/model/view-pots.model';

@Injectable()
export class FreerideService extends AbstractService<Configuration> {
  freeRideCampaignByBrandUrl: string = `freeride/campaign/brand/${this.brand}`;
  freeRideCampaignUrl: string = 'freeride/campaign';
  freeRideCampaignUrlDelete: string = `freeride/campaign/brand/${this.brand}`;
  freeRideCreatePots: string = 'freeride/campaign/createpots';
  freeRideViewPots: string = `freeride/campaign/viewpots/brand/${this.brand}`;
  sortParamName: string = `sort`;
  splashScreenUrl: string = `freeride/splashpage`;
  splash: string = `freeride/splashpage/brand/${this.brand}`;


  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getCampaigns(): Observable<HttpResponse<Campaign[]>> {
    return this.sendRequest<Campaign[]>('get', this.freeRideCampaignByBrandUrl, null);
  }
  public getCampaignsByBrandWithOrdering(sortParamValue: string): Observable<HttpResponse<Campaign[]>> {
    return this.sendRequest<Campaign[]>('get', `${this.freeRideCampaignByBrandUrl}?${this.sortParamName}=${sortParamValue}`, null);
  }
  /**
   * Get Splash Screen data.
   * @returns {Observable<HttpResponse<FreeRideSplashPageModel>>}
   */
  getAllSplashData(): Observable<HttpResponse<FreeRideSplashPageModel[]>> {
    return this.sendRequest<FreeRideSplashPageModel[]>('get', this.splash, null);
  }

  /**
 * Get Pots table Data.
 * @returns {Observable<HttpResponse<ViewPotsDataTable>>}
 */
  getViewPotsData(campaignId: string): Observable<any> {
    /*   const url = './assets/viewPotsDataMock.json';
      return this.http.get(url); */
    return this.sendRequest<ViewPotsDataTable[]>('get', `${this.freeRideViewPots}/${campaignId}`, null);
  }


  /**
   * Post Splash Screen data.
   * @returns {Observable<HttpResponse<FreeRideSplashPageModel>>}
   */
  public postSplashData(freeRideSplashData: FormData): Observable<HttpResponse<FreeRideSplashPageModel[]>> {
    return this.sendRequest<FreeRideSplashPageModel[]>('post', this.splashScreenUrl, freeRideSplashData);
  }
  /**
   * Save/Update Splash Screen data.
   * @returns {Observable<HttpResponse<FreeRideSplashPageModel>>}
   */
  public updateSplashData(freeRideSplashData: FormData, id: string): Observable<HttpResponse<FreeRideSplashPageModel[]>> {
    const url = `${this.splashScreenUrl}/${id}`;
    return this.sendRequest<FreeRideSplashPageModel[]>('put', url, freeRideSplashData);
  }
  /**
     * Create Campaign data.
     * @returns {Observable<HttpResponse<any>>}
     */
  public postNewCampaign(campaign: Campaign): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.freeRideCampaignUrl, campaign);
  }

  /**
   * Update Campaign data.
   * @returns {Observable<HttpResponse<any>>}
   */
  public updateCampaign(id: string, campaign: any, flag: boolean): Observable<HttpResponse<any>> {
    const apiUrl = `${this.freeRideCampaignUrl}/${id}/${flag}`;
    return this.sendRequest<any>('put', apiUrl, campaign);
  }

  /**
   * Create Pots.
   * @returns {Observable<HttpResponse<any>>}
   */
  public createPots(id: string): Observable<HttpResponse<any>> {
    const url = `${this.freeRideCreatePots}/${id}`;
    return this.sendRequest<any>('get', url, null);
  }

  /**
   * get Campaign data.
   * @returns {Observable<HttpResponse<any>>}
   */
  public getSingleCampaign(id: string): Observable<HttpResponse<any>> {
    const url = `${this.freeRideCampaignUrl}/${id}`;
    return this.sendRequest<any>('get', url, null);
  }

  /**
   * Delete Campaign data.
   * @returns {Observable<HttpResponse<void>>}
   */
  public deleteCampaign(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.freeRideCampaignUrlDelete}/${id}`, null);
  }

}
