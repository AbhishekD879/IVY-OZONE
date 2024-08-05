import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@root/app/shared/globalLoader/loader.service';
import {ApiClientService} from '@root/app/client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Promotion} from '@root/app/client/private/models/promotion.model';
import {Competition} from '@root/app/client/private/models/competition.model';
import {Order} from '@root/app/client/private/models/order.model';

@Injectable()
export class PromotionsAPIService {
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
        if (response instanceof HttpErrorResponse && response.status !== 400) {
          this.handleRequestError(response.error);
        }

        this.globalLoaderService.hideLoader();
        return Observable.throw(response);
      });
  }

  /**
   * get sport categories list to map promotion
   * @returns {any}
   */
  getSportCategories() {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.sportCategoriesService().getSportCategories();

    return this.wrappedObservable(getData);
  }

  /**
   * Get big competitions list
   * @returns {Observable<HttpResponse<Competition[]>>}
   */
  getCompetitions(): Observable<HttpResponse<Competition[]>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().findAllCompetitions();

    return this.wrappedObservable(getData);
  }

  /**
   * Get promotions data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getPromotionsData() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().getPromotions();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotion data to edit
   * @param {string} id
   * @returns {any}
   */
  getSinglePromotionData(id: string) {
    const getData =  this.apiClientService.promotionsService().getSinglePromotion(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Submit new created promotion
   * @param newPromotion
   * @returns {any}
   */
  postNewPromotion(newPromotion: Promotion) {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.promotionsService().postNewPromotion(newPromotion);
    return this.wrappedObservable(getData);
  }

  /**
   * Reorder promotions
   * @param {Order} newOrder , sent id of promotions
   * @returns {any}
   */
  postNewPromotionsOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().postNewPromotionsOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  postNewPromotionImage(id: string, formData: FormData) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().postNewPromotionImage(id, formData);
    return this.wrappedObservable(getData);
  }

  removePromotionImage(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().removePromotionImage(id);
    return this.wrappedObservable(getData);
  }

  putPromotionChanges(promotion: Promotion) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().putPromotionChanges(promotion.id, promotion);
    return this.wrappedObservable(getData);
  }

  deletePromotion(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.promotionsService().deletePromotion(id);
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
