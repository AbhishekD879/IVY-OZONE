import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {OtfIosAppToggle} from '@app/client/private/models/otfIosAppToggle.model';

@Injectable()
export class OtfIosAppToggleApiService {
  constructor(private globalLoaderService: GlobalLoaderService,
              private apiClientService: ApiClientService) {
  }

  getOneByBrand(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData = this.apiClientService.otfIOSAppToggleService().getOneByBrand();

    return this.wrappedObservable(getData);
  }

  create(otfIOSAppToggle: OtfIosAppToggle) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.otfIOSAppToggleService().save(otfIOSAppToggle);
    return this.wrappedObservable(getData);
  }

  update(otfIOSAppToggle: OtfIosAppToggle) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.otfIOSAppToggleService().update(otfIOSAppToggle);
    return this.wrappedObservable(getData);
  }

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
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
}
