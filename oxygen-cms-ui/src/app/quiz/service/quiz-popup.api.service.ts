import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';

@Injectable()
export class QuizPopupApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
  }

  getOneByBrand(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const popupData = this.apiClientService.quizPopupService().getOneByBrand();

    return this.wrappedObservable(popupData);
  }

  getQuizzes() {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.quizService()
      .getQuizzesByBrand();
    return this.wrappedObservable(data);
  }

  create(quizPopup: any) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.quizPopupService().saveConfig(quizPopup);
    return this.wrappedObservable(getData);
  }

  update(quizPopup: any) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.quizPopupService().updateConfig(quizPopup);
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
