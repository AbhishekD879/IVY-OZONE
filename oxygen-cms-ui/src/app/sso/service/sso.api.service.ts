import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {SsoPage} from '../../client/private/models/ssopage.model';
import {Order} from '../../client/private/models/order.model';

@Injectable()
export class SsoApiService {
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
   * get sport categories list to map pormotion
   * @returns {any}
   */
  getSportCategories() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.sportCategoriesService().getSportCategories();

    return this.wrappedObservable(getData);
  }

  /**
   * Get promotions data.
   * @returns {Observable<HttpResponse>}
   */
  getSsoPagesData(): Observable<HttpResponse<SsoPage[]>> {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.ssoPagesService().getSsoPages();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotino data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleSsoPageData(id: string): Observable<HttpResponse<SsoPage>> {
    const getData =  this.apiClientService.ssoPagesService().getSingleSsoPage(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Submit new created promotion
   * @param newSsoPage
   * @returns {any}
   */
  postNewSsoPage(newSsoPage: SsoPage): Observable<HttpResponse<SsoPage>> {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.ssoPagesService().postNewSsoPage(newSsoPage);
    return this.wrappedObservable(getData);
  }

  /**
   * Reorder promotions
   * @param {Order} newOrder
   * @returns {any}
   */
  postNewSsoPagesOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.ssoPagesService().postNewSsoPagesOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  postNewSsoPageImage(id: string, formData: FormData) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.ssoPagesService().postNewSsoPageImage(id, formData);
    return this.wrappedObservable(getData);
  }

  removeSsoPageImage(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.ssoPagesService().removeSsoPageImage(id);
    return this.wrappedObservable(getData);
  }

  putSsoPageChanges(promotion: SsoPage): Observable<HttpResponse<SsoPage>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.ssoPagesService().putSsoPageChanges(promotion.id, promotion);
    return this.wrappedObservable(getData);
  }

  deleteSsoPage(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.ssoPagesService().deleteSsoPage(id);
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
