import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Order} from '@app/client/private/models/order.model';
import {VirtualSportParent} from '@app/client/private/models/virtualSportParent.model';

@Injectable()
export class VirtualSportsService extends AbstractService<Configuration> {
  virtualsBaseUrl: string = 'virtual-sport';
  virtualsByBrandUrl: string = `virtual-sport/brand/${this.brand}`;
  virtualsOrderUrl: string = `virtual-sport/ordering`;
  sortParamName: string = `sort`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }


  public getVirtualSports(): Observable<HttpResponse<any[]>> {
    return this.sendRequest<any[]>('get', this.virtualsBaseUrl, null);
  }


  public getVirtualSportsByBrand(): Observable<HttpResponse<any[]>> {
    return this.sendRequest<any[]>('get', this.virtualsByBrandUrl, null);
  }


  public getVirtualSportsByBrandWithOrdering(sortParamValue: string): Observable<HttpResponse<any[]>> {
    return this.sendRequest<any[]>('get', `${this.virtualsByBrandUrl}?${this.sortParamName}=${sortParamValue}`, null);
  }


  public getSingleVirtualSport(id: string): Observable<HttpResponse<any>> {
    const url = `${this.virtualsBaseUrl}/${id}`;
    return this.sendRequest<any>('get', url, null);
  }


  public saveVirtualSport(virtualSport: any): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.virtualsBaseUrl, virtualSport);
  }


  public updateVirtualSport(id: string, campaign: any): Observable<HttpResponse<any>> {
    const apiUrl = `${this.virtualsBaseUrl}/${id}`;
    return this.sendRequest<any>('put', apiUrl, campaign);
  }


  public deleteVirtualSport(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.virtualsBaseUrl}/${id}`, null);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<any>> {
    const uri = `${this.virtualsBaseUrl}/${id}/icon`;
    return this.sendRequest<any>('post', uri, file);
  }

  public deleteImage(id: string): Observable<HttpResponse<any>> {
    const uri = `${this.virtualsBaseUrl}/${id}/icon`;
    return this.sendRequest<any>('delete', uri, null);
  }

  public postSportsOrder(sportsOrder: Order): Observable<HttpResponse<VirtualSportParent[]>> {
    return this.sendRequest<VirtualSportParent[]>('post', this.virtualsOrderUrl, sportsOrder);
  }
}
