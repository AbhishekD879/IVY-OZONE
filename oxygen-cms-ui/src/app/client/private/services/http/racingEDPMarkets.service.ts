import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { RacingEdpMarket } from '../../models/racing.edpmarket.model';
import { Order } from '../../models/order.model';

@Injectable()
export class RacingEdpMarketsService extends AbstractService<RacingEdpMarket[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `racing-edp-market`;
  }

  public findAllByBrand(): Observable<HttpResponse<RacingEdpMarket[]>> {
    const uri = `${this.uri}/brand/${this.brand}`; // ToDo: Add logic for getting brand
    return this.sendRequest<RacingEdpMarket[]>('get', uri, null);
  }

  public remove(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(market: RacingEdpMarket): Observable<HttpResponse<RacingEdpMarket>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<RacingEdpMarket>('post', uri, market);
  }

  public getById(id: string): Observable<HttpResponse<RacingEdpMarket>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<RacingEdpMarket>('get', uri, null);
  }

  public edit(market: RacingEdpMarket): Observable<HttpResponse<RacingEdpMarket>> {
    const uri = `${this.uri}/${market.id}`;
    return this.sendRequest<RacingEdpMarket>('put', uri, market);
  }

  public postNewOrder(newOrder: Order): Observable<HttpResponse<RacingEdpMarket[]>>  {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<RacingEdpMarket[]>('post', uri, newOrder);
  }

}
