import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { GamingSubMenu } from '../../models/gaming-submenu.model';
import { Order } from '../../models/order.model';

@Injectable()
export class GamingSubMenuService extends AbstractService<GamingSubMenu> {
  uri: string = 'game-menu';
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public findAll(): Observable<HttpResponse<GamingSubMenu[]>> {
    return this.sendRequest<GamingSubMenu[]>('get', this.uri, null);
  }

  public findAllByBrand(): Observable<HttpResponse<GamingSubMenu[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<GamingSubMenu[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<GamingSubMenu>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<GamingSubMenu>('get', uri, null);
  }
  public save(gamingSubMenu: GamingSubMenu): Observable<HttpResponse<GamingSubMenu>> {
    const uri = `${this.uri}`;
    return this.sendRequest<GamingSubMenu>('post', uri, gamingSubMenu);
  }

  public update(gamingSubMenu: GamingSubMenu): Observable<HttpResponse<GamingSubMenu>> {
    const uri = `${this.uri}/${gamingSubMenu.id}`;
    return this.sendRequest<GamingSubMenu>('put', uri, gamingSubMenu);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<GamingSubMenu[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<GamingSubMenu[]>('post', uri, obj);
  }

  public uploadPng(id: string, file: FormData): Observable<HttpResponse<GamingSubMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<GamingSubMenu>('post', uri, file);
  }

  public removePng(id: string): Observable<HttpResponse<GamingSubMenu>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<GamingSubMenu>('delete', uri, null);
  }
}
