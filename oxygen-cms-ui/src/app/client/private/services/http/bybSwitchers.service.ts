import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { BYBSwitcher } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class BYBSwitchersService extends AbstractService<BYBSwitcher> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'byb-switcher';
  }

  findAllSwitchers(): Observable<HttpResponse<BYBSwitcher[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BYBSwitcher[]>('get', uri, null);
  }

  createSwitcher(market: BYBSwitcher): Observable<HttpResponse<BYBSwitcher>> {
    return this.sendRequest<BYBSwitcher>('post', this.uri, market);
  }

  getSingleSwitcher(id: string): Observable<HttpResponse<BYBSwitcher>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BYBSwitcher>('get', uri, null);
  }

  editSwitcher(market: BYBSwitcher): Observable<HttpResponse<BYBSwitcher>> {
    const uri = `${this.uri}/${market.id}`;
    return this.sendRequest<BYBSwitcher>('put', uri, market);
  }

  deleteSwitcher(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewSwitchersOrder(marketsOrder: Order): Observable<HttpResponse<BYBSwitcher[]>> {
    return this.sendRequest<BYBSwitcher[]>('post', `${this.uri}/ordering`, marketsOrder);
  }
}
