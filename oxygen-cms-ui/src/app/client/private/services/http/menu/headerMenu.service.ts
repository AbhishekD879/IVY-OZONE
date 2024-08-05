import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { HeaderMenu } from '../../../models/headermenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class HeaderMenuService extends AbstractService<HeaderMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `header-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<HeaderMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<HeaderMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<HeaderMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<HeaderMenu>('get', uri, null);
  }
  public save(headerMenu: HeaderMenu): Observable<HttpResponse<HeaderMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<HeaderMenu>('post', uri, headerMenu);
  }

  public update(headerMenu: HeaderMenu): Observable<HttpResponse<HeaderMenu>> {
    const uri = `${this.uri}/${headerMenu.id}`;
    return this.sendRequest<HeaderMenu>('put', uri, headerMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<HeaderMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<HeaderMenu[]>('post', uri, obj);
  }
}
