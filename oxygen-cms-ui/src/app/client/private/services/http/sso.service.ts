import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {SsoPage} from '../../models/ssopage.model';
import {Order} from '../../models/order.model';

@Injectable()
export class SsoPagesService extends AbstractService<Configuration> {
  ssoPagesByBrandUrl: string = `sso-page/brand/${this.brand}`;
  ssoPagesUrl: string = 'sso-page';
  ssoPagesOrderUrl: string = 'sso-page/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getSsoPages(): Observable<HttpResponse<SsoPage[]>> {
    return this.sendRequest<SsoPage[]>('get', this.ssoPagesByBrandUrl, null);
  }

  public getSingleSsoPage(id: string): Observable<HttpResponse<SsoPage>> {
    const url = `${this.ssoPagesUrl}/${id}`;
    return this.sendRequest<SsoPage>('get', url, null);
  }

  public postNewSsoPage(ssoPage: SsoPage): Observable<HttpResponse<SsoPage>> {
    return this.sendRequest<SsoPage>('post', this.ssoPagesUrl, ssoPage);
  }

  public postNewSsoPageImage(id: string, file: FormData): Observable<HttpResponse<SsoPage>> {
    const apiUrl = `sso-page/${id}/image`;

    return this.sendRequest<SsoPage>('post', apiUrl, file);
  }

  public removeSsoPageImage(id: string): Observable<HttpResponse<SsoPage>> {
    const apiUrl = `sso-page/${id}/image`;

    return this.sendRequest<SsoPage>('delete', apiUrl, null);
  }

  public putSsoPageChanges(id: string, ssoPageData: SsoPage): Observable<HttpResponse<SsoPage>> {
    const apiUrl = `${this.ssoPagesUrl}/${id}`;

    return this.sendRequest<SsoPage>('put', apiUrl, ssoPageData);
  }

  public postNewSsoPagesOrder(ssoPagesOrder: Order): Observable<HttpResponse<SsoPage[]>> {
    return this.sendRequest<SsoPage[]>('post', this.ssoPagesOrderUrl, ssoPagesOrder);
  }

  public deleteSsoPage(id: string): Observable<HttpResponse<void>> {
    const url = `${this.ssoPagesUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
