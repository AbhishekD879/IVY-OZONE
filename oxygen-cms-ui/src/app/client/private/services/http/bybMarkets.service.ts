import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { BybMarket } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class BybMarketsService extends AbstractService<BybMarket> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'byb-market';
  }

  public findAllMarkets(): Observable<HttpResponse<BybMarket[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BybMarket[]>('get', uri, null);
  }

  public createMarket(market: BybMarket): Observable<HttpResponse<BybMarket>> {
    return this.sendRequest<BybMarket>('post', this.uri, market);
  }

  public getSingleMarket(id: string): Observable<HttpResponse<BybMarket>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BybMarket>('get', uri, null);
  }

  public editMarket(market: BybMarket): Observable<HttpResponse<BybMarket>> {
    const uri = `${this.uri}/${market.id}`;
    return this.sendRequest<BybMarket>('put', uri, market);
  }

  public deleteMarket(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public postNewMarketsOrder(marketsOrder: Order): Observable<HttpResponse<BybMarket[]>> {
    return this.sendRequest<BybMarket[]>('post', `${this.uri}/ordering`, marketsOrder);
  }
}
