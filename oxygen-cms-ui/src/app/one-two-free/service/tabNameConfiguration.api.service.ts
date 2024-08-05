import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { Observable } from 'rxjs';
import { TabNameConfigurationData } from '../constants/otf.model';

@Injectable()
export class TabNameConfigurationApiService {

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
   * get the tab-name-configuration data
   * @param showLoader 
   * @returns {Observable<HttpResponse<TabNameConfigurationData>>}
   */
  getTabNameConfigurationData(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfSeasonBadgeService().getTabNameConfiguration();
    return this.wrappedObservable(getData);
  }

  /**
   * Create tabNameConfiguration
   * @param tabNameConfigurationData 
   * @returns {Observable<HttpResponse<TabNameConfigurationData>>}
   */
  saveTabNameConfigurationData(tabNameConfigurationData: TabNameConfigurationData) {
    this.globalLoaderService.showLoader();
    const postData = this.apiClientService.otfSeasonBadgeService().postTabNameConfigurationData(tabNameConfigurationData);
    return this.wrappedObservable(postData);
  }

    /**
   * Update tabNameConfiguration data
   * @param tabNameConfiguration 
   * @returns {Observable<HttpResponse<TabNameConfigurationData>>}
   */
    updateTabNameConfigurationData(tabNameConfigurationData: TabNameConfigurationData) {
      this.globalLoaderService.showLoader();
      const postData = this.apiClientService.otfSeasonBadgeService().putTabNameConfigurationData(tabNameConfigurationData.id, tabNameConfigurationData);
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
