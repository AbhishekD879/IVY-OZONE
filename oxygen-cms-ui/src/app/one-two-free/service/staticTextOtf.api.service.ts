import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {StaticTextOtf} from '../../client/private/models/staticTextOtf.model';

@Injectable()
export class StaticTextOtfAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
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

  getStaticTextOtfsData(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }

    const getData =  this.apiClientService.staticTextOtfService().getStaticTextOtfs();

    return this.wrappedObservable(getData);
  }

  postNewStaticTextOtf(newStaticTextOtf: StaticTextOtf) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.staticTextOtfService().postNewStaticTextOtf(newStaticTextOtf);
    return this.wrappedObservable(getData);
  }

  deleteStaticTextOtf(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.staticTextOtfService().deleteStaticTextOtf(id);
    return this.wrappedObservable(getData);
  }

  getSingleStaticTextOtfsData(id: string) {
    const getData =  this.apiClientService.staticTextOtfService().getSingleStaticTextOtf(id);
    return this.wrappedObservable(getData);
  }

  putStaticTextOtfsChanges(staticText: StaticTextOtf) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.staticTextOtfService().putStaticTextOtfChanges(staticText.id, staticText);
    return this.wrappedObservable(getData);
  }

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
