import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { RightMenu } from '../../../models/rightmenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class RightMenuService extends AbstractService<RightMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `right-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<RightMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<RightMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<RightMenu>('get', uri, null);
  }
  public save(rightMenu: RightMenu): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<RightMenu>('post', uri, rightMenu);
  }

  public update(rightMenu: RightMenu): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${rightMenu.id}`;
    return this.sendRequest<RightMenu>('put', uri, rightMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<RightMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<RightMenu[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<RightMenu>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<RightMenu>('delete', uri, null);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<RightMenu>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<RightMenu>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<RightMenu>('delete', uri, null);
  }
}
