import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@root/app/client/private/services/http/transport/abstract.service';
import { BybWidget } from './byb-widget.model';
import { Widget } from '@root/app/client/private/models';
import { Order } from '@root/app/client/private/models/order.model';
import { ModuleRibbonTab } from '@root/app/client/public/models';

@Injectable()
export class BybWidgetService extends AbstractService<BybWidget[]> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `byb-widget`;
  }

  public findAllByBrand(brand: string): Observable<HttpResponse<BybWidget[]>> {
    const uri = `${this.uri}/brand/${brand}`;
    return this.sendRequest<[BybWidget]>('get', uri, null);
  }

  public postNew(newOrder: any): Observable<HttpResponse<BybWidget>> {
    const uri = `byb-widget`;
    return this.sendRequest<BybWidget>('post', uri, newOrder);
  }

  public postNewOrder(newOrder: any): Observable<HttpResponse<BybWidget>> {
      const uri = `byb-widget-data`;
      return this.sendRequest<BybWidget>('post', uri, newOrder);
    }


  public getsegmentdata(brand: string, status: any): Observable<HttpResponse<BybWidget[]>> {
    const uri = `byb-widget-data/brand/${brand}/status`;
    return this.sendRequest<[BybWidget]>('get', uri, status);
  }

  public getById(id: string): Observable<HttpResponse<BybWidget>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BybWidget>('get', uri, null);
  }

  /**
   * @param id 
   * @returns request to delete a autoseopage
   */
  public deleteBybMarket(id: string): Observable<HttpResponse<void>> {
    let uri = `byb-widget-data/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public updateWidgetData(request: Widget): Observable<HttpResponse<Widget>> {
    return this.sendRequest<Widget>('put', `${this.uri}/${request.id}`, request);
  }

  public updateValues(editedFormValues: any): any {
    const uri = `byb-widget-data`;
    return this.sendRequest<any>('put', `${uri}/${editedFormValues.id}`, editedFormValues)
  }

  public reOrder(request: Order): Observable<HttpResponse<Widget>> {
    let uri = `byb-widget-data/ordering`;
    return this.sendRequest<Widget>('post', uri, request);
  }


  public getModuleRibbonBySegment(segment: string): Observable<HttpResponse<ModuleRibbonTab[]>> {
    let uri:any='module-ribbon-tab'
    const uri1 = `${uri}/brand/${this.brand}/segment/${segment}`;
    return this.sendRequest<ModuleRibbonTab[]>('get', uri1, null);
  }

}
