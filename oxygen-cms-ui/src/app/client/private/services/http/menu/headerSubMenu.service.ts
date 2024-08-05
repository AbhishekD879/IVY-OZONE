import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { HeaderSubMenu } from '../../../models/headersubmenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class HeaderSubMenuService extends AbstractService<HeaderSubMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `header-submenu`;
  }

  public findAllByBrand(): Observable<HttpResponse<HeaderSubMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<HeaderSubMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<HeaderSubMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<HeaderSubMenu>('get', uri, null);
  }
  public save(headerSubMenu: HeaderSubMenu): Observable<HttpResponse<HeaderSubMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<HeaderSubMenu>('post', uri, headerSubMenu);
  }

  public update(headerSubMenu: HeaderSubMenu): Observable<HttpResponse<HeaderSubMenu>> {
    const uri = `${this.uri}/${headerSubMenu.id}`;
    return this.sendRequest<HeaderSubMenu>('put', uri, headerSubMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<HeaderSubMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<HeaderSubMenu[]>('post', uri, obj);
  }
}
