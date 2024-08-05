import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';

@Injectable()
export class TimelineSplashConfigApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
  }

  getOneByBrand(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const popupData = this.apiClientService.timelineSplashConfigService().getOneByBrand();

    return this.wrappedObservable(popupData);
  }

  create(timelineConfig: any) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.timelineSplashConfigService().saveConfig(timelineConfig);
    return this.wrappedObservable(getData);
  }

  update(timelineConfig: any) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.timelineSplashConfigService().updateConfig(timelineConfig);
    return this.wrappedObservable(getData);
  }

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

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
