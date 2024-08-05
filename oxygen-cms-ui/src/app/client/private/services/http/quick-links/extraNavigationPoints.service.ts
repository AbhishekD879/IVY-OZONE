import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { ExtraNavigationPoint } from '../../../models';
import { Order } from '@app/client/private/models/order.model';

@Injectable()
export class ExtraNavigationPointsService extends AbstractService<ExtraNavigationPoint | ExtraNavigationPoint[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'extra-navigation-points';
  }

  public findAllByBrand(): Observable<HttpResponse<ExtraNavigationPoint[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<ExtraNavigationPoint[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<ExtraNavigationPoint>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<ExtraNavigationPoint>('get', uri, null);
  }

  public save(extraNavigationPoint: ExtraNavigationPoint): Observable<HttpResponse<ExtraNavigationPoint>> {
    const uri = `${this.uri}`;
    return this.sendRequest<ExtraNavigationPoint>('post', uri, extraNavigationPoint);
  }

  public update(extraNavigationPoint: ExtraNavigationPoint): Observable<HttpResponse<ExtraNavigationPoint>> {
    const uri = `${this.uri}/${extraNavigationPoint.id}`;
    return this.sendRequest<ExtraNavigationPoint>('put', uri, extraNavigationPoint);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  /**
   * retrieve the list of ExtraNavigationPoint items List
   */
  public getList(): Observable<HttpResponse<ExtraNavigationPoint[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<ExtraNavigationPoint[]>('get', uri, null);
  }

  /**
   * sort the ExtraNavigationPoint point list
   * @param order row order
   * @returns 
   */
  public reorderNavigationPoints(order: Order): Observable<HttpResponse<ExtraNavigationPoint[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<ExtraNavigationPoint[]>('post', uri, order);
  }
}
