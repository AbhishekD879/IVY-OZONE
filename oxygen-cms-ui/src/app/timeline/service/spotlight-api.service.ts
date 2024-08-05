import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';

@Injectable()
export class SpotlightApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate): Observable<any> {
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

  handleRequestError(error): void {
    this.globalLoaderService.hideLoader();
  }

  hideLoader(): void {
    this.globalLoaderService.hideLoader();
  }

  getSiteServeEvents(dateFromString: string, classIdsString: string, restrictToUkAndIre: boolean, freeRide?: boolean) {
    const refreshData = this.apiClientService.timelineSpotlightService().getSiteServeEvents(dateFromString,
                                                                                            classIdsString, restrictToUkAndIre, freeRide);
    return this.wrappedObservable(refreshData);
  }

  getSpotlightsForEventId(eventId: string, campaignId: string) {
    const spotlightData = this.apiClientService.timelineSpotlightService().getSpotlightDataForEventId(eventId, campaignId);
    return this.wrappedObservable(spotlightData);
  }
}
