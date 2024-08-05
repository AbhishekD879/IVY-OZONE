import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Campaign} from '@app/client/private/models/campaign.model';

@Injectable()
export class CampaignService extends AbstractService<Configuration> {
  campaignBaseUrl: string = 'timeline/campaign';
  campaignByBrandUrl: string = `timeline/campaign/brand/${this.brand}`;
  sortParamName: string = `sort`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getCampaigns(): Observable<HttpResponse<Campaign[]>> {
    return this.sendRequest<Campaign[]>('get', this.campaignBaseUrl, null);
  }

  public getCampaignsByBrand(): Observable<HttpResponse<Campaign[]>> {
    return this.sendRequest<Campaign[]>('get', this.campaignByBrandUrl, null);
  }

  public getCampaignsByBrandWithOrdering(sortParamValue: string): Observable<HttpResponse<Campaign[]>> {
    return this.sendRequest<Campaign[]>('get', `${this.campaignByBrandUrl}?${this.sortParamName}=${sortParamValue}`, null);
  }

  public getSingleCampaign(id: string): Observable<HttpResponse<Campaign>> {
    const url = `${this.campaignBaseUrl}/${id}`;
    return this.sendRequest<Campaign>('get', url, null);
  }

  public saveCampaign(campaign: Campaign): Observable<HttpResponse<Campaign>> {
    return this.sendRequest<Campaign>('post', this.campaignBaseUrl, campaign);
  }

  public updateCampaign(id: string, campaign: Campaign): Observable<HttpResponse<Campaign>> {
    const apiUrl = `${this.campaignBaseUrl}/${id}`;
    return this.sendRequest<Campaign>('put', apiUrl, campaign);
  }

  public deleteCampaign(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.campaignBaseUrl}/${id}`, null);
  }
}
