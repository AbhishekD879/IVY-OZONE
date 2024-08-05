import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { UserService } from '@core/services/user/user.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { FREE_RIDE_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';
import { IRaceEvent, IBpError, IUserSelectionDetail } from '@lazy-modules/freeRide/models/free-ride';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import environment from '@environment/oxygenEnvConfig';

@Injectable({ providedIn: 'root' })
export class FreeRideService {

  constructor(
    private userService: UserService,
    public freeBetsService: FreeBetsService,
    public sessionStorage: SessionStorageService,
    private http: HttpClient,
    private gtmService: GtmService,
  ) {  }

  /**
   * call to get selected horse
   * @param {IUserSelectionDetail} requestSelectedHorseData
   * @returns {Observable<IRaceEvent>}
   */
  public requestSelectedHorse(requestSelectedHorseData: IUserSelectionDetail): Observable<IRaceEvent> {
    return this.http.post(environment.FREE_RIDE_PLACEBET_ENDPOINT, requestSelectedHorseData, {
        headers: this.getAuthenticationHeader()
      }).pipe(map((horseDetails: IRaceEvent) => {
        return horseDetails;
      }),
      catchError((err: IBpError) => {
        console.warn(err);
        return throwError(err);
      }));
  }

  /**
   * deletes freebet after placebet
   */
  public clearFreebet(): void {
    this.freeBetsService.isFRFreeBets.next({} as IFreebetToken);
    this.sessionStorage.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS) && this.sessionStorage.remove(FREE_RIDE_CONSTS.FREERIDE_DETAILS);
  }

  /**
   * GA for tracking freeRide
   * @param eventAction
   * @param eventLabel
   * @param eventDetails
   */
  public sendGTM(eventAction: string, eventLabel: string, eventDetails?: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: eventAction,
      eventCategory: 'free ride',
      eventLabel: eventLabel,
    };
    if (eventDetails) {
      Object.assign(gtmData, { eventDetails: eventDetails });
    }
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * create HTTPHeaders
   * @returns {HttpHeaders}
   */
  private getAuthenticationHeader(): HttpHeaders {
    return new HttpHeaders({
      token: this.userService.bppToken
    });
  }
}

