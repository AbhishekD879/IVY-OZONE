import { Injectable } from '@angular/core';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { HttpClient, HttpResponse, } from '@angular/common/http';
import { PopularBets } from '@app/client/private/models/popularBets.model';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable()
export class PopularBetsApiService extends AbstractService<PopularBets>{

  private POPULAR_BETS_DATA: string = `trending-bet`; // TO remove comment
   betType:string='';

  constructor(http: HttpClient, domain: string, brand: string, private router: Router) {
    super(http, domain, brand);
    if (this.router.url.includes('most-popular/bet-slip')) {
      this.betType = 'bet-slip';
    } else {
      this.betType = 'bet-receipt';
    }

  }

  /**
  * Get the popular bets by brand
  * @returns {Observable<HttpResponse<PopularBets>>}
  */
  public getDetailsByBrand(): Observable<HttpResponse<PopularBets>> {
    return this.sendRequest<PopularBets>('get', `${this.POPULAR_BETS_DATA}/brand/${this.brand}?type=${this.betType}`, null);
  }

  /**
   * To Save popular bets by brand
   * @param {PopularBets} request
   * @returns {Observable<HttpResponse<PopularBets>>}
   */
  public saveCMSPopularBetsData(request: PopularBets): Observable<HttpResponse<PopularBets>> {
    if (this.router.url.includes('most-popular/bet-slip')) {
     request.type=this.betType
    } else {
      request.type=this.betType
    }
    return this.sendRequest<PopularBets>('post', this.POPULAR_BETS_DATA+'?type='+this.betType, request);
  }

  /**
  * To Update popular bets
  * @param {PopularBets} request
  * @returns {Observable<HttpResponse<PopularBets>>}
  */
  public updateCMSPopularBetsData(request: PopularBets): Observable<HttpResponse<PopularBets>> {
    if (this.router.url.includes('most-popular/bet-slip')) {
      request.type=this.betType
     } else {
       request.type=this.betType
     }
    return this.sendRequest<PopularBets>('put', `${this.POPULAR_BETS_DATA}/${request.id}?type=${this.betType}`, request);
  }
}
