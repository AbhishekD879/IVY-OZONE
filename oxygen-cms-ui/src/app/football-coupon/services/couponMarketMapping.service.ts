import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { CouponMarketMapping } from '@app/client/private/models/couponMarketMapping.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';

@Injectable()
export class CouponMarketMappingService extends AbstractService<CouponMarketMapping[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `coupon-market-mapping`;
  }

  public findAllByBrand(): Observable<HttpResponse<CouponMarketMapping[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<CouponMarketMapping[]>('get', uri, null);
  }

  public delete(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(CouponMarketMapping: CouponMarketMapping): Observable<HttpResponse<CouponMarketMapping>> {
    const uri = `${this.uri}`;
    return this.sendRequest<CouponMarketMapping>('post', uri, CouponMarketMapping);
  }

  public getById(id: string): Observable<HttpResponse<CouponMarketMapping>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<CouponMarketMapping>('get', uri, null);
  }

  public edit(CouponMarketMapping: CouponMarketMapping): Observable<HttpResponse<CouponMarketMapping>> {
    const uri = `${this.uri}/${CouponMarketMapping.id}`;
    return this.sendRequest<CouponMarketMapping>('put', uri, CouponMarketMapping);
  }
}
