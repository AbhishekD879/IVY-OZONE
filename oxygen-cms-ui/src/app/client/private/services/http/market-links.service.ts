import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { MarketLink } from '../../models/marketLink.model';

@Injectable()
export class MarketLinksService extends AbstractService<MarketLink> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'statistics-links/market-links';
  }

  findAllMarketLinks(): Observable<HttpResponse<MarketLink[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<MarketLink[]>('get', uri, null);
  }

  createMarketLink(link: MarketLink): Observable<HttpResponse<MarketLink>> {
    return this.sendRequest<MarketLink>('post', this.uri, link);
  }

  getSingleMarketLink(id: string): Observable<HttpResponse<MarketLink>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<MarketLink>('get', uri, null);
  }

  editMarketLink(link: MarketLink): Observable<HttpResponse<MarketLink>> {
    const uri = `${this.uri}/${link.id}`;
    return this.sendRequest<MarketLink>('put', uri, link);
  }

  deleteMarketLink(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
