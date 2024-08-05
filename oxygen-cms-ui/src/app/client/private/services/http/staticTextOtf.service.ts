import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Order } from '../../models/order.model';
import {StaticTextOtf} from '../../models/staticTextOtf.model';

@Injectable()
export class StaticTextOtfService extends AbstractService<Configuration> {
  staticTextOtfByBrandUrl: string = `static-text-otf/brand/${this.brand}`;
  staticTextOtfUrl: string = 'static-text-otf';
  staticTextOtfOrderUrl: string = 'static-text-otf/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getStaticTextOtfs(): Observable<HttpResponse<StaticTextOtf[]>> {
    return this.sendRequest<StaticTextOtf[]>('get', this.staticTextOtfByBrandUrl, null);
  }

  public getSingleStaticTextOtf(id: string): Observable<HttpResponse<StaticTextOtf>> {
    const url = `${this.staticTextOtfUrl}/${id}`;
    return this.sendRequest<StaticTextOtf>('get', url, null);
  }

  public postNewStaticTextOtf(staticText: StaticTextOtf): Observable<HttpResponse<StaticTextOtf>> {
    return this.sendRequest<StaticTextOtf>('post', this.staticTextOtfUrl, staticText);
  }

  public putStaticTextOtfChanges(id: string, staticText: StaticTextOtf): Observable<HttpResponse<StaticTextOtf>> {
    const apiUrl = `${this.staticTextOtfUrl}/${id}`;

    return this.sendRequest<StaticTextOtf>('put', apiUrl, staticText);
  }

  public postNewStaticTextOtfOrder(staticTextOtfOrder: Order): Observable<HttpResponse<StaticTextOtf[]>> {
    return this.sendRequest<StaticTextOtf[]>('post', this.staticTextOtfOrderUrl, staticTextOtfOrder);
  }

  public deleteStaticTextOtf(id: string): Observable<HttpResponse<void>> {
    const url = `${this.staticTextOtfUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
