import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable} from 'rxjs/Observable';
import { Sport } from '../../models/sport.model';
import { OlympicsImageRequestOptions } from '../../models/olympicsImageRequestOptions';
import { Order } from '../../models/order.model';

@Injectable()
export class OlympicsPageService extends AbstractService<Configuration> {
  olympicsPageUrl: string = 'sports';
  olympicsByBrandUrl: string = `sports/?brand=${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOlympicsPageList(): Observable<HttpResponse<Sport[]>> {
    return this.sendRequest<Sport[]>('get', this.olympicsByBrandUrl, null);
  }

  public getSingleOlympicsPage(id: string): Observable<HttpResponse<Sport>> {
    const url = `${this.olympicsPageUrl}/${id}`;
    return this.sendRequest<Sport>('get', url, null);
  }

  public postOlympicsFilename(id: string, file: FormData): Observable<HttpResponse<Sport>> {
    const url = `${this.olympicsPageUrl}/${id}/files`;
    return this.sendRequest<Sport>('post', url, file);
  }

  public deleteOlympicsFilename(id: string, options: OlympicsImageRequestOptions): Observable<HttpResponse<Sport>> {
    const url = `${this.olympicsPageUrl}/${id}/files`;
    return this.sendRequest<Sport>('delete', url, options);
  }

  public postNewOlympicsPage(sportData: Sport): Observable<HttpResponse<Sport>> {
    return this.sendRequest<Sport>('post', this.olympicsPageUrl, sportData);
  }

  public putOlympicsPageChanges(id: string, sportData: Sport): Observable<HttpResponse<Sport>> {
    const url = `${this.olympicsPageUrl}/${id}`;
    return this.sendRequest<Sport>('put', url, sportData);
  }

  public deleteOlympicsPage(id: string): Observable<HttpResponse<void>> {
    const url = `${this.olympicsPageUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<Sport[]>> {
    const uri = `${this.olympicsPageUrl}/ordering`;
    return this.sendRequest<Sport[]>('post', uri, obj);
  }
}
