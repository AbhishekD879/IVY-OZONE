import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { YourCallMarket } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class YourCallMarketsService extends AbstractService<YourCallMarket> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'your-call-market';
  }

  findAllMarkets(): Observable<HttpResponse<YourCallMarket[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<YourCallMarket[]>('get', uri, null);
  }

  createMarket(market: YourCallMarket): Observable<HttpResponse<YourCallMarket>> {
    return this.sendRequest<YourCallMarket>('post', this.uri, market);
  }

  getSingleMarket(id: string): Observable<HttpResponse<YourCallMarket>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<YourCallMarket>('get', uri, null);
  }

  editMarket(market: YourCallMarket): Observable<HttpResponse<YourCallMarket>> {
    const uri = `${this.uri}/${market.id}`;
    return this.sendRequest<YourCallMarket>('put', uri, market);
  }

  deleteMarket(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewMarketsOrder(marketsOrder: Order): Observable<HttpResponse<YourCallMarket[]>> {
    return this.sendRequest<YourCallMarket[]>('post', `${this.uri}/ordering`, marketsOrder);
  }
}
