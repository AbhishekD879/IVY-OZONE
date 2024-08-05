import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from './transport/abstract.service';
import { ModuleRibbonTab } from '../../models/moduleribbontab.model';
import { Order } from '../../models/order.model';

@Injectable()
export class ModuleRibbonService extends AbstractService<ModuleRibbonTab[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `module-ribbon-tab`;
  }

  public findAllTabs(): Observable<HttpResponse<ModuleRibbonTab[]>> {
    const uri = `${this.uri}`;
    return this.sendRequest<ModuleRibbonTab[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(moduleRibbonTab: ModuleRibbonTab): Observable<HttpResponse<ModuleRibbonTab>> {
    const uri = `${this.uri}`;
    return this.sendRequest<ModuleRibbonTab>('post', uri, moduleRibbonTab);
  }

  public getById(id: string): Observable<HttpResponse<ModuleRibbonTab>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<ModuleRibbonTab>('get', uri, null);
  }

  public udpate(moduleRibbonTab: ModuleRibbonTab): Observable<HttpResponse<ModuleRibbonTab>> {
    const uri = `${this.uri}/${moduleRibbonTab.id}`;
    return this.sendRequest<ModuleRibbonTab>('put', uri, moduleRibbonTab);
  }

  public setOrder(tabsOrder: Order): Observable<HttpResponse<ModuleRibbonTab[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<ModuleRibbonTab[]>('post', uri, tabsOrder);
  }

  public getByBrand(): Observable<HttpResponse<ModuleRibbonTab[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<ModuleRibbonTab[]>('get', uri, null);
  }

  /**
     * retrieve the list of ModuleRibbonTab items based on segment selection
     * @param segment value selcted via dropdown selection
     * @returns 
     */
  public getModuleRibbonBySegment(segment: string): Observable<HttpResponse<ModuleRibbonTab[]>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}`;
    return this.sendRequest<ModuleRibbonTab[]>('get', uri, null);
  }
}
