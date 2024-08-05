import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { BottomMenu } from '../../../models/bottommenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class BottomMenuService extends AbstractService<BottomMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `bottom-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<BottomMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<BottomMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<BottomMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<BottomMenu>('get', uri, null);
  }
  public save(bottomMenu: BottomMenu): Observable<HttpResponse<BottomMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<BottomMenu>('post', uri, bottomMenu);
  }

  public update(bottomMenu: BottomMenu): Observable<HttpResponse<BottomMenu>> {
    const uri = `${this.uri}/${bottomMenu.id}`;
    return this.sendRequest<BottomMenu>('put', uri, bottomMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<BottomMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<BottomMenu[]>('post', uri, obj);
  }
}
