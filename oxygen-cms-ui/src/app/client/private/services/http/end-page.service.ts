import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {EndPage} from '@app/client/private/models/end-page.model';

@Injectable()
export class EndPageService extends AbstractService<Configuration> {
  endPageBaseUrl: string = 'end-page';
  endPageByBrandUrl: string = `end-page/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getEndPages(): Observable<HttpResponse<EndPage[]>> {
    return this.sendRequest<EndPage[]>('get', this.endPageBaseUrl, null);
  }

  public getEndPagesByBrand(): Observable<HttpResponse<EndPage[]>> {
    return this.sendRequest<EndPage[]>('get', this.endPageByBrandUrl, null);
  }

  public getSingleEndPage(id: string): Observable<HttpResponse<EndPage>> {
    const url = `${this.endPageBaseUrl}/${id}`;
    return this.sendRequest<EndPage>('get', url, null);
  }

  public saveNewEndPage(endPage: EndPage): Observable<HttpResponse<EndPage>> {
    return this.sendRequest<EndPage>('post', this.endPageBaseUrl, endPage);
  }

  public updateEndPage(id: string, endPage: EndPage): Observable<HttpResponse<EndPage>> {
    const apiUrl = `${this.endPageBaseUrl}/${id}`;
    return this.sendRequest<EndPage>('put', apiUrl, endPage);
  }

  public deleteEndPage(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.endPageBaseUrl}/${id}`, null);
  }

  public uploadBackground(id: string, background: FormData): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('post', `${this.endPageBaseUrl}/${id}/background`, background);
  }
}
