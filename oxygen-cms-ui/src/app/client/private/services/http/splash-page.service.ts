import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import {SplashPage} from '@app/client/private/models/splash-page.model';

@Injectable()
export class SplashPageService extends AbstractService<Configuration> {
  splashPageBaseUrl: string = 'splash-page';
  splashPageByBrandUrl: string = `splash-page/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getSplashPages(): Observable<HttpResponse<SplashPage[]>> {
    return this.sendRequest<SplashPage[]>('get', this.splashPageBaseUrl, null);
  }

  public getSplashPagesByBrand(): Observable<HttpResponse<SplashPage[]>> {
    return this.sendRequest<SplashPage[]>('get', this.splashPageByBrandUrl, null);
  }

  public getSingleSplashPage(id: string): Observable<HttpResponse<SplashPage>> {
    const url = `${this.splashPageBaseUrl}/${id}`;
    return this.sendRequest<SplashPage>('get', url, null);
  }

  public postNewSplashPage(splashPage: SplashPage): Observable<HttpResponse<SplashPage>> {
    return this.sendRequest<SplashPage>('post', this.splashPageBaseUrl, splashPage);
  }

  public putSplashPageChanges(id: string, splashPage: SplashPage): Observable<HttpResponse<SplashPage>> {
    const apiUrl = `${this.splashPageBaseUrl}/${id}`;
    return this.sendRequest<SplashPage>('put', apiUrl, splashPage);
  }

  public deleteSplashPage(id: string): Observable<HttpResponse<SplashPage>> {
    const url = `${this.splashPageBaseUrl}/${id}`;
    return this.sendRequest<SplashPage>('delete', url, null);
  }

  public uploadSvgImage(id: string, file: FormData): Observable<HttpResponse<SplashPage>> {
    const uri = `${this.splashPageBaseUrl}/${id}/file?svg=true`;
    return this.sendRequest<SplashPage>('post', uri, file);
  }

}
