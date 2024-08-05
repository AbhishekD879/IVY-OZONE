import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {
  HttpClient,
  HttpResponse
} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {OtfIosAppToggle} from '@app/client/private/models/otfIosAppToggle.model';

@Injectable()
export class OtfIosAppToggleService extends AbstractService<OtfIosAppToggle> {
  byBrandUrl: string = `otf-ios-app-toggle/brand/${this.brand}`;
  rootUrl: string = 'otf-ios-app-toggle';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOneByBrand(): Observable<HttpResponse<OtfIosAppToggle>> {
    return this.sendRequest<OtfIosAppToggle>('get', this.byBrandUrl, null);
  }

  public save(otfIosAppToggle: OtfIosAppToggle): Observable<HttpResponse<OtfIosAppToggle>> {
    return this.sendRequest<OtfIosAppToggle>('post', this.rootUrl, otfIosAppToggle);
  }

  public update(otfIosAppToggle: OtfIosAppToggle): Observable<HttpResponse<OtfIosAppToggle>> {
    return this.sendRequest<OtfIosAppToggle>('put', `${this.rootUrl}/${otfIosAppToggle.id}`, otfIosAppToggle);
  }
}
