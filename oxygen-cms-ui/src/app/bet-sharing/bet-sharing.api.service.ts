import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { BetShare } from '../client/private/models/betShare.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { HttpResponse, HttpClient } from '@angular/common/http';

@Injectable()
export class BetSharingAPIService extends AbstractService<BetShare>{
  private readonly SHARE_CARD_DATA: string = `bet-sharing`; // TO remove comment

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
  * Get the onboarding bet sharing by brand
  * @returns {Observable<HttpResponse<BetShare>>}
  */
  public getDetailsByBrand(): Observable<HttpResponse<BetShare>> {
    return this.sendRequest<BetShare>('get', `${this.SHARE_CARD_DATA}/brand/${this.brand}`, null);
  }

  /**
   * To Save onboarding coupon stat widget
   * @param {BetShare} request
   * @returns {Observable<HttpResponse<BetShare>>}
   */
  public saveCMSBetShareData(request: BetShare): Observable<HttpResponse<BetShare>> {
    return this.sendRequest<BetShare>('post', this.SHARE_CARD_DATA, request);
  }

  /**
  * To Update onboarding bet sharing
  * @param {BetShare} request
  * @returns {Observable<HttpResponse<BetShare>>}
  */
  public updateCMSBetShareData(request: BetShare): Observable<HttpResponse<BetShare>> {
    return this.sendRequest<BetShare>('put', `${this.SHARE_CARD_DATA}/${request.id}`, request);
  }
}
