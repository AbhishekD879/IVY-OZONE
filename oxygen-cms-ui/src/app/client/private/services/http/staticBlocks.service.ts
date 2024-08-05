import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {StaticBlock} from '../../models/staticblock.model';

@Injectable()
export class StaticBlocksService extends AbstractService<StaticBlock[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `static-block/brand`;
  }

  public findAllByBrand(): Observable<HttpResponse<StaticBlock[]>> {
    const uri = `${this.uri}/${this.brand}`;
    return this.sendRequest<StaticBlock[]>('get', uri, null);
  }

  public remove(id: string):  Observable<HttpResponse<void>> {
    const uri = `static-block/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public add(staticblock: StaticBlock): Observable<HttpResponse<StaticBlock>> {
    const uri = `static-block/`;
    return this.sendRequest<StaticBlock>('post', uri, staticblock);
  }

  public getById(id: string): Observable<HttpResponse<StaticBlock>>  {
    const uri = `static-block/${id}`;
    return this.sendRequest<StaticBlock>('get', uri, null);
  }

  public edit(staticblock: StaticBlock): Observable<HttpResponse<StaticBlock>> {
    const uri = `static-block/${staticblock.id}`;
    return this.sendRequest<StaticBlock>('put', uri, staticblock);
  }
}
