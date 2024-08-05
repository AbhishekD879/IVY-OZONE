import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {OfferModule} from '../../client/private/models/offermodule.model';
import {Order} from '../../client/private/models/order.model';

@Injectable()
export class OfferModuleAPIService {
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

  /**
   * Get offers data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getOfferModulesData(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }

    const getData =  this.apiClientService.offerModulesService().getOfferModules();

    return this.wrappedObservable(getData);
  }

  postNewOfferModule(newOfferModule: OfferModule) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.offerModulesService().postNewOfferModule(newOfferModule);
    return this.wrappedObservable(getData);
  }

    /**
   * Reorder offer modules
   * @param {Order} newOrder , sent id of promotions
   * @returns {any}
   */
  postNewOfferModulesOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offerModulesService().postNewOfferModulesOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  deleteOfferModule(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offerModulesService().deleteOfferModule(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Load single offer data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleOfferModulesData(id: string) {
    const getData =  this.apiClientService.offerModulesService().getSingleOfferModule(id);
    return this.wrappedObservable(getData);
  }

  putOfferModulesChanges(offerModule: OfferModule) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.offerModulesService().putOfferModuleChanges(offerModule.id, offerModule);
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
