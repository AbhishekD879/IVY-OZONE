import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { INetworkWIndicator } from '../../../../network-indicator/network-indicator-model';



@Injectable()
/**
 * network Indicator service is for save and get data 
 */
export class networkIndicatorService extends AbstractService<Configuration> {
  private readonly NETWORK_INDICATOR_URL: string = `networkIndicator`; 

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the network Indicator by brand
   * @returns {Observable<HttpResponse<INetworkWIndicator>>}
   */
  public getDetailsByBrand(): Observable<HttpResponse<INetworkWIndicator>> {
    return this.sendRequest<INetworkWIndicator>('get', `${this.NETWORK_INDICATOR_URL}/brand/${this.brand}`, null);
  }

  /**
   * To Save Network Indicator
   * @param {INetworkWIndicator} request
   * @returns {Observable<HttpResponse<INetworkWIndicator>>}
   */
  public saveNetworkIndicator(request: INetworkWIndicator): Observable<HttpResponse<INetworkWIndicator>> {
    return this.sendRequest<INetworkWIndicator>('post', this.NETWORK_INDICATOR_URL, request);
  }

  /**
   * To Update Network Indicator
   * @param {INetworkWIndicator} request
   * @returns {Observable<HttpResponse<INetworkWIndicator>>}
   */
  public updateNetworkIndicator(request: INetworkWIndicator): Observable<HttpResponse<INetworkWIndicator>> {
    return this.sendRequest<INetworkWIndicator>('put', `${this.NETWORK_INDICATOR_URL}/${request.id}`, request);
  }
}
