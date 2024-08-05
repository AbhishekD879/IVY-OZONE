import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { CouponSegment } from '@app/client/private/models/footballcoupon.model';
import { Order } from '@app/client/private/models/order.model';

@Injectable()
export class FootballCouponService extends AbstractService<CouponSegment[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `coupon-segment`;
  }

  public findAllByBrand(): Observable<HttpResponse<CouponSegment[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<CouponSegment[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(couponSegment: CouponSegment): Observable<HttpResponse<CouponSegment>> {
    const uri = `${this.uri}`;
    return this.sendRequest<CouponSegment>('post', uri, couponSegment);
  }

  public getById(id: string): Observable<HttpResponse<CouponSegment>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<CouponSegment>('get', uri, null);
  }

  public edit(couponSegment: CouponSegment): Observable<HttpResponse<CouponSegment>> {
    const uri = `${this.uri}/${couponSegment.id}`;
    return this.sendRequest<CouponSegment>('put', uri, couponSegment);
  }

  public reorder(obj: Order): Observable<HttpResponse<CouponSegment[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<CouponSegment[]>('post', uri, obj);
  }
}
