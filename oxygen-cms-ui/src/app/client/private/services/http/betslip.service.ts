import { Injectable } from '@angular/core';
import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { IbetslipsAcca, IoddsBoost } from '@app/betslip/service/betslip.model';

@Injectable({
providedIn: 'root'
})
export class BetSlipService extends AbstractService<Configuration> {
    //Acca Insurance section start//
  accaBaseUrl: string = 'acca-insurance-messages';
  betslipAccaBaseUrl: string = `${this.accaBaseUrl}/brand/${this.brand}`;
  
  constructor(http: HttpClient, domain: string, brand: string) { 
    super(http, domain, brand);
  }
  public getBetSlip(): Observable<HttpResponse<IbetslipsAcca>> {
    const url = `${this.betslipAccaBaseUrl}`;
    return this.sendRequest<IbetslipsAcca>('get', url, null)  
  }

  public saveBetslip(betslipAcc: IbetslipsAcca): Observable<HttpResponse<IbetslipsAcca>> {
    return this.sendRequest<IbetslipsAcca>('post', this.accaBaseUrl, betslipAcc);
  }

  public edit(request: IbetslipsAcca): Observable<HttpResponse<IbetslipsAcca>> {
    return this.sendRequest<IbetslipsAcca>('put',`${this.accaBaseUrl}/${request.id}`, request);
  }

  public uploadSvg(id: string, file: FormData): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/${id}/image?fileType=svg`;
    return this.sendRequest<any>('post', uri, file);
  }
  //Acca Insurance section end//

  //Odds Boost messages section start//

  oddsBoost: string = 'odds-boost-messages';
  oddsBoostBaseUrl: string = `${this.oddsBoost}/brand/${this.brand}`;
  
 
  public getOddsBoost(): Observable<HttpResponse<IbetslipsAcca>> {
    const url = `${this.oddsBoostBaseUrl}`;
    return this.sendRequest<IbetslipsAcca>('get', url, null)  
  }

  public saveOddsBoost(betslipOddsBoost: IbetslipsAcca): Observable<HttpResponse<IbetslipsAcca>> {
    return this.sendRequest<IbetslipsAcca>('post', this.oddsBoost, betslipOddsBoost);
  }

  public editOddsBoost(request: IoddsBoost): Observable<HttpResponse<IbetslipsAcca>> {
    return this.sendRequest<IbetslipsAcca>('put',`${this.oddsBoost}/${request.id}`, request);
  }
 //Odds Boost messages section end//
}
