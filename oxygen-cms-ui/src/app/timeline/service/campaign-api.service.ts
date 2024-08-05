import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Campaign} from '@app/client/private/models/campaign.model';

@Injectable()
export class CampaignApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate): Observable<any> {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  handleRequestError(error): void {
    this.globalLoaderService.hideLoader();
  }

  hideLoader(): void {
    this.globalLoaderService.hideLoader();
  }

  getCampaigns(): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.campaignService().getCampaigns();
    return this.wrappedObservable(data);
  }

  getCampaignsByBrand(): Observable<any> {
    const data = this.apiClientService.campaignService().getCampaignsByBrand();
    return this.wrappedObservable(data);
  }

  getCampaignsByBrandWithOrdering(sortParamValue: string): Observable<any> {
    const data = this.apiClientService.campaignService().getCampaignsByBrandWithOrdering(sortParamValue);
    return this.wrappedObservable(data);
  }

  getCampaign(id: string): Observable<any> {
    const data = this.apiClientService.campaignService().getSingleCampaign(id);
    return this.wrappedObservable(data);
  }

  createCampaign(campaign: Campaign): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.campaignService().saveCampaign(campaign);
    return this.wrappedObservable(data);
  }

  updateCampaign(campaign: Campaign): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.campaignService().updateCampaign(campaign.id, campaign);
    return this.wrappedObservable(data);
  }

  deleteCampaign(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.campaignService().deleteCampaign(id);
    return this.wrappedObservable(data);
  }

  republishPosts(campaignId: string): Observable<any> {
    const data = this.apiClientService.postService().republishByCampaignId(campaignId);
    return this.wrappedObservable(data);
  }
}
