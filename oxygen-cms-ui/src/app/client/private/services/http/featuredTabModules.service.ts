import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { HomeModule } from '../../models/homemodule.model';
import { FeaturedTabModule } from '../../models/featuredTabModule';
import { FeaturedModuleEventsRequest } from '../../models/featuredModuleEventsRequest';
import { Order } from '../../models/order.model';

@Injectable()
export class FeaturedTabModulesService extends AbstractService<HomeModule[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `home-module`;
  }
  

  public findAllByBrand(isActive: boolean): Observable<HttpResponse<HomeModule[]>> {
    const uri = `${this.uri}/brand/${this.brand}?active=${isActive}`;
    return this.sendRequest<HomeModule[]>('get', uri, null);
  }

  public findAllByEventHubIndex(hubIndex: number): Observable<HttpResponse<HomeModule[]>> {
    // home-module/brand/bma/eventhub/9
    const uri = `${this.uri}/brand/${this.brand}/eventhub/${hubIndex}`;
    return this.sendRequest<HomeModule[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(module: FeaturedTabModule): Observable<HttpResponse<FeaturedTabModule>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<any>('post', uri, module);
  }

  public getById(id: string): Observable<HttpResponse<FeaturedTabModule>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<FeaturedTabModule>('get', uri, null);
  }

  public edit(module: FeaturedTabModule): Observable<HttpResponse<FeaturedTabModule>> {
    const uri = `${this.uri}/${module.id}`;
    return this.sendRequest<FeaturedTabModule>('put', uri, module);
  }

  public loadOpenbetEvents(options: FeaturedModuleEventsRequest): Observable<HttpResponse<any[]>> {
    const uri = `${this.uri}/brand/${this.brand}/ss/event`;
    return this.sendRequest<any>('get', uri, options);
  }

  public reorder(order: Order): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<void>('post', uri, order);
  }

  public findAllByEventHubIndexAndSegment(hubIndex: number, segment: string): Observable<HttpResponse<HomeModule[]>> {
    const uri = `${this.uri}/brand/${this.brand}/eventhub/${hubIndex}/segment/${segment}`;
    return this.sendRequest<HomeModule[]>('get', uri, null);
  }

  public findAllByBrandAndSegment(isActive: boolean, segment: string): Observable<HttpResponse<HomeModule[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}?active=${isActive}`;
    return this.sendRequest<HomeModule[]>('get', uri, null);
  }
}
