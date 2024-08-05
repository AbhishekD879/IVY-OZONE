import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../../client/private/services/http/';
import { Brand } from '../../../client/private/models';
import {Order} from '../../../client/private/models/order.model';
import { HttpResponse } from '@angular/common/http';

@Injectable()
export class BrandsAPIService {
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
          const message = response.error ? response.error.message : response.message;
          this.handleRequestError(message);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Get brands data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getBrandsListData(): Observable<HttpResponse<Brand[]>>  {
   this.globalLoaderService.showLoader();

    const getData = this.apiClientService.brands().findAllBrands();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single brand data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleBrandData(id: string): Observable<HttpResponse<Brand>> {
    const getData =  this.apiClientService.brands().getSingleBrand(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to brand.
   * @param {Brand} brand
   */
  putBrandChanges(brand: Brand): Observable<HttpResponse<Brand>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.brands().editBrand(brand);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes brand.
   * @param {string} id
   */
  deleteBrand(id: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.brands().deleteBrand(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new brand.
   * @param {Brand} brand [description]
   */
  createBrand(brand: Brand): Observable<HttpResponse<Brand>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.brands().createBrand(brand);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for brands.
   * @param {any} order
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  postNewBrandsOrder(order: Order): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.brands().postNewBrandsOrder(order);

    return this.wrappedObservable(getData);
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(message) {
    this.globalLoaderService.hideLoader();
  }
}
