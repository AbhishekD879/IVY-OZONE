import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {ExternalLink} from '../../models/externalLink.model';

@Injectable()
export class ExternalLinkService extends AbstractService<ExternalLink[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `external-link`;
  }

  public findAllByBrand(): Observable<HttpResponse<ExternalLink[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<ExternalLink[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(externalLink: ExternalLink): Observable<HttpResponse<ExternalLink>> {
    const uri = `${this.uri}`;
    return this.sendRequest<ExternalLink>('post', uri, externalLink);
  }

  public getById(id: string): Observable<HttpResponse<ExternalLink>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<ExternalLink>('get', uri, null);
  }

  public edit(externalLink: ExternalLink): Observable<HttpResponse<ExternalLink>> {
    const uri = `${this.uri}/${externalLink.id}`;
    return this.sendRequest<ExternalLink>('put', uri, externalLink);
  }
}
