import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { leaderBoardUserRankData } from '@app/lazy-modules/promoLeaderBoard/constants/leaderboard.model';
import { Injectable } from '@angular/core';

@Injectable()

/** FeatureName:  Promo SandBox LeaderBoard
 *   Description: API call to Fetch LeaderBoard Records
 *   Class: LeaderboardService
 **/
export class LeaderboardService {
  brand: string = environment.brand;
  constructor(
    protected http: HttpClient,
    protected userService: UserService,
    protected windowRef: WindowRefService
  ) {
  }

  /**
    * Get LeaderBoard DATA
    * @returns : Observable<leaderBoardUserRankData>
    */
  fetchleaderboard(leaderboardConfigId, userStatus, topX, promotionId): Observable<HttpResponse<leaderBoardUserRankData>> {
    const params = {
      promotionId: promotionId,
      customerId: this.getCustomerId(userStatus),
      customerRanking: userStatus,
      noOfPosition: topX,
      leaderboardId: leaderboardConfigId
    }

    const endpointUrl = environment.PROMO_LB_ENDPOINT;
    return this.http.post<leaderBoardUserRankData>(endpointUrl, params, {
      headers: this.getAuthenticationHeader(userStatus),
      observe: 'response'
    });
  }

  /**
   * Get CustomerId based on user loggedIn status
   * @returns : string
   */
  private getCustomerId(userStatus): string {
    if (userStatus) {
      const clientConfig = (this.windowRef.nativeWindow && this.windowRef.nativeWindow.clientConfig) || {};
      return clientConfig && clientConfig.vnClaims && clientConfig.vnClaims['http://api.bwin.com/v3/user/pg/nameidentifier'] && clientConfig.vnClaims['http://api.bwin.com/v3/user/pg/nameidentifier'].toString() || '';
    }
    return '';
  }

  /**
 * create HTTPHeaders
 * @returns {HttpHeaders}
 */
  private getAuthenticationHeader(userStatus): HttpHeaders {
    const token = !userStatus ? '': this.userService.bppToken;
    return new HttpHeaders({
      token: token
    });
  }

}
