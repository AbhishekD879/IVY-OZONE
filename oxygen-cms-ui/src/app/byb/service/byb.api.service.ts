import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/';
import { BybMarket } from '../../client/private/models';
import { BYBSwitcher } from '../../client/private/models';
import { Order } from '../../client/private/models/order.model';

@Injectable()
export class BybAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param {Observable<HttpResponse<any>>} observableDate
   * @returns {Observable<HttpResponse<any>>}
   */
  private wrappedObservable(observableDate: Observable<HttpResponse<any>>): Observable<HttpResponse<any>> {
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
   * Handle networking error.
   * Notify user.
   */
  public handleRequestError(message) {
    this.globalLoaderService.hideLoader();
  }

  // Banach Switchers API
  /**
   * Get switchers data.
   * @returns {Observable<HttpResponse<BYBSwitcher[]>>}
   */
  getSwitchersList(): Observable<HttpResponse<BYBSwitcher[]>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybSwitchers().findAllSwitchers();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single switcher data to edit.
   * @param {string} id
   * @returns {Observable<HttpResponse<BYBSwitcher>>}
   */
  getSingleSwitcher(id: string): Observable<HttpResponse<BYBSwitcher>> {
    const getData =  this.apiClientService.bybSwitchers().getSingleSwitcher(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to swicther.
   * @param {BYBSwitcher} switcher
   * @returns {Observable<HttpResponse<BYBSwitcher>>}
   */
  putSwitcherChanges(switcher: BYBSwitcher): Observable<HttpResponse<BYBSwitcher>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybSwitchers().editSwitcher(switcher);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes switcher.
   * @param {string} id
   * @returns {Observable<HttpResponse<void>>}
   */
  deleteSwitcher(id: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybSwitchers().deleteSwitcher(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new swicther.
   * @param {BYBSwitcher} switcher
   * @returns Observable<HttpResponse<BYBSwitcher>>
   */
  createSwitcher(switcher: BYBSwitcher): Observable<HttpResponse<BYBSwitcher>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybSwitchers().createSwitcher(switcher);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for byb swicthers.
   * @param {Order} switchersOrder
   * @returns {Observable<HttpResponse<BYBSwitcher[]>>}
   */
  postNewSwitchersOrder(switchersOrder: Order): Observable<HttpResponse<BYBSwitcher[]>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybSwitchers().postNewSwitchersOrder(switchersOrder);

    return this.wrappedObservable(getData);
  }

  // Markets API
  /**
   * Get markets data.
   * @returns {Observable<HttpResponse<BybMarket[]>>}
   */
  public getMarketsList(): Observable<HttpResponse<BybMarket[]>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().findAllMarkets();
    return this.wrappedObservable(getData);
  }

  /**
   * Load single market data to edit.
   * @param {string} id
   * @returns {Observable<HttpResponse<BybMarket>>}
   */
  public getSingleMarket(id: string): Observable<HttpResponse<BybMarket>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().getSingleMarket(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to market.
   * @param {BybMarket} market
   * @returns {Observable<HttpResponse<BybMarket>>}
   */
  public putMarketChanges(market: BybMarket): Observable<HttpResponse<BybMarket>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().editMarket(market);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes market.
   * @param {string} id
   * @returns {Observable<HttpResponse<void>>}
   */
  public deleteMarket(id: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().deleteMarket(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new market.
   * @param {BybMarket} market
   * @returns {Observable<HttpResponse<BybMarket>>}
   */
  public createMarket(market: BybMarket): Observable<HttpResponse<BybMarket>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().createMarket(market);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for leagues.
   * @param {Order} marketsOrder
   * @returns {Observable<HttpResponse<BybMarket[]>>}
   */
  public postNewMarketsOrder(marketsOrder: Order): Observable<HttpResponse<BybMarket[]>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.bybMarkets().postNewMarketsOrder(marketsOrder);
    return this.wrappedObservable(getData);
  }
}
