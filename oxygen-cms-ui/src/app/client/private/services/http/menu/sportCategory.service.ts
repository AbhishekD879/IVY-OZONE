import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { SportCategory } from '../../../models/sportcategory.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class SportCategoryService extends AbstractService<SportCategory> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `sport-category`;
  }

  public findAllByBrand(): Observable<HttpResponse<SportCategory[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<SportCategory[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<SportCategory>('get', uri, null);
  }
  public save(sportCategory: SportCategory): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}`;
    return this.sendRequest<SportCategory>('post', uri, sportCategory);
  }

  public update(sportCategory: SportCategory): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${sportCategory.id}`;
    return this.sendRequest<SportCategory>('put', uri, sportCategory);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<SportCategory[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<SportCategory[]>('post', uri, obj);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<SportCategory>('post', uri, file);
  }

  public removeSvg(id: string): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<SportCategory>('delete', uri, null);
  }

  public uploadImage(id: string, file: FormData): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<SportCategory>('post', uri, file);
  }

  public removeImage(id: string): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=image`;
    return this.sendRequest<SportCategory>('delete', uri, null);
  }

  public uploadIcon(id: string, file: FormData): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<SportCategory>('post', uri, file);
  }

  public removeIcon(id: string): Observable<HttpResponse<SportCategory>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<SportCategory>('delete', uri, null);
  }

  public sportReorder(obj: Order): Observable<HttpResponse<SportCategory[]>> {
    let uri = `trending-tab/ordering`;
    return this.sendRequest<SportCategory[]>('post', uri, obj);
  }
}
