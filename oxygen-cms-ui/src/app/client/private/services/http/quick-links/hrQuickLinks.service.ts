import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from '../transport/abstract.service';
import { HRQuickLink } from '../../../models/hrquicklink.model';
import { Order } from '../../../models/order.model';

@Injectable()
export class HrQuickLinksService extends AbstractService<HRQuickLink> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `hr-quick-link`;
  }

  public findAllByBrand(): Observable<HttpResponse<HRQuickLink[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<HRQuickLink[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<HRQuickLink>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<HRQuickLink>('get', uri, null);
  }
  public save(hrQuickLink: HRQuickLink): Observable<HttpResponse<HRQuickLink>> {
    const uri = `${this.uri}`;
    return this.sendRequest<HRQuickLink>('post', uri, hrQuickLink);
  }

  public update(hrQuickLink: HRQuickLink): Observable<HttpResponse<HRQuickLink>> {
    const uri = `${this.uri}/${hrQuickLink.id}`;
    return this.sendRequest<HRQuickLink>('put', uri, hrQuickLink);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public reorder(obj: Order): Observable<HttpResponse<HRQuickLink[]>> {
    const uri = `${this.uri}/ordering`;
    return this.sendRequest<HRQuickLink[]>('post', uri, obj);
  }

  public uploadIcon(id: string, file: FormData): Observable<HttpResponse<HRQuickLink>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<HRQuickLink>('post', uri, file);
  }

  public removeIcon(id: string): Observable<HttpResponse<HRQuickLink>> {
    const uri = `${this.uri}/${id}/image?fileType=icon`;
    return this.sendRequest<HRQuickLink>('delete', uri, null);
  }
}
