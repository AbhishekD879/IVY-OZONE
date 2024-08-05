import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { ITermsAndConditions } from '@app/five-a-side-showdown/models/terms-and-conditions';

@Injectable()
/**
 * Contest Manager service for creation removal, editing , uploading of contests
 * and prizes
 */
export class TermsAndConditionsService extends AbstractService<Configuration> {
  private readonly TANDC_URL: string = `termsandcondition`; // TO remove comment

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the terms and conditions by brand
   * @returns {Observable<HttpResponse<TermsAndConditionsService[]>>}
   */
  public getDetailsByBrand(): Observable<HttpResponse<ITermsAndConditions>> {
    return this.sendRequest<ITermsAndConditions>('get', `${this.TANDC_URL}/${this.brand}`, null);
  }

  /**
   * To Save terms and conditions
   * @param {ITermsAndConditions} request
   * @returns {Observable<HttpResponse<ITermsAndConditions>>}
   */
  public saveTermsAndConditions(request: ITermsAndConditions): Observable<HttpResponse<ITermsAndConditions>> {
    return this.sendRequest<ITermsAndConditions>('post', this.TANDC_URL, request);
  }

  /**
   * To Update terms and conditions
   * @param {ITermsAndConditions} request
   * @returns {Observable<HttpResponse<ITermsAndConditions>>}
   */
  public updateTermsAndConditions(request: ITermsAndConditions): Observable<HttpResponse<ITermsAndConditions>> {
    return this.sendRequest<ITermsAndConditions>('put', `${this.TANDC_URL}/${request.id}`, request);
  }
}
