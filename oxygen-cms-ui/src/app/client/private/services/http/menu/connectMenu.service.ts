import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { ConnectMenu } from '../../../models/connectmenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class ConnectMenuService extends AbstractService<ConnectMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `connect-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<ConnectMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<ConnectMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<ConnectMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<ConnectMenu>('get', uri, null);
  }
  public save(connectMenu: ConnectMenu): Observable<HttpResponse<ConnectMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<ConnectMenu>('post', uri, connectMenu);
  }

  public update(connectMenu: ConnectMenu): Observable<HttpResponse<ConnectMenu>> {
    const uri = `${this.uri}/${connectMenu.id}`;
    return this.sendRequest<ConnectMenu>('put', uri, connectMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<ConnectMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<ConnectMenu[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<ConnectMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<ConnectMenu>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<ConnectMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<ConnectMenu>('delete', uri, null);
  }
}
