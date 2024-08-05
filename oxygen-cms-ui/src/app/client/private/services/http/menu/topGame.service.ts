import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { TopGame } from '../../../models/topgame.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class TopGameService extends AbstractService<TopGame> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `top-game`;
  }

  public findAllByBrand(): Observable<HttpResponse<TopGame[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<TopGame[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<TopGame>('get', uri, null);
  }
  public save(topGame: TopGame): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}`;
    return this.sendRequest<TopGame>('post', uri, topGame);
  }

  public update(topGame: TopGame): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${topGame.id}`;
    return this.sendRequest<TopGame>('put', uri, topGame);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<TopGame[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<TopGame[]>('post', uri, obj);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<TopGame>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${id}/image`;
    return this.sendRequest<TopGame>('delete', uri, null);
  }

  public uploadIcon(id: string, file: FormData): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<TopGame>('post', uri, file);
  }

  public removeIcon(id: string): Observable<HttpResponse<TopGame>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<TopGame>('delete', uri, null);
  }
}
