import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { BetReceiptBanner } from '../../models/betreceiptbanner.model';
import { Order } from '../../models/order.model';

@Injectable()
export class BetReceiptMobileBannerService extends AbstractService<BetReceiptBanner[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `bet-receipt-banner`;
  }

  public findAllByBrand(): Observable<HttpResponse<BetReceiptBanner[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BetReceiptBanner[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(banner: BetReceiptBanner): Observable<HttpResponse<BetReceiptBanner>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<BetReceiptBanner>('post', uri, banner);
  }

  public getById(id: string): Observable<HttpResponse<BetReceiptBanner>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BetReceiptBanner>('get', uri, null);
  }

  public edit(banner: BetReceiptBanner): Observable<HttpResponse<BetReceiptBanner>> {
    const uri = `${this.uri}/${banner.id}`;
    return this.sendRequest<BetReceiptBanner>('put', uri, banner);
  }

  public postNewBannerImage(id: string, file: FormData): Observable<HttpResponse<BetReceiptBanner>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<BetReceiptBanner>('post', apiUrl, file);
  }

  public removeBannerImage(id: string): Observable<HttpResponse<BetReceiptBanner>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<BetReceiptBanner>('delete', apiUrl, null);
  }

  public postNewBannersOrder(betReceiptBanner: Order): Observable<HttpResponse<BetReceiptBanner[]>> {
    const apiUrl = `${this.uri}/ordering`;
    return this.sendRequest<BetReceiptBanner[]>('post', apiUrl, betReceiptBanner);
  }
}
