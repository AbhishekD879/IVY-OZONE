import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { HeaderContactMenu } from '../../../models/headercontactmenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class HeaderContactMenuService extends AbstractService<HeaderContactMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `header-contact-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<HeaderContactMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<HeaderContactMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<HeaderContactMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<HeaderContactMenu>('get', uri, null);
  }
  public save(headerContactMenu: HeaderContactMenu): Observable<HttpResponse<HeaderContactMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<HeaderContactMenu>('post', uri, headerContactMenu);
  }

  public update(headerContactMenu: HeaderContactMenu): Observable<HttpResponse<HeaderContactMenu>> {
    const uri = `${this.uri}/${headerContactMenu.id}`;
    return this.sendRequest<HeaderContactMenu>('put', uri, headerContactMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<HeaderContactMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<HeaderContactMenu[]>('post', uri, obj);
  }
}
