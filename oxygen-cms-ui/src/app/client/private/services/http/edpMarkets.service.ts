import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { EdpMarket } from '../../models/edpmarket.model';
import { Order } from '../../models/order.model';

@Injectable()
export class EdpMarketsService extends AbstractService<EdpMarket[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `edp-market`;
  }

  public findAllByBrand(): Observable<HttpResponse<EdpMarket[]>> {
    const uri = `${this.uri}/brand/${this.brand}`; // ToDo: Add logic for getting brand
    return this.sendRequest<EdpMarket[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(league: EdpMarket): Observable<HttpResponse<EdpMarket>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<EdpMarket>('post', uri, league);
  }

  public getById(id: string): Observable<HttpResponse<EdpMarket>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<EdpMarket>('get', uri, null);
  }

  public edit(league: EdpMarket): Observable<HttpResponse<EdpMarket>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<EdpMarket>('put', uri, league);
  }

  public postNewOrder(newOrder: Order): Observable<HttpResponse<EdpMarket[]>>  {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<EdpMarket[]>('post', uri, newOrder);
  }
}
