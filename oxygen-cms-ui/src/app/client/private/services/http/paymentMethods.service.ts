import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from './transport/abstract.service';
import { PaymentMethod } from '../../models/paymentMethod.model';
import { Order } from '../../models/order.model';

@Injectable()
export class PaymentMethodsService extends AbstractService<PaymentMethod[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `payment-methods`;
  }

  public findAllByBrand(): Observable<HttpResponse<PaymentMethod[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<PaymentMethod[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(paymentMethod: PaymentMethod): Observable<HttpResponse<PaymentMethod>> {
    const uri = `${this.uri}`;
    return this.sendRequest<PaymentMethod>('post', uri, paymentMethod);
  }

  public getById(id: string): Observable<HttpResponse<PaymentMethod>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<PaymentMethod>('get', uri, null);
  }

  public edit(paymentMethod: PaymentMethod): Observable<HttpResponse<PaymentMethod>> {
    const uri = `${this.uri}/${paymentMethod.id}`;
    return this.sendRequest<PaymentMethod>('put', uri, paymentMethod);
  }

  public postNewOrder(newOrder: Order): Observable<HttpResponse<PaymentMethod[]>>  {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<PaymentMethod[]>('post', uri, newOrder);
  }
}
