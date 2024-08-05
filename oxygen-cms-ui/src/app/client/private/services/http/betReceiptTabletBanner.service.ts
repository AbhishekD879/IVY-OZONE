import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { BetReceiptBannerTablet } from '../../models/betreceiptbannertablet.model';
import { Order } from '../../models/order.model';

@Injectable()
export class BetReceiptTabletBannerService extends AbstractService<BetReceiptBannerTablet[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `bet-receipt-banner-tablet`;
  }

  public findAllByBrand(): Observable<HttpResponse<BetReceiptBannerTablet[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BetReceiptBannerTablet[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(banner: BetReceiptBannerTablet): Observable<HttpResponse<BetReceiptBannerTablet>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<BetReceiptBannerTablet>('post', uri, banner);
  }

  public getById(id: string): Observable<HttpResponse<BetReceiptBannerTablet>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BetReceiptBannerTablet>('get', uri, null);
  }

  public edit(banner: BetReceiptBannerTablet): Observable<HttpResponse<BetReceiptBannerTablet>> {
    const uri = `${this.uri}/${banner.id}`;
    return this.sendRequest<BetReceiptBannerTablet>('put', uri, banner);
  }

  public postNewBannerImage(id: string, file: FormData): Observable<HttpResponse<BetReceiptBannerTablet>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<BetReceiptBannerTablet>('post', apiUrl, file);
  }

  public removeBannerImage(id: string): Observable<HttpResponse<BetReceiptBannerTablet>> {
    const apiUrl = `${this.uri}/${id}/image`;
    return this.sendRequest<BetReceiptBannerTablet>('delete', apiUrl, null);
  }

  public postNewBannersOrder(betReceiptBanner: Order): Observable<HttpResponse<BetReceiptBannerTablet[]>> {
    const apiUrl = `${this.uri}/ordering`;
    return this.sendRequest<BetReceiptBannerTablet[]>('post', apiUrl, betReceiptBanner);
  }
}
