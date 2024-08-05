import { Injectable } from '@angular/core';
import { Observable } from 'rxjs'; 
import { HttpClient, HttpResponse } from '@angular/common/http';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { ForYou } from './for-you-personalized.model';
 
@Injectable()
export class ForYouService extends AbstractService<ForYou>{
  private readonly FOR_YOU_DATA: string = `popular-tab`;  
  constructor(http: HttpClient, domain: string, tabId: string) {
    super(http, domain, tabId);
  }
  /**
  * 
  * @returns {Observable<HttpResponse<ForYou>>}
  */
  getDetailsByBrand(tabId: string): Observable<HttpResponse<ForYou>> {
    return this.sendRequest<ForYou>('get', `${this.FOR_YOU_DATA}/${tabId}`, null);
  }

  /**
  * To Update onboarding foryouPersonalized
  * @param {ForYou} request
  * @returns {Observable<HttpResponse<ForYou>>}
  */
  public saveCMSForYouPersonalizedData(request: any): Observable<HttpResponse<ForYou>> {
    return this.sendRequest<ForYou>('put', `${this.FOR_YOU_DATA}/${request.id}`, request);
  }
}
