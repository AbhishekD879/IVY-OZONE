import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { UserMenu } from '../../../models/usermenu.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class UserMenuService extends AbstractService<UserMenu> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `user-menu`;
  }

  public findAllByBrand(): Observable<HttpResponse<UserMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<UserMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<UserMenu>('get', uri, null);
  }
  public save(userMenu: UserMenu): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<UserMenu>('post', uri, userMenu);
  }

  public update(userMenu: UserMenu): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${userMenu.id}`;
    return this.sendRequest<UserMenu>('put', uri, userMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<UserMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<UserMenu[]>('post', uri, obj);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<UserMenu>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<UserMenu>('delete', uri, null);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<UserMenu>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<UserMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<UserMenu>('delete', uri, null);
  }
}
