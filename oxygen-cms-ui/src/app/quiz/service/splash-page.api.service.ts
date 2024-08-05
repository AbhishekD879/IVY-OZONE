import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {SplashPage} from '@app/client/private/models/splash-page.model';

@Injectable()
export class SplashPageApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
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

  getSplashPages(): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.splashPageService().getSplashPages();
    return this.wrappedObservable(data);
  }

  getSplashPagesByBrand(): Observable<any> {
    const data = this.apiClientService.splashPageService().getSplashPagesByBrand();
    return this.wrappedObservable(data);
  }

  getSplashPage(id: string): Observable<any> {
    const data = this.apiClientService.splashPageService().getSingleSplashPage(id);
    return this.wrappedObservable(data);
  }

  createSplashPage(splashPage: SplashPage): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.splashPageService().postNewSplashPage(splashPage);
    return this.wrappedObservable(data);
  }

  updateSplashPage(splashPage: SplashPage): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.splashPageService().putSplashPageChanges(splashPage.id, splashPage);
    return this.wrappedObservable(data);
  }

  deleteSplashPage(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.splashPageService().deleteSplashPage(id);
    return this.wrappedObservable(data);
  }

  uploadSvgFiles(id: string, background: File, logo: File, footer: File): Observable<any> {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('background', background);
    formData.append('logo', logo);
    formData.append('footer', footer);
    const  data = this.apiClientService.splashPageService().uploadSvgImage(id, formData);
    return this.wrappedObservable(data);

  }

}
