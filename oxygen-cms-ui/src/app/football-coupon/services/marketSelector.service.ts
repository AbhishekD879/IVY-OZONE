import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { MarketSelector } from '@app/client/private/models/marketselector.model';
import { Order } from '@app/client/private/models/order.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';

@Injectable()
export class MarketSelectorService extends AbstractService<MarketSelector[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `coupon-market-selector`;
  }

  public findAllByBrand(): Observable<HttpResponse<MarketSelector[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<MarketSelector[]>('get', uri, null);
  }

  public delete(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(marketSelector: MarketSelector): Observable<HttpResponse<MarketSelector>> {
    const uri = `${this.uri}`;
    return this.sendRequest<MarketSelector>('post', uri, marketSelector);
  }

  public getById(id: string): Observable<HttpResponse<MarketSelector>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<MarketSelector>('get', uri, null);
  }

  public edit(marketSelector: MarketSelector): Observable<HttpResponse<MarketSelector>> {
    const uri = `${this.uri}/${marketSelector.id}`;
    return this.sendRequest<MarketSelector>('put', uri, marketSelector);
  }

  public reorder(obj: Order): Observable<HttpResponse<MarketSelector[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<MarketSelector[]>('post', uri, obj);
  }

  /**
   *  Get used templateMarketNames
   */
  public getUsedMarketTemplateNames(): Observable<string[]> {
    return this
      .findAllByBrand()
      .map(response => (response.body as MarketSelector[])
        .map( marketSelector => marketSelector.templateMarketName));
  }
}
