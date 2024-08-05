import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { Observable } from 'rxjs';
import { MyBadges } from '@root/app/one-two-free/constants/otf.model';

@Injectable()
export class MybadgesApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) { }

  /**
  * Wrap request to handle success/error.
  * @param observableDate
  */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  /**
   * get the my badges data
   * @param showLoader 
   * @returns {Observable<HttpResponse<MyBadges>>}
   */
  getMyBadgesData(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfSeasonBadgeService().getBadgeData();
    return this.wrappedObservable(getData);
  }

  /**
   * Create My Badges
   * @param badgeData 
   * @returns {Observable<HttpResponse<MyBadges>>}
   */
  createMyBadges(badgeData: MyBadges) {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().postnewBadgeData(badgeData);
    return this.wrappedObservable(postData);
  }

  /**
   * Update My badges data
   * @param badgeData 
   * @returns {Observable<HttpResponse<MyBadges>>}
   */
  updateMyBadges(badgeData: MyBadges) {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().putBadgeChanges(badgeData.id, badgeData);
    return this.wrappedObservable(postData);
  }

  /**
   * handle request error 
   * @param error 
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
