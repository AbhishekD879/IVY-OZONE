import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { IFirstBetPlacement } from '@root/app/on-boarding-overlay/first-bet-on-boarding-overlay/first-bet-placement-overlay.model';


@Injectable()

export class firstBetPlacementService extends AbstractService<Configuration> {

    private readonly FIRST_BET_ONBOARDING: string = `first-bet-place-tutorial`; // TO remove comment
  
    constructor(http: HttpClient, domain: string, brand: string) {
      super(http, domain, brand);
    }

      /**
   * Get the onboarding first bet by brand
   * @returns {Observable<HttpResponse<IFirstBetPlacement>>}
   */
  public getDetailsByBrand(): Observable<HttpResponse<IFirstBetPlacement>> {
    return this.sendRequest<IFirstBetPlacement>('get', `${this.FIRST_BET_ONBOARDING}/brand/${this.brand}`, null);
  }

    /**
   * To Save onboarding first bet
   * @param {IFirstBetPlacement} request
   * @returns {Observable<HttpResponse<IFirstBetPlacement>>}
   */
     public saveFirstBet(request: IFirstBetPlacement): Observable<HttpResponse<IFirstBetPlacement>> {
        return this.sendRequest<IFirstBetPlacement>('post', this.FIRST_BET_ONBOARDING, request);
      }


      /**
   * To Update onboarding first bet
   * @param {IFirstBetPlacement} request
   * @returns {Observable<HttpResponse<IFirstBetPlacement>>}
   */
  public updateFirstBet(request: IFirstBetPlacement): Observable<HttpResponse<IFirstBetPlacement>> {
    return this.sendRequest<IFirstBetPlacement>('put', `${this.FIRST_BET_ONBOARDING}/${request.id}`, request);
  }

  postFirstBetBulbIcon(id: string, file: FormData): Observable<HttpResponse<IFirstBetPlacement>> {
    const apiUrl = `first-bet-place-tutorial/${id}/image`;
    return this.sendRequest<any>('post', apiUrl, file);

  }

  removeFirstBetBulbIcon(id: string): Observable<HttpResponse<IFirstBetPlacement>> {
    const apiUrl = `first-bet-place-tutorial/${id}/image`;
    return this.sendRequest<any>('delete', apiUrl, null);
  }

}