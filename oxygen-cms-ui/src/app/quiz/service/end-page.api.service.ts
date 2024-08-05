import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {EndPage} from '@app/client/private/models/end-page.model';

@Injectable()
export class EndPageApiService {

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

  getEndPages(): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.endPageService().getEndPages();
    return this.wrappedObservable(data);
  }

  getEndPagesByBrand(): Observable<any> {
    const data = this.apiClientService.endPageService().getEndPagesByBrand();
    return this.wrappedObservable(data);
  }

  getEndPage(id: string): Observable<any> {
    const data = this.apiClientService.endPageService().getSingleEndPage(id);
    return this.wrappedObservable(data);
  }

  createEndPage(endPage: EndPage): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.endPageService().saveNewEndPage(endPage);
    return this.wrappedObservable(data);
  }

  updateEndPage(endPage: EndPage): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.endPageService().updateEndPage(endPage.id, endPage);
    return this.wrappedObservable(data);
  }

  deleteEndPage(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.endPageService().deleteEndPage(id);
    return this.wrappedObservable(data);
  }

  uploadBackground(id: string, background: File): Observable<any> {
    this.globalLoaderService.showLoader();
    const formData = new FormData();
    formData.append('background', background);

    const data = this.apiClientService.endPageService().uploadBackground(id, formData);
    return this.wrappedObservable(data);
  }
}
