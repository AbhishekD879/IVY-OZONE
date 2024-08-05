import {AbstractService} from './transport/abstract.service';

import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';


@Injectable()
export class PublicApiService extends AbstractService<any> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = ``;
  }

  public getSystemConfigByBrand(): Observable<HttpResponse<any>> {
    const uri = `${this.brand}/system-configuration`;
    return this.sendRequest<any>('get', uri, null);
  }
}
