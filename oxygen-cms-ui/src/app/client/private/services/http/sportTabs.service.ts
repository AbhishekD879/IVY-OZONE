import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from './transport/abstract.service';
import { Order } from '../../models/order.model';
import { SportTab } from '@app/client/private/models/sporttab.model';

@Injectable()
export class SportTabService extends AbstractService<SportTab[]> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `sport-tab`;
  }

  public findAllByBrandAndSportId(brand: string, sportId: number): Observable<HttpResponse<SportTab[]>> {
    const uri = `${this.uri}/brand/${brand}/sport/${sportId}`;
    return this.sendRequest<SportTab[]>('get', uri, null);
  }

  public getById(id: string): Observable<HttpResponse<SportTab>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SportTab>('get', uri, null);
  }

  public edit(sportTab: SportTab): Observable<HttpResponse<SportTab>> {
    const uri = `${this.uri}/${sportTab.id}`;
    return this.sendRequest<SportTab>('put', uri, sportTab);
  }

  public postNewOrder(newOrder: Order): Observable<HttpResponse<SportTab[]>>  {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<SportTab[]>('post', uri, newOrder);
  }
}
