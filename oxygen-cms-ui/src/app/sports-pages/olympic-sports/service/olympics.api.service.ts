import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Sport} from '../../../client/private/models/sport.model';
import {OlympicsImageRequestOptions} from '../../../client/private/models/olympicsImageRequestOptions';
import {Order} from '../../../client/private/models/order.model';

@Injectable()
export class OlympicsAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
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

  /**
   * Get widgets data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getOlympicsListData() {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.olympicsPageService().getOlympicsPageList();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotino data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleOlympicsItemData(id: string) {
    const getData =  this.apiClientService.olympicsPageService().getSingleOlympicsPage(id);
    return this.wrappedObservable(getData);
  }

  putOlympicsItemChanges(olympicsPage: Sport): Observable<HttpResponse<Sport>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.olympicsPageService().putOlympicsPageChanges(olympicsPage.id, olympicsPage);
    return this.wrappedObservable(getData);
  }

  postNewOlympicsFilename(id: string, formData: FormData): Observable<HttpResponse<Sport>> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.olympicsPageService().postOlympicsFilename(id, formData);
    return this.wrappedObservable(getData);
  }

  postNewOlympicsOrder(order: Order): Observable<HttpResponse<Sport>> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.olympicsPageService().reorder(order);
    return this.wrappedObservable(getData);
  }

  deleteOlympicsFilename(id: string, options: OlympicsImageRequestOptions): Observable<HttpResponse<Sport>> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.olympicsPageService().deleteOlympicsFilename(id, options);
    return this.wrappedObservable(getData);
  }

  deleteOlympicsPage(id: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.olympicsPageService().deleteOlympicsPage(id);
    return this.wrappedObservable(getData);
  }

  createOlympicsItem(olympicsPage: Sport): Observable<HttpResponse<Sport>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.olympicsPageService().postNewOlympicsPage(olympicsPage);
    return this.wrappedObservable(getData);
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
