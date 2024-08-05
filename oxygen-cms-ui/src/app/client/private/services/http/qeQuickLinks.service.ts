import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';

@Injectable()
export class QEQuickLinksService extends AbstractService<QEQuickLinks> {
  uri: string = 'question-engine/quick-links';
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public findAll(): Observable<HttpResponse<QEQuickLinks[]>> {
    return this.sendRequest<QEQuickLinks[]>('get', this.uri, null);
  }

  public findAllByBrand(): Observable<HttpResponse<QEQuickLinks[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<QEQuickLinks[]>('get', uri, null);
  }

  public findOne(id: string): Observable<HttpResponse<QEQuickLinks>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<QEQuickLinks>('get', uri, null);
  }
  public save(qeQuickLinks: QEQuickLinks): Observable<HttpResponse<QEQuickLinks>> {
    const uri = `${this.uri}`;
    return this.sendRequest<QEQuickLinks>('post', uri, qeQuickLinks);
  }

  public update(qeQuickLinks: QEQuickLinks): Observable<HttpResponse<QEQuickLinks>> {
    const uri = `${this.uri}/${qeQuickLinks.id}`;
    return this.sendRequest<QEQuickLinks>('put', uri, qeQuickLinks);
  }

  public delete(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
