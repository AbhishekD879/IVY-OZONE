import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Football3DBanner } from '../../models/football3dbanner.model';
import { Order } from '../../models/order.model';

@Injectable()
export class Football3dBannersService extends AbstractService<Configuration> {
  Football3DBannersByBrandUrl: string = `football-3d-banner/brand/${this.brand}`;
  Football3DBannersUrl: string = 'football-3d-banner';
  Football3DBannersOrderUrl: string = 'football-3d-banner/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getFootball3DFootball3DBanners(): Observable<HttpResponse<Football3DBanner[]>> {
    return this.sendRequest<Football3DBanner[]>('get', this.Football3DBannersByBrandUrl, null);
  }

  public getSingleFootball3DBanner(id: string): Observable<HttpResponse<Football3DBanner>> {
    const url = `${this.Football3DBannersUrl}/${id}`;
    return this.sendRequest<Football3DBanner>('get', url, null);
  }

  public postNewFootball3DBanner(football3DBanner: Football3DBanner): Observable<HttpResponse<Football3DBanner>> {
    return this.sendRequest<Football3DBanner>('post', this.Football3DBannersUrl, football3DBanner);
  }

  public postNewFootball3DBannerImage(id: string, file: FormData): Observable<HttpResponse<Football3DBanner>> {
    const apiUrl = `football-3d-banner/${id}/image`;

    return this.sendRequest<Football3DBanner>('post', apiUrl, file);
  }

  public removeFootball3DBannerImage(id: string): Observable<HttpResponse<Football3DBanner>> {
    const apiUrl = `football-3d-banner/${id}/image`;
    return this.sendRequest<Football3DBanner>('delete', apiUrl, null);
  }

  public putFootball3DBannerChanges(football3DBannerData: Football3DBanner): Observable<HttpResponse<Football3DBanner>> {
    const apiUrl = `${this.Football3DBannersUrl}/${football3DBannerData.id}`;

    return this.sendRequest<Football3DBanner>('put', apiUrl, football3DBannerData);
  }

  public postNewFootball3DBannersOrder(Football3DBannersOrder: Order): Observable<HttpResponse<Football3DBanner[]>> {
    return this.sendRequest<Football3DBanner[]>('post', this.Football3DBannersOrderUrl, Football3DBannersOrder);
  }

  public deleteFootball3DBanner(id: string): Observable<HttpResponse<void>> {
    const url = `${this.Football3DBannersUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
