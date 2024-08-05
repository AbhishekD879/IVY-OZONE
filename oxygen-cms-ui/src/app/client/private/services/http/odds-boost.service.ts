import { OddsBoost } from '../../models/odds-boost.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

import { AbstractService } from './transport/abstract.service';

@Injectable()
export class OddsBoostService extends AbstractService<OddsBoost> {

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `odds-boost`;
  }

  public get(): Observable<HttpResponse<OddsBoost>> {
    const uri = `${this.uri}/${this.brand}`;
    return this.sendRequest<OddsBoost>('get', uri, null);
  }

  public udpate(oddsBoost: OddsBoost): Observable<HttpResponse<OddsBoost>> {
    const uri = `${this.uri}/${this.brand}`;
    return this.sendRequest<OddsBoost>('put', uri, oddsBoost);
  }

  public uploadSvg(file: FormData): Observable<HttpResponse<OddsBoost>> {
    const uri = `${this.uri}/${this.brand}/image?fileType=svg`;
    return this.sendRequest<OddsBoost>('post', uri, file);
  }

  public removeSvg(): Observable<HttpResponse<OddsBoost>> {
    const uri = `${this.uri}/${this.brand}/image?fileType=svg`;
    return this.sendRequest<OddsBoost>('delete', uri, null);
  }
}
