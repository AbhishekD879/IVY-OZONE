import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { NavigationPoint } from '../../../models';
import { Order } from '@app/client/private/models/order.model';

@Injectable()
export class NavigationPointsService extends AbstractService<NavigationPoint | NavigationPoint[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'navigation-points';
  }

  public findAllByBrand(): Observable<HttpResponse<NavigationPoint[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<NavigationPoint[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<NavigationPoint>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<NavigationPoint>('get', uri, null);
  }

  public save(navigationPoint: NavigationPoint): Observable<HttpResponse<NavigationPoint>> {
    const uri = `${this.uri}`;
    return this.sendRequest<NavigationPoint>('post', uri, navigationPoint);
  }

  public update(navigationPoint: NavigationPoint): Observable<HttpResponse<NavigationPoint>> {
    const uri = `${this.uri}/${navigationPoint.id}`;
    return this.sendRequest<NavigationPoint>('put', uri, navigationPoint);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  /**
   * retrieve the list of NavigationPoints items based on segment selection
   * @param segment value seelcted via dropdown selection
   * @returns 
   */
  public getListBySegment(segment: String): Observable<HttpResponse<NavigationPoint[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}`;
    return this.sendRequest<NavigationPoint[]>('get', uri, null);
  }

  /**
   * sort the navigation point list
   * @param order row order
   * @returns 
   */
  public reorderNavigationPoints(order: Order): Observable<HttpResponse<NavigationPoint[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<NavigationPoint[]>('post', uri, order);
  }
}
