import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../../client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Banner} from '../../../client/private/models/banner.model';
import { Order } from '../../../client/private/models/order.model';

@Injectable()
export class BannersApiService {
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
   * Get promotions data.
   * @returns {Observable<HttpResponse>}
   */
  getBannersData() {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.bannersService().getBanners();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotino data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleBannerData(id: string) {
    const getData =  this.apiClientService.bannersService().getSingleBanner(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Submit new created promotion
   * @param newBanner
   * @returns {any}
   */
  postNewBanner(newBanner: Banner) {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.bannersService().postNewBanner(newBanner);
    return this.wrappedObservable(getData);
  }

  /**
   * Reorder promotions
   * @param {Array<string>} newBannersOrder , sent id of promotions
   * @returns {any}
   */
  postNewBannersOrder(newBannersOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bannersService().postNewBannersOrder(newBannersOrder);
    return this.wrappedObservable(getData);
  }

  postNewBannerImage(id: string, formData: FormData) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bannersService().postNewBannerImage(id, formData);
    return this.wrappedObservable(getData);
  }

  putBannerChanges(promotion: Banner) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bannersService().putBannerChanges(promotion.id, promotion);
    return this.wrappedObservable(getData);
  }

  deleteBanner(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bannersService().deleteBanner(id);
    return this.wrappedObservable(getData);
  }

  deleteBannerImage(id: string, isDesktop: boolean) {
    this.globalLoaderService.showLoader();

    const params = {
      desktopImage: isDesktop.toString()
    };

    const getData = this.apiClientService.bannersService().removeBannerImage(id, params);
    return this.wrappedObservable(getData);
  }

  /**
   * get sport categories list to map pormotion
   * @returns {any}
   */
  getSportCategories() {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.sportCategoriesService().getSportCategories();

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
