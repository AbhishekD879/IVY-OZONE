import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { IMatchDayRewardsResponse, IHowItWorks, IProxyError } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class EuroService {
  constructor(
    private bppService: BppService
    ) {}

  /**
   * Gets euro response
   * @param {IMatchDayRewardsResponse} euroResponse
   * @returns Observable<IMatchDayRewardsResponse>
   */
  public getMatchRewardsBadges(isUserLoggedIn: boolean): Observable<IMatchDayRewardsResponse> {
    const getEurosData = isUserLoggedIn ? 'getMatchDayRewardsWithBadges' : 'getMatchDayRewardsWithOutBadges';
    const params =  isUserLoggedIn ? {
      returnOffers: 'Y',
      returnFreebetTokens: 'N'
    } : '';
    return (this.bppService.send(getEurosData, params) as Observable<IMatchDayRewardsResponse>).pipe(
      catchError((error: IProxyError) => {
        return throwError(error);
      }));
  }

  /**
   * Gets howitworks string
   * @returns Observable<IHowItWorks>
   */
   public getHowItWorksData(): Observable<IHowItWorks> {
    return (this.bppService.send('getHowItWorksData') as Observable<IHowItWorks>).pipe(
      catchError(() => {
        return throwError('error');
      }));
  }
}
