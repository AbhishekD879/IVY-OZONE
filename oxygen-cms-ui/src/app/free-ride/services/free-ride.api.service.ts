import { Injectable } from '@angular/core';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http/index';
import 'rxjs/add/operator/catch';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { Campaign } from '@app/client/private/models/freeRideCampaign.model';
import { FreeRideSplashPageModel } from '../splash-page/model/splash-page.model';

@Injectable()
export class FreeRideAPIService {
  constructor(private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) { }

  /**
* Wrap request to handle success/error.
* @param observableDate
*/
wrappedObservable(observableDate) {
  return observableDate
    .map(res => {
      this.globalLoaderService.hideLoader();
      return res;
    })
    .catch(response => {
      if (response instanceof HttpErrorResponse && response.status !== 400) {
        this.handleRequestError(response.error);
      }

      this.globalLoaderService.hideLoader();
      return Observable.throw(response);
    });
}

  /**
 * Handle networking error.
 * Notify user.
 */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }

  /**
   * Get Splash Screen data.
   * @returns {Observable<HttpResponse<any>>}
   */
  getAllSplashData() {
    const data = this.apiClientService.freeRideService().getAllSplashData();
    return this.wrappedObservable(data.map(res => res.body));
  }

  /**
   * Save/Update Splash Screen data.
   * @returns {Observable<HttpResponse<FreeRideSplashPageModel>>}
   */
  splashData(splashData: FormData, id: string): Observable<FreeRideSplashPageModel> {
    const data = id
      ? this.apiClientService.freeRideService().updateSplashData(splashData, id)
      : this.apiClientService.freeRideService().postSplashData(splashData);
    return this.wrappedObservable(data);
  }

  /**
 * Submit new created campaign
 * @param newCampaign
 * @returns {any}
 */
  postNewCampaign(newCampaign: Campaign) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.freeRideService().postNewCampaign(newCampaign);
    return this.wrappedObservable(getData);
  }

  /**
* Submit updated  campaign
* @param newCampaign
* @returns {any}
*/
  updateCampaign(campaign: any, flag: boolean): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.freeRideService().updateCampaign(campaign.id, campaign, flag);
    return this.wrappedObservable(data);
  }

  /**
 * Load single campaign data to edit
 * @param {string} id
 * @returns {any}
 */
  getSingleCampaignData(id: string) {
    const getData = this.apiClientService.freeRideService().getSingleCampaign(id);
    return this.wrappedObservable(getData);
  }

  /**
     * Create Pots to Campaign
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  createPots(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.freeRideService().createPots(id);
    return this.wrappedObservable(getData);
  }


/**
     * Delete Campaign
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  deleteCampaign(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.freeRideService().deleteCampaign(id);
    return this.wrappedObservable(data);
  }

  /**
     * get Campaign
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  getCampaignsByBrandWithOrdering(sortParamValue: string): Observable<Campaign> {
    const data = this.apiClientService.freeRideService().getCampaignsByBrandWithOrdering(sortParamValue);
    return this.wrappedObservable(data.map(res => res.body));
  }

  /**
     * View Pots to Campaign
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  getViewPotsData(campaignId: string) {
     const data = this.apiClientService.freeRideService().getViewPotsData(campaignId);
     return this.wrappedObservable(data);
  }
}
