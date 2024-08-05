import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { StatContentInfo,StaticEventTitle } from '../../models/statContentInfo.model';

@Injectable()
export class StatContentInfoService extends AbstractService<StatContentInfo[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `statistic-content`;
  }

  public findAllByBrand(): Observable<HttpResponse<StatContentInfo[]>> {
    const uri = `${this.uri}/brand/${this.brand}`; // ToDo: Add logic for getting brand
    return this.sendRequest<StatContentInfo[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(staticContent: StatContentInfo): Observable<HttpResponse<StatContentInfo>> {
    const uri = `${this.uri}/`;
    return this.sendRequest<StatContentInfo>('post', uri, staticContent);
  }

  public getById(id: string): Observable<HttpResponse<StatContentInfo>>  {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<StatContentInfo>('get', uri, null);
  }

  public edit(staticContent: StatContentInfo): Observable<HttpResponse<StatContentInfo>> {
    const uri = `${this.uri}/${staticContent.id}`;
    return this.sendRequest<StatContentInfo>('put', uri, staticContent);
  }
  public getEventTitleById(id: string): Observable<HttpResponse<StaticEventTitle>>  {
    const uri = `${this.uri}/${this.brand}/${id}`;
    return this.sendRequest<StaticEventTitle>('get', uri, null);
  }
}
