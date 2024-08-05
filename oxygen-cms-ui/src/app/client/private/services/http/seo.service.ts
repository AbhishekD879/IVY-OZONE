import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {SeoPage} from '../../models/seopage.model';

@Injectable()
export class SeoPageService extends AbstractService<Configuration> {
  seoPageUrl: string = 'seo-page';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getSeoPageList(): Observable<HttpResponse<SeoPage[]>> {
    return this.sendRequest<SeoPage[]>('get', `${this.seoPageUrl}/brand/${this.brand}`, null);
  }

  public getSingleSeoPage(id: string): Observable<HttpResponse<SeoPage>> {
    const url = `${this.seoPageUrl}/${id}`;
    return this.sendRequest<SeoPage>('get', url, null);
  }

  public postNewSeoPage(promotion: SeoPage): Observable<HttpResponse<SeoPage>> {
    return this.sendRequest<SeoPage>('post', this.seoPageUrl, promotion);
  }

  public putSeoPageChanges(id: string, prmotionData: SeoPage): Observable<HttpResponse<SeoPage>> {
    const apiUrl = `${this.seoPageUrl}/${id}`;

    return this.sendRequest<SeoPage>('put', apiUrl, prmotionData);
  }

  public deleteSeoPage(id: string): Observable<HttpResponse<void>> {
    const url = `${this.seoPageUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
