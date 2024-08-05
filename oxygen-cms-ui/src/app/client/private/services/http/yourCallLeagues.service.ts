import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { YourCallLeague } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class YourCallLeaguesService extends AbstractService<YourCallLeague> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'your-call-league';
  }

  findAllLeagues(): Observable<HttpResponse<YourCallLeague[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<YourCallLeague[]>('get', uri, null);
  }

  createLeague(league: YourCallLeague): Observable<HttpResponse<YourCallLeague>> {
    return this.sendRequest<YourCallLeague>('post', this.uri, league);
  }

  getSingleLeague(id: string): Observable<HttpResponse<YourCallLeague>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<YourCallLeague>('get', uri, null);
  }

  editLeague(league: YourCallLeague): Observable<HttpResponse<YourCallLeague>> {
    const uri = `${this.uri}/${league.id}`;
    return this.sendRequest<YourCallLeague>('put', uri, league);
  }

  deleteLeague(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewLeaguesOrder(leaguesOrder: Order): Observable<HttpResponse<YourCallLeague[]>> {
    return this.sendRequest<YourCallLeague[]>('post', `${this.uri}/ordering`, leaguesOrder);
  }
}
