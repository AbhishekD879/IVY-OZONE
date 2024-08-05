import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Offer} from '../../client/private/models/offer.model';
import {Order} from '../../client/private/models/order.model';

@Injectable()
export class OffersAPIService {
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
   * Get offers data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getOffersData() {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.offersService().getOffers();

    return this.wrappedObservable(getData);
  }

    /**
   * Load single offer data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleOffersData(id: string) {
    const getData =  this.apiClientService.offersService().getSingleOffer(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Create new offer
   * @param newOffer - offer model which should be created and stored
   */
  postNewOffer(newOffer: Offer) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.offersService().postNewOffer(newOffer);
    return this.wrappedObservable(getData);
  }

    /**
   * Reorder offers
   * @param {Order} newOrder , sent id of offers
   * @returns {any}
   */
  postNewOffersOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offersService().postNewOfferOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  /**
   * Delete offer with provided id
   * @param id Offer id to delete
   */
  deleteOffer(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offersService().deleteOffer(id);
    return this.wrappedObservable(getData);
  }

  postNewOfferImage(id: string, formData: FormData) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offersService().postNewOfferImage(id, formData);
    return this.wrappedObservable(getData);
  }

  removeOfferImage(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offersService().removeOfferImage(id);
    return this.wrappedObservable(getData);
  }

  putOfferChanges(offer: Offer) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offersService().putOfferChanges(offer.id, offer);
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
